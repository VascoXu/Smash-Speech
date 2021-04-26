import os
import streamlit as st
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime, date, timedelta


# Set settings for app
st.set_page_config(layout="wide")

# Title
st.title("Text-to-Speech Analysis")

# Audio directories
audio_dirs = glob("smashlab/*")
dirs = [os.path.basename(audio_dir) for audio_dir in audio_dirs]

# Dropdowns
option = st.selectbox(
    'Select a file',
    dirs
)

comparison = st.selectbox(
    'Compare',
    ('Audio sources', 'Transcription sources')
)

if comparison == "Audio sources":
    source = st.selectbox(
        'Select a source',
        ("Google", "Amazon")
    )
else:
    source = st.selectbox(
        'Select a source',
        ("Computer", "Watch")
    )   

# Confidence checkbox
confidence = st.checkbox("Display confidence?")

# Find files in directory
audio_dir = glob(f"smashlab/{option}/{source.lower()}/*")

# Display side-by-side 
col1, col2 = st.beta_columns(2)
with col1:
    if comparison == "Audio sources":
        # Compare audio sources
        col1.header("Computer Transcription")
        comp_file = [files for files in audio_dir if "computer" in files and files.endswith(".txt")]
        
        # Check confidence
        if confidence and source != "Amazon":
            comp_file = [files for files in comp_file if "conf" in files]
        else:
            comp_file = [files for files in comp_file if "conf" not in files]
        
        comp_file = comp_file[0]

        with open(comp_file, "r") as f:
            st.write(f.read())
    else:
        # Compare transcription sources
        col1.header("Amazon")

        # Find files in directory
        audio_dir = glob(f"smashlab/{option}/amazon/*")

        comp_file = [files for files in audio_dir if "amazon" in files and source.lower() in files and files.endswith(".txt")][0]

        with open(comp_file, "r") as f:
            st.write(f.read())

with col2:
    if comparison == "Audio sources":
        # Compare audio sources
        col2.header("Watch Transcription")
        watch_file = [files for files in audio_dir if "watch" in files and files.endswith(".txt")]

        # Check confidence
        if confidence and source != "Amazon":
            watch_file = [files for files in watch_file if "conf" in files]
        else:
            watch_file = [files for files in watch_file if "conf" not in files]

        watch_file = watch_file[0]

        with open(watch_file, "r") as f:
            st.write(f.read())
    else:
        # Compare transcription sources
        col2.header("Google")

        # Find files in directory
        audio_dir = glob(f"smashlab/{option}/google/*")

        comp_file = [files for files in audio_dir if "google" in files and source.lower() in files and files.endswith(".txt")]

        # Check confidence
        if confidence:
            comp_file = [files for files in comp_file if "conf" in files]
        else:
            comp_file = [files for files in comp_file if "conf" not in files]

        comp_file = comp_file[0]

        with open(comp_file, "r") as f:
            st.write(f.read())

# Display computer audio
# audio_dir = glob(f"smashlab/{option}/*")
# audio_col1, audio_col2 = st.beta_columns(2)
# with audio_col1:
#     audio_col1.header("Computer Audio")
#     audio_files = [files for files in audio_dir if "computer" in files and files.endswith(".wav")][0]
#     audio_file = open(audio_files, 'rb')
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format='audio/wav')

# with audio_col2:
#     audio_col2.header("Watch Audio")
#     audio_files = [files for files in audio_dir if "watch" in files and files.endswith(".wav")][0]
#     audio_file = open(audio_files, 'rb')
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format='audio/wav')