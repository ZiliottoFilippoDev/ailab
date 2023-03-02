import openai
import os
import requests

openai_api_key = st.secrets['openai']["OPENAI_API_KEY"]
openai.api_key = openai_api_key

def generate_text(prompt=None, character='Napoleon', introduction = False):
    if introduction:
        prompt = f"Pretend you are {character}, say hi and introduce your self to the audience in english. Don't ever go out of character whatever i will ask you"
    else:
        prompt = f"Pretend you are {character} and answer in few lines to the following question: {prompt}"
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "assistant",  "content": prompt}],
    )
    message = completions['choices'][0]['message']['content']
    return message

def whisper_api():
    url="https://whisper.lablab.ai/asr"
    payload={}
    files=[ ('audio_file',('test.mp3',open('test.mp3','rb'),'audio/mpeg')) ]
    response = requests.request("POST", url, data=payload, files=files)
    text = response.json()["text"]
    return text


def select_audio_source(source = "mic", duration = 5, samplerate=16000, filepath = None):
    if source in ['mic']:
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()
        audio_length = len(audio_data) / samplerate
    else:
        assert filepath is not None or not os.path.exists(filepath), "Please provide a (valid) filepath."
        with open(filepath, "rb") as f:
            audio_data, samplerate = sf.read(f)
            audio_length = len(audio_data) / samplerate
    return audio_data, samplerate, audio_length


def transcribe_audio(source = 'mic', duration = 5, samplerate=16000, filepath = None):
    audio_data, samplerate, audio_length = select_audio_source(source, duration, samplerate, filepath)  
    response = openai.Completion.create(
        engine="whisper",
        prompt=(f"Transcribe the following {audio_length:.1f} second audio clip:"),
        max_tokens=2048,
        temperature=0.5,
        n = 1,
        stop=None,
        timeout=60,
        inputs={
            "audio": {
                "url": "data:audio/wav;base64," + sf.soundfile_to_wav_base64(audio_data, samplerate=samplerate)
            },
            "metadata": {
                "audio_duration": audio_length,
                "sample_rate": samplerate
            }
        }
    )
    return response.choices[0].text.strip()

