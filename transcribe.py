from google.cloud import speech
from pydub import AudioSegment
from datetime import datetime
from glob import glob
import pandas as pd
import urllib.request
import io
import os
import os.path
import json
import time
import boto3
import shutil


def amazon_speech(audio_dir, url):
    """Transcribe audio using Amazon Speech-To-Text"""

    audio = AudioSegment.from_wav(url)
    duration = audio.duration_seconds
    if duration == 0:
        return

    transcribe = boto3.client('transcribe')
    job_name = f"v8_{os.path.basename(url)}"
    job_uri = f"s3://{url}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    parse_amazon(status['TranscriptionJob']['Transcript']['TranscriptFileUri'], audio_dir, url)


def parse_amazon(aws_url, audio_dir, filepath):
    """Parse Amazon transcription"""

    transcription = ""
    with urllib.request.urlopen(aws_url) as url:
        data = json.loads(url.read().decode())
        transcription = data['results']['transcripts'][0]['transcript']
        items = data['results']['items']
        for item in items:
            transcript = item['alternatives'][0]['content']
            confidence = round(float(item['alternatives'][0]['confidence']), 2)

            transcription += f"{transcript} "

    # write transcription to file
    source = "computer" if "computer" in filepath else "watch"
    basename = os.path.basename(filepath)
    basename = os.path.splitext(basename)[0]
    num = basename.split("_")
    num = num[len(num)-1]
    filename = f"{audio_dir}/amazon/{source}/{basename}_amazon_{num}.txt"
    with open(filename, "w+") as f:
        f.write(transcription)


def google_speech(audio_dir, url):
    """Transcribe audio using Google Speech-To-Text"""

    try:
        audio = AudioSegment.from_wav(url)
        duration = audio.duration_seconds
        if duration == 0:
            return

        gcs_uri = f"gs://{url}"
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)

        audio_channel_count = 2 if "watch" in url else 1
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
            audio_channel_count=audio_channel_count,
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=90)

        # iterate through transcription result
        transcription = ""
        for index, result in enumerate(response.results):
            transcript = result.alternatives[0].transcript
            confidence = round(float(result.alternatives[0].confidence), 2)

            transcription += f"{transcript} "
        
        # write transcription to file
        source = "computer" if "computer" in url else "watch"
        basename = os.path.basename(url)
        basename = os.path.splitext(basename)[0]
        num = basename.split("_")
        num = num[len(num)-1]
        filename = f"{audio_dir}/google/{source}/{basename}_google_{num}.txt"
        with open(filename, "w+") as f:
            f.write(transcription)
    
    except:
        pass

def timestring_to_seconds(s):
    h, m, s = [int(i) for i in s.split(':')]
    return 3600*h + 60*m + s


def split_audio(path, audio_file, logfile):
    """Split audio files based on the logfile"""
    
    # Parse logfile
    log = pd.read_csv(logfile)
    rel_time = log['Relative Time'][2:].tolist()
    rel_time.pop(1)
    for i in range(0, len(rel_time) - 1):
        t1 = timestring_to_seconds(rel_time[i])
        t2 = timestring_to_seconds(rel_time[i+1])

        t1 = t1 * 1000
        t2 = t2 * 1000
        audio = AudioSegment.from_wav(audio_file)
        sliced = audio[t1:t2]
        source = "computer" if "computer" in audio_file else "watch"
        basename = os.path.basename(audio_file)
        basename = os.path.splitext(basename)[0]
        sliced.export(f"{path}/parts/{source}/{basename}_{i}.wav", format="wav")


def transcribe():
    """Script to trascribe Smash audio files"""

    """
    audio_dirs = glob("../smashlab/*")
    for audio_dir in audio_dirs:
        audio_files = glob(f"{audio_dir}/*.wav")
        logfile = glob(f"{audio_dir}/logfiles/*.csv")
        for audio_file in audio_files:
            if audio_file.endswith(".wav"):
                if len(logfile) > 0:
                    split_audio(audio_dir, audio_file, logfile[0])
                # basename = os.path.basename(audio_file)
                # basename = os.path.splitext(basename)[0]
                # path = os.path.dirname(audio_file)
                # filename = f"{path}/amazon/{basename}_amazon_conf.txt"                
                # if not os.path.isfile(filename):
                # pass
                # amazon_speech(audio_file)
    """

    audio_dirs = glob("smashlab/*")
    for audio_dir in audio_dirs:
        comp_files = glob(f"{audio_dir}/parts/computer/*")
        watch_files = glob(f"{audio_dir}/parts/watch/*")

        # computer files
        for audio_file in comp_files:
            if "r06_32_manual" not in audio_file:
                if audio_file.endswith(".wav"):
                    pass
                    # amazon_speech(audio_dir, audio_file)

        # watch files
        for audio_file in watch_files:
            if audio_file.endswith(".wav"):
                if "r06_32_manual" not in audio_file:
                    amazon_speech(audio_dir, audio_file)

        # basename = os.path.basename(audio_file)
        # basename = os.path.splitext(basename)[0]
        # path = os.path.dirname(audio_file)
        # num = basename.split("_")
        # num = num[len(num)-1]
        # filename = f"{path}/amazon/{basename}_amazon_{num}.txt"
        # if not os.path.isfile(filename):
        # pass

transcribe()