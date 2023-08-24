import streamlit as st
from config import GenerationArgsDefault, DreamViewerConfig
from DreamViewer import DreamViewer
from utils import set_seed

import os
import pyaudio
import wave

def record_audio(recording_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    
    st.warning("Recording audio...")
    for _ in range(0, int(RATE / CHUNK * recording_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    st.warning("Recording finished.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return b''.join(frames)

def main():
    # Initial page configurations
    st.set_page_config(page_title = "View you dreams!", page_icon = ":star:")
    if 'processing_done' not in st.session_state:
        st.session_state.processing_done = False

    # 
    st.title("DreamViewer 🦄")

    # File upload and recording
    st.header("Upload or Record Audio:")

    # Create a radio button to select the option
    option = st.radio("", ("Upload an audio file", "Record Audio"))

    # Track user actions
    audio_uploaded = False
    audio_recorded = False
    title_entered = False

    # Based on the selected option, render the appropriate section
    if option == "Upload an audio file":
        st.subheader("Upload an Audio File")
        audio_file = st.file_uploader("Choose an MP3 or WAV file", type=["mp3", "wav"])
        if audio_file is not None:
            st.audio(audio_file, format='audio/mp3')
            audio_uploaded = True
    elif option == "Record Audio":
        st.subheader("Record Audio")
        recording_time = st.slider("Select recording time (seconds)", 1, 30, 5)
        st.write("Press the 'Record Audio' button below:")
        record_audio_bt = st.button("Record Audio")
        if record_audio_bt:
            audio_file = record_audio(recording_time)
            st.audio(audio_file, format='audio/mp3') 
            audio_recorded = True

    # Story title
    st.subheader("Story Title")
    story_title = st.text_input("Enter Story Title")

    # Check if story title added
    if audio_uploaded or audio_recorded:
        if story_title:
            title_entered = True

    # Display the "Process data" button only if conditions are met

    if title_entered and (audio_uploaded or audio_recorded):
        if st.button("Process data"):
            with st.spinner("Processing..."):
                
                # Save the audio file
                os.makedirs(GenerationArgsDefault.AUDIO_DATA, exist_ok = True)
                audio_path = os.path.join(GenerationArgsDefault.AUDIO_DATA, story_title+".mp3")
                with open(audio_path, 'wb') as f:
                    f.write(audio_file.getbuffer())

                # Define arguments and set model configuration
                args = {'audio_file': audio_path, 'story_name': story_title}
                config = DreamViewerConfig(**{k:v for k,v in args.items()})
                set_seed(config.seed)

                # Create output directory if needed
                os.makedirs(config.output_dir, exist_ok=True)

                # Define DreamViewer model
                st.session_state.dv = DreamViewer(config)

                st.session_state.processing_done = True
    else:
        warning_message = "⚠️ Please complete the audio and story title options before processing data."
        st.markdown(f'<p style="color:white; background-color:rgba(255, 255, 0, 0.2); padding:10px; border-radius:5px;">{warning_message}</p>', unsafe_allow_html=True)

    # Generate the video
    if st.session_state.processing_done:
        if st.button("Generate Video"):
            with st.spinner("Generating video..."):
                st.session_state.dv.generate()
                video_path = os.path.join(config.output_dir, config.story_name + ".mp4")
                st.video(video_path)
                st.markdown(f'<a href="{video_path}" download>Click here to download the video</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()