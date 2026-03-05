import streamlit as st
import streamlit.components.v1 as components
import subprocess
import tempfile
import base64 as _b64
import os
import math
import io
import urllib.request
from PIL import Image

LOGO_URL       = "https://github.com/lucasbe-lpr/luluflix/blob/main/luluflix.png?raw=true"
DEFAULT_WM_URL = "https://github.com/lucasbe-lpr/luluflix/blob/main/lpr.png?raw=true"
FAVICON_URL    = "https://github.com/lucasbe-lpr/luluflix/blob/main/favicon.png?raw=true"

try:
    _fav_data = urllib.request.urlopen(FAVICON_URL).read()
    _fav_img  = Image.open(io.BytesIO(_fav_data))
except Exception:
    _fav_img  = "▶"

st.set_page_config(
    page_title="Luluflix",
    page_icon=_fav_img,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&family=Roboto+Condensed:wght@400;500;700&display=swap');

:root {
  --blue:      #0068B1;
  --blue-dim:  #e8f2fb;
  --white:     #ffffff;
  --bg:        #fafafa;
  --ink:       #111111;
  --sub:       #555555;
  --muted:     #999999;
  --border:    #e4e4e4;
  --border-mid:#d0d0d0;
  --green:     #166534;
  --red:       #991b1b;
  --red-bg:    #fff1f1;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
  background: var(--white) !important;
  color: var(--ink) !important;
  font-family: 'Roboto', sans-serif !important;
  font-weight: 400 !important;
}
.block-container {
  background: var(--white) !important;
  padding: 0 2rem 5rem !important;
  max-width: 600px !important;
}
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.site-header {
  padding: 2rem 0 1.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.8rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.site-header img { height: 44px; width: auto; display: block; }
.site-header-right { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.01em; }

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important; margin-bottom: 1.8rem !important; padding: 0 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 1.5px solid transparent !important;
  margin-bottom: -1px !important;
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.85rem !important;
  font-weight: 400 !important;
  padding: 0.6rem 1.4rem 0.6rem 0 !important;
  transition: color 0.12s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--ink) !important;
  font-weight: 500 !important;
  border-bottom: 1.5px solid var(--blue) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: var(--sub) !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }

[data-testid="stFileUploader"] { background: transparent !important; margin-bottom: 1.6rem !important; }
[data-testid="stFileUploader"] section {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  padding: 1.6rem 1.4rem !important;
  transition: border-color 0.15s, background 0.15s !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploader"] section:focus-within {
  border-color: var(--blue) !important;
  background: var(--blue-dim) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { text-align: center !important; }
[data-testid="stFileUploaderDropzoneInstructions"] * {
  color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.82rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span { color: var(--sub) !important; font-weight: 500 !important; }
[data-testid="stFileUploader"] button {
  background: var(--white) !important;
  border: 1px solid var(--border-mid) !important;
  color: var(--sub) !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 0.78rem !important;
  padding: 0.28rem 0.9rem !important;
  border-radius: 999px !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06) !important;
}
[data-testid="stFileUploader"] button:hover { border-color: var(--blue) !important; color: var(--blue) !important; }
[data-testid="stFileUploaderFileName"] { color: var(--ink) !important; font-weight: 500 !important; font-size: 0.82rem !important; }
[data-testid="stFileUploaderDeleteBtn"] button {
  background: transparent !important; border: none !important;
  color: var(--muted) !important; box-shadow: none !important; border-radius: 4px !important;
}
[data-testid="stFileUploaderDeleteBtn"] button:hover { color: var(--red) !important; background: var(--red-bg) !important; }

.section-label {
  font-size: 0.7rem; font-weight: 500; color: var(--muted);
  letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 0.6rem; margin-top: 0;
}
.specs-row {
  display: flex; border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; margin-bottom: 1.6rem; background: var(--bg);
}
.spec-cell {
  flex: 1; padding: 0.75rem 1rem; border-right: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 0.18rem;
}
.spec-cell:last-child { border-right: none; }
.spec-k { font-size: 0.58rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.07em; color: var(--muted); }
.spec-v { font-size: 0.92rem; font-weight: 500; color: var(--ink); line-height: 1.2; }

.preview-wrap {
  border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; margin-bottom: 1.2rem; background: #f0f0f0;
}
.preview-bar {
  padding: 0.35rem 0.85rem; border-bottom: 1px solid var(--border);
  background: var(--white); font-size: 0.62rem; color: var(--muted);
  font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase;
}

div.stButton > button {
  width: 100% !important; background: var(--blue) !important; border: none !important;
  color: var(--white) !important; font-family: 'Roboto', sans-serif !important;
  font-size: 0.85rem !important; font-weight: 500 !important;
  padding: 0 1.4rem !important; height: 38px !important; border-radius: 999px !important;
  transition: background 0.15s, transform 0.1s !important;
  box-shadow: 0 1px 2px rgba(0,104,177,0.15), 0 2px 6px rgba(0,104,177,0.1) !important;
  cursor: pointer !important;
}
div.stButton > button:hover { background: #005fa8 !important; transform: translateY(-1px) !important; }
div.stButton > button:active { transform: translateY(0) !important; }
div.stButton > button:disabled {
  background: var(--border) !important; color: var(--muted) !important;
  box-shadow: none !important; cursor: default !important; transform: none !important;
}

div.stDownloadButton > button,
div[data-testid="stDownloadButton"] > button {
  width: 100% !important; background: #16a34a !important; border: none !important;
  color: #fff !important; font-family: 'Roboto', sans-serif !important;
  font-size: 0.85rem !important; font-weight: 500 !important;
  padding: 0 1.4rem !important; height: 38px !important; border-radius: 999px !important;
  transition: background 0.15s, transform 0.1s !important;
  box-shadow: 0 1px 2px rgba(22,163,74,0.18), 0 2px 6px rgba(22,163,74,0.1) !important;
}
div.stDownloadButton > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
  background: #15803d !important; transform: translateY(-1px) !important;
}
div.stDownloadButton > button:active,
div[data-testid="stDownloadButton"] > button:active { transform: translateY(0) !important; }

div[data-testid="stProgress"] { display: none !important; }

.encoding-wrap { display: flex; align-items: center; gap: 0.7rem; padding: 0.5rem 0; margin: 0.5rem 0; }
.encoding-ring {
  width: 16px; height: 16px; border: 2px solid var(--border);
  border-top-color: var(--blue); border-radius: 50%; flex-shrink: 0;
  animation: spin 0.75s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.encoding-text { font-size: 0.8rem; color: var(--sub); }

.fake-progress-wrap { margin: 0.6rem 0 0.4rem; }
.fake-progress-track { height: 3px; background: var(--border); border-radius: 99px; overflow: hidden; }
.fake-progress-bar {
  height: 100%; border-radius: 99px;
  background: linear-gradient(90deg, var(--blue-dim), var(--blue), var(--blue-dim));
  background-size: 200% 100%; animation: indeterminate 1.4s ease-in-out infinite;
}
@keyframes indeterminate { 0% { background-position: 200% center; } 100% { background-position: -200% center; } }

.status { font-size: 0.78rem; padding: 0.5rem 0; margin: 0.5rem 0; color: var(--muted); line-height: 1.4; }
.status-ok  { color: var(--green); }
.status-err { color: var(--red); }
.status-idle { color: var(--muted); }

.site-footer {
  margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  font-size: 0.7rem; color: var(--muted);
}
.footer-name { color: var(--sub); font-weight: 500; }

div[data-testid="stSpinner"] p {
  font-size: 0.78rem !important; color: var(--muted) !important;
  font-family: 'Roboto', sans-serif !important;
}

[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] [data-baseweb="base-input"] {
  align-items: center !important;
}
[data-testid="stNumberInputStepDown"],
[data-testid="stNumberInputStepUp"] {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  align-self: center !important;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  min-height: 28px !important;
  padding: 0 !important;
  margin: 0 2px !important;
  background: transparent !important;
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  color: var(--sub) !important;
  box-shadow: none !important;
  cursor: pointer !important;
}
[data-testid="stNumberInputStepDown"]:hover,
[data-testid="stNumberInputStepUp"]:hover {
  background: var(--bg) !important;
  border-color: var(--border-mid) !important;
  color: var(--ink) !important;
  box-shadow: none !important;
}
[data-testid="stNumberInputStepDown"] svg,
[data-testid="stNumberInputStepUp"] svg {
  width: 12px !important;
  height: 12px !important;
  display: block !important;
}
[data-testid="stNumberInput"] [data-baseweb="base-input"]:focus-within {
  border-color: var(--border-mid) !important;
  box-shadow: none !important;
}
[data-testid="stNumberInput"] input:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="site-header">
  <img src="{LOGO_URL}" alt="Luluflix" />
  <span class="site-header-right">outils vidéo</span>
</div>
""", unsafe_allow_html=True)


def get_default_logo() -> str:
    if "default_logo_path" not in st.session_state:
        tmp = tempfile.mkdtemp()
        path = os.path.join(tmp, "default_wm.png")
        urllib.request.urlretrieve(DEFAULT_WM_URL, path)
        st.session_state.default_logo_path = path
    return st.session_state.default_logo_path

def composite_logo(base: Image.Image, logo_path: str, force_w: int = None, force_h: int = None) -> Image.Image:
    W = force_w if force_w else base.size[0]
    H = force_h if force_h else base.size[1]
    logo_w = int(math.sqrt(W**2 + H**2) * 0.1307)
    logo = Image.open(logo_path).convert("RGBA")
    ratio = logo_w / logo.width
    logo = logo.resize((logo_w, int(logo.height * ratio)), Image.LANCZOS)
    x = W - logo_w - int(W * 0.05)
    y = int(H * 0.07)
    out = base.convert("RGBA")
    out.paste(logo, (x, y), logo)
    return out

def get_video_info(path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=0", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = {}
    for line in result.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            info[k.strip()] = v.strip()
    w = int(info.get("width", 0))
    h = int(info.get("height", 0))
    dur = float(info.get("duration", 0))
    fps_raw = info.get("r_frame_rate", "25/1")
    try:
        num, den = fps_raw.split("/")
        fps = round(float(num) / float(den), 2)
    except Exception:
        fps = 25.0
    return {"width": w, "height": h, "duration": dur, "fps": fps}

def fmt_time(secs: float) -> str:
    m, s = divmod(int(secs), 60)
    return f"{m}:{s:02d}"

def extract_frame(video_path: str, timecode: float) -> Image.Image:
    result = subprocess.run([
        "ffmpeg", "-y", "-ss", str(timecode), "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"
    ], capture_output=True)
    return Image.open(io.BytesIO(result.stdout)).convert("RGB")

def make_thumbnail(video_path: str, logo_path: str, info: dict) -> Image.Image:
    result = subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vframes", "1", "-f", "image2pipe", "-vcodec", "png", "pipe:1"
    ], capture_output=True)
    frame = Image.open(io.BytesIO(result.stdout)).convert("RGBA")
    return composite_logo(frame, logo_path, force_w=info["width"], force_h=info["height"]).convert("RGB")

def render_video(video_path: str, logo_path: str, output_path: str, info: dict, progress_cb=None):
    W, H = info["width"], info["height"]
    logo_w = int(math.sqrt(W**2 + H**2) * 0.1307)
    x = W - logo_w - int(W * 0.05)
    y = int(H * 0.07)
    filter_complex = f"[1:v]scale={logo_w}:-1[logo];[0:v][logo]overlay={x}:{y}"
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path, "-i", logo_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "copy", "-movflags", "+faststart",
        "-progress", "pipe:1", output_path
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    total = info["duration"]
    while True:
        line = process.stdout.readline()
        if not line: break
        if line.strip().startswith("out_time_ms="):
            try:
                ms = int(line.strip().split("=")[1])
                if total > 0 and progress_cb:
                    progress_cb(min(ms / 1_000_000 / total, 1.0))
            except Exception:
                pass
    process.wait()
    if process.returncode != 0:
        raise RuntimeError(process.stderr.read())

def trim_video(video_path: str, output_path: str, t_start: float, t_end: float):
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(t_start), "-to", str(t_end),
        "-i", video_path,
        "-c", "copy", "-movflags", "+faststart",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())


for k in ["thumbnail", "rendered_bytes", "trim_bytes", "_last_video_name", "_last_trim_name"]:
    if k not in st.session_state:
        st.session_state[k] = None

tab_v, tab_p, tab_s, tab_t = st.tabs(["Watermark vidéo", "Watermark photo", "Capture d'écran", "Couper une vidéo (βêta)"])


with tab_v:
    st.markdown('<p class="section-label">Source</p>', unsafe_allow_html=True)
    video_file = st.file_uploader(
        "Déposez votre vidéo ici",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        key="vu", label_visibility="collapsed"
    )
    if video_file:
        if st.session_state._last_video_name != video_file.name:
            st.session_state.thumbnail = None
            st.session_state.rendered_bytes = None
            st.session_state._last_video_name = video_file.name
        lp = get_default_logo()
        tmp = tempfile.mkdtemp()
        vp = os.path.join(tmp, "src" + os.path.splitext(video_file.name)[1])
        with open(vp, "wb") as f: f.write(video_file.read())
        nfo = get_video_info(vp)
        st.markdown(f"""
        <div class="specs-row">
          <div class="spec-cell"><span class="spec-k">Largeur</span><span class="spec-v">{nfo['width']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Hauteur</span><span class="spec-v">{nfo['height']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Durée</span><span class="spec-v">{fmt_time(nfo['duration'])}</span></div>
          <div class="spec-cell"><span class="spec-k">FPS</span><span class="spec-v">{nfo['fps']}</span></div>
        </div>""", unsafe_allow_html=True)
        if st.session_state.thumbnail is None:
            with st.spinner("Génération de l'aperçu…"):
                st.session_state.thumbnail = make_thumbnail(vp, lp, nfo)
        st.markdown('<div class="preview-wrap"><div class="preview-bar">Aperçu</div>', unsafe_allow_html=True)
        st.image(st.session_state.thumbnail, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.rendered_bytes:
            if st.button("Générer le rendu", key="vbtn"):
                out = os.path.join(tmp, "video_ready_to_post.mp4")
                ph = st.empty()
                ph.markdown('<div class="encoding-wrap"><div class="encoding-ring"></div><span class="encoding-text">Encodage en cours…</span></div><div class="fake-progress-wrap"><div class="fake-progress-track"><div class="fake-progress-bar"></div></div></div>', unsafe_allow_html=True)
                try:
                    render_video(vp, lp, out, nfo)
                    ph.empty()
                    with open(out, "rb") as f:
                        st.session_state.rendered_bytes = f.read()
                    st.rerun()
                except Exception as e:
                    ph.markdown(f'<div class="status status-err">Erreur : {e}</div>', unsafe_allow_html=True)
        else:
            st.download_button("↓  Télécharger la vidéo", data=st.session_state.rendered_bytes,
                file_name="video_ready_to_post.mp4", mime="video/mp4", key="vdl")
    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo via "Browse files".</div>', unsafe_allow_html=True)


with tab_p:
    st.markdown('<p class="section-label">Source</p>', unsafe_allow_html=True)
    photo_file = st.file_uploader("Déposez votre image ici", type=["png", "jpg", "jpeg"],
        key="pu", label_visibility="collapsed")
    if photo_file:
        lp2 = get_default_logo()
        base = Image.open(photo_file)
        W, H = base.size
        fmt = (base.format or photo_file.name.rsplit(".", 1)[-1]).upper()
        st.markdown(f"""
        <div class="specs-row">
          <div class="spec-cell"><span class="spec-k">Largeur</span><span class="spec-v">{W} px</span></div>
          <div class="spec-cell"><span class="spec-k">Hauteur</span><span class="spec-v">{H} px</span></div>
          <div class="spec-cell"><span class="spec-k">Format</span><span class="spec-v">{fmt}</span></div>
          <div class="spec-cell"><span class="spec-k">Logo</span><span class="spec-v">{int(math.sqrt(W**2+H**2)*0.1307)} px</span></div>
        </div>""", unsafe_allow_html=True)
        result_img = composite_logo(base, lp2)
        st.markdown('<div class="preview-wrap"><div class="preview-bar">Aperçu</div>', unsafe_allow_html=True)
        st.image(result_img.convert("RGB"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        buf = io.BytesIO()
        ext = photo_file.name.rsplit(".", 1)[-1].lower()
        if ext == "png":
            result_img.save(buf, format="PNG")
            fname, mime = "photo_ready_to_post.png", "image/png"
        else:
            result_img.convert("RGB").save(buf, format="JPEG", quality=97, subsampling=0)
            fname, mime = "photo_ready_to_post.jpg", "image/jpeg"
        st.download_button("↓  Télécharger la photo", data=buf.getvalue(),
            file_name=fname, mime=mime, key="pdl")
    else:
        st.markdown('<div class="status status-idle">Déposez une image via "Browse files".</div>', unsafe_allow_html=True)


with tab_s:
    st.markdown('<p class="section-label">Source</p>', unsafe_allow_html=True)
    scr_file = st.file_uploader("Déposez votre vidéo ici", type=["mp4", "mov", "avi", "mkv", "webm"],
        key="su", label_visibility="collapsed")
    if scr_file:
        tmp_s = tempfile.mkdtemp()
        sp = os.path.join(tmp_s, "src" + os.path.splitext(scr_file.name)[1])
        with open(sp, "wb") as f: f.write(scr_file.read())
        nfo_s = get_video_info(sp)
        dur_s = nfo_s["duration"]
        st.markdown(f"""
        <div class="specs-row">
          <div class="spec-cell"><span class="spec-k">Largeur</span><span class="spec-v">{nfo_s['width']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Hauteur</span><span class="spec-v">{nfo_s['height']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Durée</span><span class="spec-v">{fmt_time(dur_s)}</span></div>
          <div class="spec-cell"><span class="spec-k">FPS</span><span class="spec-v">{nfo_s['fps']}</span></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Timecode (secondes)</p>', unsafe_allow_html=True)
        timecode = st.number_input(
            "tc", min_value=0.0, max_value=float(dur_s),
            value=float(st.session_state.get("cap_tc_ni", 0.0)),
            step=0.1, format="%.2f",
            key="cap_tc_ni", label_visibility="collapsed")
        with st.spinner(""):
            frame = extract_frame(sp, timecode)
        st.markdown(f'<div class="preview-wrap"><div class="preview-bar">Aperçu — {fmt_time(timecode)} / {fmt_time(dur_s)}</div>', unsafe_allow_html=True)
        st.image(frame, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        buf_s = io.BytesIO()
        frame.save(buf_s, format="PNG")
        st.download_button("↓  Télécharger la capture", data=buf_s.getvalue(),
            file_name=f"capture_{fmt_time(timecode).replace(':', '-')}.png",
            mime="image/png", key="sdl")
    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo via "Browse files".</div>', unsafe_allow_html=True)


with tab_t:
    st.markdown('<p class="section-label">Source</p>', unsafe_allow_html=True)
    trim_file = st.file_uploader("Déposez votre vidéo ici", type=["mp4", "mov", "avi", "mkv", "webm"],
        key="tu", label_visibility="collapsed")
    if trim_file:
        if st.session_state._last_trim_name != trim_file.name:
            st.session_state.trim_bytes = None
            st.session_state._last_trim_name = trim_file.name
        tmp_t = tempfile.mkdtemp()
        tp = os.path.join(tmp_t, "src" + os.path.splitext(trim_file.name)[1])
        with open(tp, "wb") as f: f.write(trim_file.read())
        nfo_t = get_video_info(tp)
        dur_t = nfo_t["duration"]
        st.markdown(f"""
        <div class="specs-row">
          <div class="spec-cell"><span class="spec-k">Largeur</span><span class="spec-v">{nfo_t['width']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Hauteur</span><span class="spec-v">{nfo_t['height']} px</span></div>
          <div class="spec-cell"><span class="spec-k">Durée</span><span class="spec-v">{fmt_time(dur_t)}</span></div>
          <div class="spec-cell"><span class="spec-k">FPS</span><span class="spec-v">{nfo_t['fps']}</span></div>
        </div>""", unsafe_allow_html=True)

        with open(tp, "rb") as f:
            vid_b64 = _b64.b64encode(f.read()).decode()
        ext_mime = "video/mp4"
        if tp.endswith(".mov"): ext_mime = "video/quicktime"
        elif tp.endswith(".webm"): ext_mime = "video/webm"

        dur_t_str = str(round(dur_t, 4))
        dur_t_fmt = fmt_time(dur_t)

        html_parts = []
        html_parts.append("<!DOCTYPE html><html><head>")
        html_parts.append("<meta charset='utf-8'>")
        html_parts.append("<meta name='viewport' content='width=device-width,initial-scale=1'>")
        html_parts.append("<style>")
        html_parts.append("*{box-sizing:border-box;margin:0;padding:0;}")
        html_parts.append("body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fff;padding:0 0 24px;}")
        html_parts.append("video{width:100%;border-radius:10px;background:#111;display:block;max-height:260px;object-fit:contain;}")
        html_parts.append(".pbar{display:flex;align-items:center;gap:10px;margin-top:10px;}")
        html_parts.append(".pbtn{width:34px;height:34px;border-radius:50%;border:1.5px solid #e4e4e4;background:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:border-color .12s,box-shadow .12s;outline:none;}")
        html_parts.append(".pbtn:hover{border-color:#0068B1;box-shadow:0 0 0 3px rgba(0,104,177,.1);}")
        html_parts.append(".pbtn svg{width:11px;height:11px;fill:#444;pointer-events:none;}")
        html_parts.append(".tdisp{font-size:11px;color:#999;flex-shrink:0;min-width:78px;text-align:right;font-variant-numeric:tabular-nums;}")
        html_parts.append(".pwrap{flex:1;position:relative;height:32px;display:flex;align-items:center;cursor:pointer;}")
        html_parts.append(".ptrack{position:absolute;left:0;right:0;height:3px;background:#ebebeb;border-radius:99px;}")
        html_parts.append(".psel{position:absolute;height:3px;background:#d4e6f5;border-radius:99px;pointer-events:none;z-index:1;}")
        html_parts.append(".pfill{position:absolute;height:3px;background:#0068B1;border-radius:99px;pointer-events:none;z-index:2;}")
        html_parts.append(".pmark-s,.pmark-e{position:absolute;top:50%;transform:translateY(-50%);width:1px;height:10px;background:#0068B1;opacity:.5;pointer-events:none;z-index:3;}")
        html_parts.append(".ph{position:absolute;top:50%;transform:translate(-50%,-50%);width:4px;height:16px;background:#0068B1;border-radius:99px;cursor:grab;z-index:5;transition:height .1s,opacity .1s;}")
        html_parts.append(".ph:hover{height:20px;}")
        html_parts.append(".ph:active{cursor:grabbing;opacity:.75;}")
        html_parts.append(".sect{margin-top:22px;}")
        html_parts.append(".sect-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}")
        html_parts.append(".clbl{font-size:10px;font-weight:500;color:#aaa;letter-spacing:.06em;text-transform:uppercase;}")
        html_parts.append(".srange{font-size:12px;font-weight:500;color:#555;font-variant-numeric:tabular-nums;}")
        html_parts.append(".srange em{font-style:normal;color:#0068B1;font-weight:600;}")
        html_parts.append(".cwrap{position:relative;height:40px;display:flex;align-items:center;user-select:none;touch-action:none;margin:0 8px;overflow:visible;}")
        html_parts.append(".ctrack{position:absolute;left:0;right:0;height:3px;background:#ebebeb;border-radius:99px;}")
        html_parts.append(".csel{position:absolute;height:3px;background:#0068B1;opacity:.25;border-radius:99px;pointer-events:none;}")
        html_parts.append(".chandle{position:absolute;top:50%;transform:translate(-50%,-50%);width:6px;height:22px;background:#0068B1;border-radius:99px;cursor:ew-resize;z-index:3;transition:width .1s,opacity .1s;}")
        html_parts.append(".chandle:hover,.chandle.dragging{width:8px;}")
        html_parts.append(".dur-chip{display:inline-block;background:#eef5fb;color:#0068B1;font-size:10px;font-weight:600;letter-spacing:.03em;padding:2px 7px;border-radius:99px;margin-left:7px;}")
        html_parts.append("</style></head><body>")

        html_parts.append("<video id='vid' src='data:" + ext_mime + ";base64," + vid_b64 + "' preload='metadata'></video>")

        html_parts.append("<div class='pbar'>")
        html_parts.append("  <button class='pbtn' id='pbtn' onclick='togglePlay()'>")
        html_parts.append("    <svg id='psvg' viewBox='0 0 24 24'><polygon id='ico_play' points='5,3 19,12 5,21'/><rect id='ico_p1' x='6' y='4' width='4' height='16' style='display:none'/><rect id='ico_p2' x='14' y='4' width='4' height='16' style='display:none'/></svg>")
        html_parts.append("  </button>")
        html_parts.append("  <div class='pwrap' id='pw'>")
        html_parts.append("    <div class='ptrack'></div>")
        html_parts.append("    <div class='psel' id='ps'></div>")
        html_parts.append("    <div class='pfill' id='pf'></div>")
        html_parts.append("    <div class='pmark-s' id='pms'></div>")
        html_parts.append("    <div class='pmark-e' id='pme'></div>")
        html_parts.append("    <div class='ph' id='ph' style='left:0%'></div>")
        html_parts.append("  </div>")
        html_parts.append("  <div class='tdisp' id='td'>0:00 / " + dur_t_fmt + "</div>")
        html_parts.append("</div>")

        html_parts.append("<div class='sect'>")
        html_parts.append("  <div class='sect-top'>")
        html_parts.append("    <span class='clbl'>Sélection<span class='dur-chip' id='durChip'>0:00</span></span>")
        html_parts.append("    <span class='srange' id='srange'><em>0:00</em> → <em>" + dur_t_fmt + "</em></span>")
        html_parts.append("  </div>")
        html_parts.append("  <div class='cwrap' id='cw'>")
        html_parts.append("    <div class='ctrack'></div>")
        html_parts.append("    <div class='csel' id='cs'></div>")
        html_parts.append("    <div class='chandle' id='hs' style='left:0%'></div>")
        html_parts.append("    <div class='chandle' id='he' style='left:100%'></div>")
        html_parts.append("  </div>")
        html_parts.append("</div>")

        html_parts.append("<script>")
        html_parts.append("var vid=document.getElementById('vid'),dur=" + dur_t_str + ",tS=0,tE=dur,dr=null;")
        html_parts.append("function fT(s){var m=Math.floor(s/60),sc=Math.floor(s%60);return m+':'+(sc<10?'0':'')+sc;}")
        html_parts.append("function pct(t){return(t/dur*100).toFixed(4)+'%';}")
        html_parts.append("function updC(){")
        html_parts.append("  var hs=document.getElementById('hs'),he=document.getElementById('he');")
        html_parts.append("  hs.style.left=pct(tS); he.style.left=pct(tE);")
        html_parts.append("  document.getElementById('cs').style.left=pct(tS);")
        html_parts.append("  document.getElementById('cs').style.width=((tE-tS)/dur*100).toFixed(4)+'%';")
        html_parts.append("  document.getElementById('ps').style.left=pct(tS);")
        html_parts.append("  document.getElementById('ps').style.width=((tE-tS)/dur*100).toFixed(4)+'%';")
        html_parts.append("  document.getElementById('pms').style.left=pct(tS);")
        html_parts.append("  document.getElementById('pme').style.left=pct(tE);")
        html_parts.append("  document.getElementById('srange').innerHTML='<em>'+fT(tS)+'</em> → <em>'+fT(tE)+'</em>';")
        html_parts.append("  document.getElementById('durChip').textContent=fT(tE-tS);")
        html_parts.append("  updPlayheadFill();")
        html_parts.append("}")
        html_parts.append("function updPlayheadFill(){")
        html_parts.append("  var ct=vid.currentTime,ps=tS/dur*100,pc=Math.max(ps,Math.min(tE/dur*100,ct/dur*100));")
        html_parts.append("  document.getElementById('pf').style.left=ps.toFixed(4)+'%';")
        html_parts.append("  document.getElementById('pf').style.width=(pc-ps).toFixed(4)+'%';")
        html_parts.append("}")
        html_parts.append("vid.addEventListener('timeupdate',function(){")
        html_parts.append("  document.getElementById('ph').style.left=(vid.currentTime/dur*100).toFixed(4)+'%';")
        html_parts.append("  updPlayheadFill();")
        html_parts.append("  document.getElementById('td').textContent=fT(vid.currentTime)+' / '+fT(dur);")
        html_parts.append("  if(vid.currentTime>=tE){vid.pause();vid.currentTime=tE;}")
        html_parts.append("});")
        html_parts.append("function setPlayIcon(p){")
        html_parts.append("  document.getElementById('ico_play').style.display=p?'none':'block';")
        html_parts.append("  document.getElementById('ico_p1').style.display=p?'block':'none';")
        html_parts.append("  document.getElementById('ico_p2').style.display=p?'block':'none';")
        html_parts.append("}")
        html_parts.append("function togglePlay(){if(vid.paused){if(vid.currentTime<tS||vid.currentTime>=tE)vid.currentTime=tS;vid.play();}else{vid.pause();}}")
        html_parts.append("vid.addEventListener('pause',function(){setPlayIcon(false);});")
        html_parts.append("vid.addEventListener('play',function(){setPlayIcon(true);});")
        html_parts.append("function posE(e,el){var r=el.getBoundingClientRect(),x=(e.touches?e.touches[0].clientX:e.clientX)-r.left;return Math.max(0,Math.min(1,x/r.width))*dur;}")
        html_parts.append("document.getElementById('ph').addEventListener('mousedown',function(e){e.preventDefault();dr='head';});")
        html_parts.append("document.getElementById('ph').addEventListener('touchstart',function(){dr='head';},{passive:true});")
        html_parts.append("document.getElementById('pw').addEventListener('click',function(e){if(dr)return;var t=Math.max(tS,Math.min(tE,posE(e,this)));vid.currentTime=t;});")
        html_parts.append("document.getElementById('hs').addEventListener('mousedown',function(e){e.preventDefault();dr='s';this.classList.add('dragging');});")
        html_parts.append("document.getElementById('he').addEventListener('mousedown',function(e){e.preventDefault();dr='e';this.classList.add('dragging');});")
        html_parts.append("document.getElementById('hs').addEventListener('touchstart',function(){dr='s';this.classList.add('dragging');},{passive:true});")
        html_parts.append("document.getElementById('he').addEventListener('touchstart',function(){dr='e';this.classList.add('dragging');},{passive:true});")
        html_parts.append("document.addEventListener('mousemove',function(e){")
        html_parts.append("  if(!dr)return;")
        html_parts.append("  if(dr==='head'){var t=Math.max(tS,Math.min(tE,posE(e,document.getElementById('pw'))));vid.currentTime=t;}")
        html_parts.append("  else if(dr==='s'){tS=Math.min(posE(e,document.getElementById('cw')),tE-0.1);updC();}")
        html_parts.append("  else{tE=Math.max(posE(e,document.getElementById('cw')),tS+0.1);updC();}")
        html_parts.append("});")
        html_parts.append("document.addEventListener('touchmove',function(e){")
        html_parts.append("  if(!dr)return;")
        html_parts.append("  if(dr==='head'){var t=Math.max(tS,Math.min(tE,posE(e,document.getElementById('pw'))));vid.currentTime=t;}")
        html_parts.append("  else if(dr==='s'){tS=Math.min(posE(e,document.getElementById('cw')),tE-0.1);updC();}")
        html_parts.append("  else{tE=Math.max(posE(e,document.getElementById('cw')),tS+0.1);updC();}")
        html_parts.append("},{passive:true});")
        html_parts.append("document.addEventListener('mouseup',function(){")
        html_parts.append("  if(dr==='s')document.getElementById('hs').classList.remove('dragging');")
        html_parts.append("  if(dr==='e')document.getElementById('he').classList.remove('dragging');")
        html_parts.append("  dr=null;")
        html_parts.append("});")
        html_parts.append("document.addEventListener('touchend',function(){")
        html_parts.append("  document.getElementById('hs').classList.remove('dragging');")
        html_parts.append("  document.getElementById('he').classList.remove('dragging');")
        html_parts.append("  dr=null;")
        html_parts.append("});")
        html_parts.append("updC();")
        html_parts.append("</script></body></html>")

        components.html("".join(html_parts), height=430, scrolling=False)

        t_start = 0.0
        t_end = float(dur_t)

        if not st.session_state.trim_bytes:
            if st.button("Couper la vidéo", key="tbtn"):
                out_t = os.path.join(tmp_t, "video_coupee.mp4")
                ph_t = st.empty()
                ph_t.markdown('<div class="encoding-wrap"><div class="encoding-ring"></div><span class="encoding-text">Coupe en cours…</span></div><div class="fake-progress-wrap"><div class="fake-progress-track"><div class="fake-progress-bar"></div></div></div>', unsafe_allow_html=True)
                try:
                    trim_video(tp, out_t, t_start, t_end)
                    ph_t.empty()
                    with open(out_t, "rb") as f:
                        st.session_state.trim_bytes = f.read()
                    st.rerun()
                except Exception as e:
                    ph_t.markdown(f'<div class="status status-err">Erreur : {e}</div>', unsafe_allow_html=True)
        else:
            st.download_button("↓  Télécharger la vidéo", data=st.session_state.trim_bytes,
                file_name="video_coupee.mp4", mime="video/mp4", key="tdl")
    else:
        st.markdown('<div class="status status-idle">Déposez une vidéo via "Browse files".</div>', unsafe_allow_html=True)


st.markdown("""
<div class="site-footer">
  <span class="footer-name">© lucas bessonnat</span>
  <span>v1.0. Aucune donnée n'est conservée sur un serveur.</span>
</div>
""", unsafe_allow_html=True)
