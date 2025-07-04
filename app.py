from flask import Flask, render_template, request, jsonify
from pytubefix import YouTube
import os
import assemblyai as aai
from datetime import datetime
import re
import google.generativeai as genai
from dotenv import load_dotenv
from tts import save_audio

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AAI_API_KEY = os.getenv("AAI_API_KEY")

app = Flask(__name__)


genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/', methods=['GET'])
def home():
        
    return render_template('index.html')

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    link = request.get_json()['link']
    transcription = get_transcription(link)
    title = yt_title(link)
    summary = generate_summary_from_transcription(transcription, title)
    save_audio()
    return jsonify({'content': summary})

def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='media/')
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    # title = yt_title(link)
    aai.settings.api_key = AAI_API_KEY
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    os.remove(audio_file)

    return transcript.text

def generate_summary_from_transcription(transcription, title):

    summary_example = '''Title: The Rise of Electric Vehicles: Shaping a Greener Future

Introduction:
The automotive industry is undergoing a profound transformation as electric vehicles (EVs) surge in popularity. With advancements in technology and growing environmental concerns, EVs are revolutionizing transportation worldwide.

The Shift Towards Electric Mobility:
Traditional vehicles powered by internal combustion engines contribute significantly to air pollution and climate change. In response, governments and automotive manufacturers are increasingly investing in electric mobility. Countries are setting ambitious targets to phase out petrol and diesel vehicles in favor of EVs, promoting sustainable transportation alternatives.

Technological Advancements:
Advancements in battery technology are driving the widespread adoption of EVs. Lithium-ion batteries, with their improved energy density and declining costs, are making electric vehicles more affordable and practical for consumers. Additionally, innovations in charging infrastructure are addressing concerns about range anxiety, making EVs a viable option for long-distance travel.

Environmental Impact:
The transition to electric mobility is crucial for reducing greenhouse gas emissions and combating climate change. EVs produce zero tailpipe emissions, reducing air pollution in urban areas and improving public health. Furthermore, renewable energy sources like solar and wind power can power EVs, further reducing their environmental footprint.

Economic Opportunities:
The shift towards electric vehicles presents significant economic opportunities. It fosters job creation in manufacturing, research, and infrastructure development. Moreover, it reduces dependence on imported oil, enhancing energy security and promoting economic resilience.

Challenges and Solutions:
Despite their benefits, electric vehicles face challenges such as limited charging infrastructure, higher upfront costs, and concerns about battery recycling. However, governments, businesses, and researchers are collaborating to address these challenges through investments in charging networks, incentives for consumers, and advancements in battery recycling technologies.

Conclusion:
Electric vehicles are poised to transform the automotive industry and play a vital role in mitigating climate change. With continued innovation and collaboration, EVs have the potential to create a greener, more sustainable future for generations to come. Embracing electric mobility is not just a choice; it's a necessity in our journey towards a cleaner and healthier planet.
'''

    prompt = f"Based on the following transcript from a podcast, write a comprehensive summary blog post in about 500-700 words, write it based on the transcript and make it look like a proper summary. Also try to identify and mention the speakers in the podcast in the beginning of the summary and add a final conclusion paragraph at the end. If you are unable to find the speakers, then don't mention them. Also add a title to the summary. Use the following example format given to structure the summary blog post. \n\nExample Format: {summary_example}\n\ntitle: {title}\ntranscript: {transcription}\n\nSummary Blog Post:"

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(prompt)

    generated_content = response.text

    formatted_output = format_output(generated_content)

    with open('output/output.txt', 'w') as f:
        f.write(formatted_output.replace('<br>', ' '))
    f.close()
    return formatted_output


def format_output(html_content):
    replaced_content = html_content.replace('\n', '<br>\n')
    replaced_content= replaced_content.replace('*', '')
    replaced_content= replaced_content.replace('#', '')
    return replaced_content


if __name__ == '__main__':
    app.run(debug=True, port=8080)

# data['tasks']['taskResult']['results']['documents'][0]['summaries'][0]['text']