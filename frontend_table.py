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

if comparison == "Audio sources":
    #declare the dictionary that will be converted to a pandas dataframe
    dict = {"Computer Transcription": [], "Watch Transcription": [], "Ground Truth": []}

    #Computer Transcription first
    audio_dir = glob(f"mohs_study/{option}/{source.lower()}/computer/*")
    transcriptions = sorted(audio_dir, key=cmp_to_key(compare))

    writing = ""
    for transcription in transcriptions:
        with open(transcription) as f:
            writing = f"{f.read()}"
        dict["Computer Transcription"].append(writing)


    #Watch Transcription next
    audio_dir = glob(f"mohs_study/{option}/{source.lower()}/watch/*")
    transcriptions = sorted(audio_dir, key=cmp_to_key(compare))

    writing = ""
    for transcription in transcriptions:
        with open(transcription) as f:
            writing = f"{f.read()}"
        dict["Watch Transcription"].append(writing)

    #Ground Truth
    audio_dir = glob(f"mohs_study/{option}/logfiles/*.csv")
    transcriptions = pd.read_csv(audio_dir[0]) 

    writing = ""
    start = 3
    while start < (len(transcriptions.index)-1):
        step = transcriptions.iloc[start][2]
        if step[2] == ':':
            writing = (f"{step[3:]}")
        elif step[3] == ':':
            writing = (f"{step[4:]}")
        elif step[4] == ':':
            writing = (f"{step[5:]}")
        elif step[5] == ':':
            writing = (f"{step[6:]}")
        else:
            writing = (f"{step}")

        dict["Ground Truth"].append(writing)
        start += 1
    #dataframe setup and table creation
    table = pd.DataFrame.from_dict(dict, orient='index')
    st.table(table.transpose())
else:
    #declare the dictionary that will be converted to a pandas dataframe
    dict = {"Amazon": [], "Google": [], "Ground Truth": []}

    #Amazon first
    audio_dir = glob(f"mohs_study/{option}/amazon/{source.lower()}/*")
    transcriptions = sorted(audio_dir, key=cmp_to_key(compare))

    writing = ""
    for transcription in transcriptions:
        with open(transcription) as f:
            writing = f"{f.read()}"
        dict["Amazon"].append(writing)


    #Google next
    audio_dir = glob(f"mohs_study/{option}/google/{source.lower()}/*")
    transcriptions = sorted(audio_dir, key=cmp_to_key(compare))

    writing = ""
    for transcription in transcriptions:
        with open(transcription) as f:
            writing = f"{f.read()}"
        dict["Google"].append(writing)

    #Ground Truth
    audio_dir = glob(f"mohs_study/{option}/logfiles/*.csv")
    transcriptions = pd.read_csv(audio_dir[0]) 

    writing = ""
    start = 3
    while start < (len(transcriptions.index)-1):
        step = transcriptions.iloc[start][2]
        if step[2] == ':':
            writing = (f"{step[3:]}")
        elif step[3] == ':':
            writing = (f"{step[4:]}")
        elif step[4] == ':':
            writing = (f"{step[5:]}")
        elif step[5] == ':':
            writing = (f"{step[6:]}")
        else:
            writing = (f"{step}")

        dict["Ground Truth"].append(writing)
        start += 1
    #dataframe setup and table creation
    table = pd.DataFrame.from_dict(dict, orient='index')
    st.table(table.transpose())

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