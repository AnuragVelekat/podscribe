## 🎙️ PodScribe
PodScribe is a Flask-based app that summarizes podcasts from YouTube links with both text and audio output.

### 🛠️ Tech Stack
- Backend: Flask, Python

- Frontend: HTML, CSS, JavaScript

- Video Download: pytube

- Transcription: AssemblyAI API

- Summarization: Google Gemini API

- Text-to-Speech: pyttsx3

### ⚙️ How It Works
- User submits a YouTube link.

- Audio is extracted using pytube.

- Audio is transcribed via AssemblyAI.

- Transcript is summarized using Gemini.

- Summary is converted to speech with pyttsx3.

- App returns both the text and TTS audio summary.
