import os
import streamlit as st
import numpy as np
import pandas as pd
from glob import glob
from datetime import datetime, date, timedelta

from functools import cmp_to_key

# Set settings for app
st.set_page_config(layout="wide")

# Title
st.title("Text-to-Speech Analysis")

# Audio directories
audio_dirs = glob("mohs_study/*")
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
# confidence = st.checkbox("Display confidence?")

# Find files in directory
audio_dir = glob(f"mohs_study/{option}/{source.lower()}/*")

# Custom compare 
def compare(s1, s2):
    base1 = os.path.basename(s1)
    base1 = os.path.splitext(base1)[0]

    base2 = os.path.basename(s2)
    base2 = os.path.splitext(base2)[0]

    num1 = base1.split("_")
    num1 = num1[len(num1)-1]

    num2 = base2.split("_")
    num2 = num2[len(num2)-1]

    return int(num1) - int(num2)


# Display side-by-side 
col1, col2, col3 = st.beta_columns(3)
with col1:
    if comparison == "Audio sources":
        # Compare audio sources
        col1.header("Computer Transcription")

        # Find files in directory
        audio_dir = glob(f"mohs_study/{option}/{source.lower()}/computer/*")
        transcriptions = sorted(audio_dir, key=cmp_to_key(compare))
        
        writing = ""
        index = 0
        for transcription in transcriptions:
            with open(transcription) as f:
                writing += f"{index}: {f.read()} \n\n"
            index += 1
        st.write(writing)

    else:
        # Compare transcription sources
        col1.header("Amazon")

        # Find files in directory
        audio_dir = glob(f"mohs_study/{option}/amazon/{source.lower()}/*")
        transcriptions = sorted(audio_dir, key=cmp_to_key(compare))
        
        writing = ""
        index = 0
        for transcription in transcriptions:
            with open(transcription) as f:
                writing += f"{index}: {f.read()} \n\n"
            index += 1
        st.write(writing)

with col2:
    if comparison == "Audio sources":
        # Compare audio sources
        col2.header("Watch Transcription")
        
        # Find files in directory
        audio_dir = glob(f"mohs_study/{option}/{source.lower()}/watch/*")
        transcriptions = sorted(audio_dir, key=cmp_to_key(compare))
        
        writing = ""
        index = 0
        for transcription in transcriptions:
            with open(transcription) as f:
                writing += f"{index}: {f.read()} \n\n"
            index += 1
        st.write(writing)

    else:
        # Compare transcription sources
        col2.header("Google")

        # Find files in directory
        audio_dir = glob(f"mohs_study/{option}/google/{source.lower()}/*")
        transcriptions = sorted(audio_dir, key=cmp_to_key(compare))
        
        writing = ""
        index = 0
        for transcription in transcriptions:
            with open(transcription) as f:
                writing += f"{index}: {f.read()} \n\n"
            index += 1
        st.write(writing)

with col3: # Testing column to provide the ground truth speech data from the computer.
    col3.header("Ground Truth")

    # Find files in directory
    audio_dir = glob(f"mohs_study/{option}/logfiles/*.csv")
    transcriptions = pd.read_csv(audio_dir[0]) 

    writing = ""
    index = 0
    start = 3
    while start < (len(transcriptions.index)-1):
        step = transcriptions.iloc[start][2]
        if step[2] == ':':
            st.write(f"{index}: {step[3:]} \n\n")
        elif step[3] == ':':
            st.write(f"{index}: {step[4:]} \n\n")
        elif step[4] == ':':
            st.write(f"{index}: {step[5:]} \n\n")
        elif step[5] == ':':
            st.write(f"{index}: {step[6:]} \n\n")
        else:
            st.write(f"{index}: {step} \n\n")
        start += 1
        index += 1



# Display computer audio
# audio_dir = glob(f"mohs_study/{option}/*")
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