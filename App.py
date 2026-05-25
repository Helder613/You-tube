import streamlit as st
import yt_dlp
import os
import tempfile
 
st.title("YouTube Downloader")
 
url = st.text_input("Paste YouTube URL here")
format_choice = st.radio("Format", ["MP4 Video", "MP3 Audio"])
 
with st.expander("Having trouble? Upload cookies.txt"):
    st.caption("If you get a 403 error, export cookies from your browser using the 'Get cookies.txt LOCALLY' Chrome extension while logged into YouTube, then upload here.")
    cookies_file = st.file_uploader("cookies.txt (optional)", type="txt")
 
if st.button("Download") and url:
    with st.spinner("Downloading..."):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {
                    'outtmpl': tmpdir + '/%(title)s.%(ext)s',
                }
 
                if cookies_file:
                    cookies_path = os.path.join(tmpdir, "cookies.txt")
                    with open(cookies_path, "wb") as f:
                        f.write(cookies_file.read())
                    ydl_opts['cookiefile'] = cookies_path
 
                if format_choice == "MP3 Audio":
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'
 
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
 
                files = [f for f in os.listdir(tmpdir) if f != 'cookies.txt']
                file = files[0]
                filepath = os.path.join(tmpdir, file)
 
                with open(filepath, "rb") as f:
                    st.success("Done!")
                    st.download_button(
                        label="Save " + file,
                        data=f,
                        file_name=file
                    )
        except Exception as e:
            err = str(e)
            if "403" in err:
                st.error("YouTube blocked this server. Please upload your cookies.txt file (expand the section above).")
            else:
                st.error("Download failed: " + err)
 
