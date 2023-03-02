import streamlit as st
import time
from io import BytesIO
import pyttsx3
from text import answers, characters
from multiprocessing import Process
import speech_recognition as sr
from functions import generate_text

def reproduce_voice(text, name):
    engine = pyttsx3.init()
    engine.setProperty('rate', 138)
    voices = engine.getProperty('voices') 
    if name in ['Queen Elizabeth I', 'Cleopatra']:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[2].id) 
    engine.say(text)
    engine.runAndWait()

def write_text(text,name, time_sleep=0.4, first_sleep = 5, speaker=True):
    time.sleep(first_sleep)
    t = st.empty()
    lst = text.split(" ")
    if speaker:
        color = "blue"
    else:
        color = "green"
    output_text = f"**:{color}[{name}]**: "
    for i in range(len(lst)):
        output_text += lst[i] + ' '
        t.markdown(output_text)
        time.sleep(time_sleep)

def on_click_name(text, name, time_sleep=0.4, answer = False):
    if not answer:
        gen_text = generate_text(None, name, introduction=True)
        audio_process = Process(target=reproduce_voice, args=(gen_text, name),)
        audio_process.start()
        write_text(gen_text, name)
        audio_process.join()
    else:
        gen_text = generate_text(text, name, introduction=False)
        audio_process = Process(target=reproduce_voice, args=(gen_text, name),)
        audio_process.start()
        write_text(gen_text, name)
        audio_process.join()


def main():
    st.set_page_config(page_title="Loqui",page_icon="📚",)
    st.title("Interactive Learning")
    st.markdown('**DISCLAIMER**: This is a super-early version where no character video is generated!!!\
                 Future version will have a proper UI. Stay tuned!')
    st.markdown('---')
    st.caption("Select a Historical character of your interest and ask him/her something.")
    global name

    cont1 = st.container()
    cont2 = st.container()
    cont3 = st.container()

    with cont1:
        cols = st.columns([1 for i in range(len(characters))]+ [2])
        stop = cols[-1].button("STOP", key="question")
        with cols[0]:
            b1 = st.button("Queen Elizabeth I")
            if b1:
                name = "Queen Elizabeth I"
        with cols[1]:
            b2 = st.button("Cleopatra")
            if b2:
                name = "Cleopatra"
        with cols[2]:
            b3 = st.button("Napoleon")
            if b3:
                name = "Napoleon"
        with cols[3]:
            b4 = st.button("Julius Caesar")
            if b4:
                name = "Julius Caesar"
        st.markdown('---')

    with cont2:
        try: 
            st.session_state.name = name
            on_click_name(None, st.session_state.name)
        except: pass
        
    for i in range(6):
        st.markdown('#')

    with cont3:
        try: 
            st.session_state.name = name 
        except: pass
        ask = st.button("Ask me something 🔊")
        r = sr.Recognizer()
        if ask:
            if st.session_state.name is None:
                st.error("Please select a character first!")
            else:
                with sr.Microphone() as source:
                    placeholder = st.empty()
                    with placeholder.container():
                        st.info("Speak now...", icon = "🎤")
                        audio = r.listen(source, phrase_time_limit=4)
                    placeholder.empty()   
                try:
                    text = r.recognize_google(audio)      
                    text += '?'
                except sr.UnknownValueError:
                    text = None
                    st.error("Sorry, I didn't understand what you said.")
                if text is not None:
                    gen_text = generate_text(text,st.session_state.name)
                    write_text(text,name='You', time_sleep=0.3, first_sleep=0.1, speaker=False)                  
                    on_click_name(gen_text, st.session_state.name, answer=True, time_sleep=0.2)

if __name__ == "__main__":
    main()






