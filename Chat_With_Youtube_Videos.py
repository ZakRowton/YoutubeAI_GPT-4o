from pytube import YouTube
from moviepy.editor import *
from openai import OpenAI

openai_key = 'OPENAI_API_KEY'
client = OpenAI(api_key=openai_key)

def trascribe_speech(filename, model = "whisper-1"):
    audio_file = open(filename, "rb")
    transcript = client.audio.transcriptions.create(
        model=model,
        file=audio_file
    )
    return transcript.text

def download_video(url, save_path='./'):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(output_path=save_path, filename='Youtube_Video_Output.mp4')
        return True
    except Exception as e:
        return False

def convert_to_mp3(filename):
    try:
        video = VideoFileClip(filename + ".mp4")
        video.audio.write_audiofile(filename + ".mp3")
        video.close()
        print("Video -> Audio Conversion Successful!")
        return True
    except Exception as e:
        print("Video -> Audio Conversion Failed!")
        return False

def prompt(transcription, question, model = "gpt-4o"):
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": ("TRANSCRIPTION: " + transcription + " PROMPT: " + question)}],
            stream=True,
        )
        if stream is None:
            print("An Error Occurred While Generating The Response!\nStream Was NULL!")
            return
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                cleaned_content = chunk.choices[0].delta.content.replace('\n', '')
                print(cleaned_content)
    except Exception as e:
        print("An Error Occurred While Generating The Response!")


def main():
    url = input("Enter the YouTube video URL: ")
    question = input("Enter Your Question: ")
    download_video(url)
    convert_to_mp3('testt')
    transcription = trascribe_speech('testt.mp3')
    prompt(transcription, question)

if __name__ == "__main__":
    main()
