# 🎬 K-Video Trim

Ferramenta simples: Ela corta vídeos.

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/)

## Como usar

```bash
1. Clone o projeto
git clone https://github.com/kerstenbr/k-videotrim.git

2. Entre na pasta
cd k-videotrim

3. Suba o container
docker compose up --build

4. Acesse no browser em
http://localhost:8000
```

## Uso da ferramenta

1. **Arraste** um vídeo para a área central (ou clique para selecionar)
2. Formatos aceitos: MP4, MOV, MKV, WEBM, AVI
3. Use os **handles** verde (IN) e vermelho (OUT) na timeline para definir o trecho
4. Clique **Marcar IN** / **Marcar OUT** para capturar a posição atual do player
5. Clique **Preview** para assistir apenas o trecho selecionado
6. Clique **Exportar** — o arquivo cortado e baixado automaticamente

## Atalhos de teclado

| Tecla        | Ação                     |
|--------------|--------------------------|
| `Space`      | Play / Pause             |
| `I`          | Marcar ponto IN          |
| `O`          | Marcar ponto OUT         |
| `←`          | Retroceder 1 segundo     |
| `→`          | Avançar 1 segundo        |
| `P`          | Preview do trecho        |
| `E`          | Exportar                 |
| `Ctrl+O`     | Abrir outro arquivo      |