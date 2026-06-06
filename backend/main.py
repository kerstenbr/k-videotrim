import os
import uuid
import subprocess
import asyncio
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

UPLOAD_DIR = Path("/tmp/k-videotrim_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm", ".avi"}

app = FastAPI(title="K-Video Trim")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def cleanup_files(*paths: Path):
    for p in paths:
        try:
            if p and p.exists():
                p.unlink()
        except Exception:
            pass


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    frontend_path = Path("/app/frontend/index.html")
    if not frontend_path.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return HTMLResponse(content=frontend_path.read_text(encoding="utf-8"))


@app.post("/api/trim")
async def trim_video(
    file: UploadFile = File(...),
    start: float = Form(...),
    end: float = Form(...),
):
    # Validações
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não suportado: {ext}. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    if start < 0:
        raise HTTPException(status_code=400, detail="Tempo de início não pode ser negativo.")

    if end <= start:
        raise HTTPException(
            status_code=400,
            detail=f"Tempo de fim ({end}s) deve ser maior que o início ({start}s)."
        )

    session_id = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{session_id}_input{ext}"
    output_path = UPLOAD_DIR / f"{session_id}_output{ext}"

    try:
        # Salvar arquivo recebido
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Arquivo vazio recebido.")

        input_path.write_bytes(content)

        # Montar nome de saída com timecodes
        def fmt(s: float) -> str:
            h = int(s // 3600)
            m = int((s % 3600) // 60)
            sec = s % 60
            return f"{h:02d}h{m:02d}m{sec:05.2f}s"

        stem = Path(file.filename).stem
        output_filename = f"{stem}_trim_{fmt(start)}-{fmt(end)}{ext}"

        # Executar FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-ss", str(start),
            "-to", str(end),
            "-c", "copy",
            "-avoid_negative_ts", "1",
            str(output_path)
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            error_msg = stderr.decode(errors="replace")[-500:]
            raise HTTPException(
                status_code=500,
                detail=f"Erro no FFmpeg: {error_msg}"
            )

        if not output_path.exists() or output_path.stat().st_size == 0:
            raise HTTPException(
                status_code=500,
                detail="FFmpeg não gerou o arquivo de saída."
            )

        # Retornar arquivo e agendar limpeza
        response = FileResponse(
            path=str(output_path),
            media_type="video/mp4",
            filename=output_filename,
            headers={"Content-Disposition": f'attachment; filename="{output_filename}"'},
        )

        # Agendar limpeza após envio (background)
        async def _cleanup():
            await asyncio.sleep(30)
            cleanup_files(input_path, output_path)

        asyncio.create_task(_cleanup())

        return response

    except HTTPException:
        cleanup_files(input_path, output_path)
        raise
    except Exception as e:
        cleanup_files(input_path, output_path)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")