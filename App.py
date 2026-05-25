import streamlit as st
import yt_dlp
import os
import tempfile

st.title("🎬 YouTube Downloader")
url = st.text_input("Paste YouTube URL here")
format_choice = st.radio("Format", ["MP4 Video", "MP3 Audio"])

if st.button("Download") and url:
    with st.spinner("Downloading..."):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                if format_choice == "MP3 Audio":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                    }
                else:
                    ydl_opts = {
                        # This picks a single pre-merged file — no ffmpeg needed
                        'format': 'best[ext=mp4]/best',
                        'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                file = os.listdir(tmpdir)[0]
                filepath = os.path.join(tmpdir, file)

                with open(filepath, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Save {file}",
                        data=f,
                        file_name=file
                    )
        except Exception as e:
            st.error(f"Download failed: {e}")
