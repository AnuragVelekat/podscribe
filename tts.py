import pyttsx3

def save_audio():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    with open('output/output.txt', 'r') as f:
        text = f.read()
    f.close()
    engine.save_to_file(text, 'static/audio/output.wav')
    engine.runAndWait()
    print('audio saved')

if __name__ == '__main__':
    save_audio()