import streamlit as st
import yt_dlp
import static_ffmpeg
import os
import tempfile

# This makes ffmpeg available to yt-dlp
static_ffmpeg.add_paths()

st.title("🎬 YouTube Downloader")

url = st.text_input("Paste YouTube URL here")
format_choice = st.radio("Format", ["MP4 Video", "MP3 Audio"])
cookies_file = st.file_uploader("Upload cookies.txt", type="txt")

if st.button("Download") and url:
    if not cookies_file:
        st.warning("Please upload your cookies.txt file first.")
    else:
        with st.spinner("Downloading..."):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    cookies_path = os.path.join(tmpdir, "cookies.txt")
                    with open(cookies_path, "wb") as f:
                        f.write(cookies_file.read())

                    if format_choice == "MP3 Audio":
                        ydl_opts = {
                            'format': 'besta

