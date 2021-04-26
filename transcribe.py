from google.cloud import speech
from glob import glob
import urllib.request
import io
import os
import os.path
import json
import time
import boto3


def amazon_speech(url):
    """Transcribe audio using Amazon Speech-To-Text"""

    transcribe = boto3.client('transcribe')
    job_name = os.path.basename(url)
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
    
    parse_amazon(status['TranscriptionJob']['Transcript']['TranscriptFileUri'], url)


def parse_amazon(aws_url, filepath):
    """Parse Amazon transcription"""

    transcription = ""
    with urllib.request.urlopen(aws_url) as url:
        data = json.loads(url.read().decode())
        transcription = data['results']['transcripts'][0]['transcript']
        """
        items = data['results']['items']
        for item in items:
            transcript = item['alternatives'][0]['content']
            confidence = round(float(item['alternatives'][0]['confidence']), 2)

            transcription += f"{transcript} "
        """

    # write transcription to file
    basename = os.path.basename(filepath)
    basename = os.path.splitext(basename)[0]
    path = os.path.dirname(filepath)
    filename = f"{path}/amazon/{basename}_amazon_conf.txt"
    with open(filename, "w+") as f:
        f.write(transcription)


def google_speech(url):
    """Transcribe audio using Google Speech-To-Text"""

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
    print(response)
    transcription = ""
    for index, result in enumerate(response.results):
        transcript = result.alternatives[0].transcript
        confidence = round(float(result.alternatives[0].confidence), 2)

        transcription += f"{transcript} ({confidence}) "
    
    # write transcription to file
    filename = f"{os.path.splitext(url)[0]}_google_conf.txt"
    with open(filename, "w+") as f:
        f.write(transcription)


def transcribe():
    """Script to trascribe Smash audio files"""

    audio_dirs = glob("smashlab/*")
    for audio_dir in audio_dirs:
        audio_files = glob(f"{audio_dir}/*")
        for audio_file in audio_files:
            if audio_file.endswith(".wav"):
                basename = os.path.basename(audio_file)
                basename = os.path.splitext(basename)[0]
                path = os.path.dirname(audio_file)
                filename = f"{path}/amazon/{basename}_amazon_conf.txt"                
                if not os.path.isfile(filename):
                    # amazon_speech(audio_file)
                    pass
