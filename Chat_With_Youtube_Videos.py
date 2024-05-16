#### Imported Libraries21 
from pytube import YouTube
from moviepy.editor import *
from openai import OpenAI


#### Variables
openai_key = 'OPENAI_API_KEY'
client = OpenAI(api_key=openai_key)
verbos_logging = True
video_file_name = 'Youtube_Video_Output'
audio_file_name = 'Youtube_Audio_Output'
default_speech_model = "whisper-1"
default_chat_model = "gpt-4o"


#### Transcribe Speech From MP3 File
def trascribe_speech(filename, model = default_speech_model):
    try:
        audio_file = open(filename, "rb")
        transcript = client.audio.transcriptions.create(
            model=model,
            file=audio_file
        )

        if (verbos_logging):
            print("Transcription: ", transcript.text)

        return transcript.text
    except Exception as e:
        print("An Error Occurred While Transcribing The Audio File!")
        return None


#### Download YouTube Video From URL
def download_video(url, filename, save_path='./'):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video.download(output_path=save_path, filename=filename)
        if (verbos_logging):
            print("Video Downloaded Successfully! FileName: " + filename + ".mp4")
        return True
    except Exception as e:
        return False


#### Convert MP4 to MP3
def convert_to_mp3(filename):
    try:
        video = VideoFileClip(filename + ".mp4")
        video.audio.write_audiofile(filename + ".mp3")
        if (verbos_logging):
            print("Audio File Created Successfully! FileName: " + filename + ".mp3")
        video.close()
        if (verbos_logging):
            print("Video -> Audio Conversion Successful!")
        return True
    except Exception as e:
        print("ERROR: Video -> Audio Conversion Failed!")
        return False


#### Chat Completion Function
def prompt(question, transcription = "", model = default_chat_model):
    try:
        arsval = []
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": ("TRANSCRIPTION: " + transcription + " PROMPT: " + question)}],
            stream=True,
        )

        if stream is None:
            print("ERROR: An Error Occurred While Generating The Response!\nStream Was NULL!")
            return None
        
        if (verbos_logging):
            print("Response: \n")

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                if (verbos_logging):
                    print(chunk.choices[0].delta.content);
                arsval.append(chunk.choices[0].delta.content)
    except Exception as e:
        print("An Error Occurred While Generating The Response!")


#### Main Function
def main():
    try:
        url = input("Enter the YouTube video URL: ")
        question = input("Enter Your Question: ")
        download_video(url, (video_file_name + '.mp4'))
        convert_to_mp3(video_file_name)
        transcription = trascribe_speech(audio_file_name + '.mp3')
        prompt(question, transcription)

        if (verbos_logging):
            print("Operation Completed Successfully!")
    except Exception as e:
        print("ERROR: Operation Failed!")


#### Main Function Call
if __name__ == "__main__":
    main()
