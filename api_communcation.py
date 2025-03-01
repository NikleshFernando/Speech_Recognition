import time
import requests
from api_secret import API_KEY_ASSEMBLYAI


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization':API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename,chunk_size= 5242880):
        with open(filename,'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url = upload_response.json().get('upload_url')

    return audio_url

#transcribe

def trancribe(audio_url):
    transcript_request = {"audio_url":audio_url}
    transcript_response = requests.post(transcript_endpoint,json=transcript_request,headers=headers)
    job_id = transcript_response.json()['id']
    return job_id

#Polling

def poll(transcribe_id):
    polling_endpoint = transcript_endpoint + '/' + transcribe_id
    polling_response= requests.get(polling_endpoint,headers=headers)
    return polling_response.json()

def get_transciption_results_url(audio_url):
    transcript_id = trancribe(audio_url)
    while True:
        data = poll(transcribe_id=transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data,data['error']
        
        print("Waiting 30 Seconds........")
        time.sleep(30)
    

#Save transcript
def save_transcript(audio_url,filename):
    data,error = get_transciption_results_url(audio_url)

    if data:
        text_filename = filename + ".txt"
        with open(text_filename,"w") as f:
            f.write(data['text'])

        print("Transcription Saved!!!")
    elif error:
        print("Error",error)