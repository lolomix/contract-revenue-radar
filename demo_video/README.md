# Demo Video

Generate a local MP4 walkthrough for the Qdrant submission:

```bash
.venv/bin/pip install pillow
.venv/bin/python scripts/create_demo_video.py
```

Output:

```text
demo_video/contract_revenue_radar_qdrant_demo.mp4
```

The video is generated locally with `ffmpeg` and `espeak-ng`. It is under the 3-minute target and can be uploaded to YouTube, Loom, Google Drive, Dropbox, or another service accepted by the Qdrant submission form.

Install all Python extras at once:

```bash
.venv/bin/pip install -e ".[qdrant,demo]"
```
