import streamlit as st
import yt_dlp
import os
import tempfile
 
st.title("YouTube Downloader")
 
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
                            'format': 'bestaudio/best',
                            'outtmpl': tmpdir + '/%(title)s.%(ext)s',
                            'cookiefile': cookies_path,
                            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                        }
                    else:
                        ydl_opts = {
                            'format': 'bestvideo+bestaudio/best',
                            'outtmpl': tmpdir + '/%(title)s.%(ext)s',
                            'cookiefile': cookies_path,
                            'merge_output_format': 'mp4',
                        }
 
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
 
                    files = [f for f in os.listdir(tmpdir) if f != 'cookies.txt']
                    file = files[0]
                    filepath = os.path.join(tmpdir, file)
 
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="Save " + file,
                            data=f,
                            file_name=file
                        )
            except Exception as e:
                st.error("Download failed: " + str(e))
