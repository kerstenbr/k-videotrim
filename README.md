<p align="center">
  <img src="logo.png" alt="K-Video Trim logo" width="180" />
</p>

<h1 align="center">K-Video Trim</h1>

<p align="center">
  <strong>Keep the part you want.</strong><br />
  A simple video trimmer you can run on your own machine.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> ·
  <a href="#features">Features</a> ·
  <a href="#how-to-use">How to Use</a> ·
  <a href="#keyboard-shortcuts">Keyboard Shortcuts</a>
</p>

---

Drop in a video, pick the start and end, and download your clip. K-Video Trim keeps things simple with a browser interface and FFmpeg handling the cut behind the scenes.

## Quick Start

You'll need [Docker](https://docs.docker.com/get-docker/) with [Docker Compose](https://docs.docker.com/compose/) installed and running.

```bash
git clone https://github.com/kerstenbr/k-videotrim.git
cd k-videotrim
docker compose up --build
```

Open **[localhost:8000](http://localhost:8000)** in your browser and drop in a video.

<details>
<summary>Run in the background or stop the app</summary>

To keep the app running in the background:

```bash
docker compose up --build -d
```

To stop it:

```bash
docker compose down
```

</details>

## Features

- **Drag and drop** — open a video by dropping it onto the page or choosing a file.
- **Visual trimming** — drag the green IN and red OUT handles to select your clip.
- **Selection preview** — watch just the selected section before exporting.
- **Quick export** — FFmpeg copies the streams without re-encoding.
- **Keyboard shortcuts** — control playback, set trim points, and export from the keyboard.
- **Run it yourself** — a single Docker Compose command starts the app on your machine.

**Accepted formats:** MP4, MOV, MKV, WEBM, and AVI. Browser preview support depends on the video's format and codecs.

## How to Use

1. **Open a video.** Drag it onto the upload area or click to browse your files.
2. **Choose your clip.** Move the green **IN** and red **OUT** handles on the timeline. You can also move the playhead and mark each point with **I** or **O**.
3. **Preview the selection.** Click **Preview** or press **P** to watch the section you've chosen.
4. **Export.** Click the export button or press **E**. Your trimmed video downloads automatically.

The interface currently uses Portuguese labels: **Marcar IN** and **Marcar OUT** set the trim points, and **Exportar** downloads the clip.

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `Space` | Play / pause |
| `I` | Set the IN point |
| `O` | Set the OUT point |
| `←` | Seek backward 1 second |
| `→` | Seek forward 1 second |
| `P` | Preview the selected section |
| `E` | Export the clip |
| `Ctrl+O` / `⌘+O` | Open another file |

## Under the Hood

The interface uses plain HTML, CSS, and JavaScript. A Python **FastAPI** backend receives the video and trims it with **FFmpeg**, then returns the file for download.

Exports use stream copy (`-c copy`) to avoid re-encoding. Cut boundaries can depend on keyframes, so exports may not match the preview frame for frame.
