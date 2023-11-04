import sys
import yt_dlp as ydl
import ffmpeg
import soundfile as sf
from scipy.interpolate import interp1d
import numpy as np
import os
import shutil

# Define ydl globally
ydl = ydl.YoutubeDL({
    'format': 'best',
    'outtmpl': '%(title)s.%(ext)s',  # Output template for the downloaded file
})

def download_youtube_video(video_id):
    # Download the video
    info_dict = ydl.extract_info(video_id, download=True)
    # Get the downloaded file name
    return ydl.prepare_filename(info_dict)

def slow_down_audio(input_path, output_path, slowdown_factor=0.8):
    # Load the WebM file using ffmpeg
    input_audio = ffmpeg.input(input_path)

    # Define the input file name for the extracted audio
    input_file = "input.wav"

    # Extract audio using ffmpeg
    audio_stream = input_audio['a:0']
    output_audio = ffmpeg.output(audio_stream, input_file, format='wav')
    ffmpeg.run(output_audio)

    # Load the input audio file
    data, samplerate = sf.read(input_file)

    # Calculate the new length of the audio after slowing down
    new_length = int(len(data) / slowdown_factor)

    # Create a function to interpolate the audio data
    interp_fn = interp1d(np.arange(len(data)), data.T, kind='linear', axis=1)

    # Calculate the new data points using interpolation
    slow_data = interp_fn(np.linspace(0, len(data) - 1, new_length)).T

    # Save the slowed down audio to the output file
    sf.write(output_path, slow_data, samplerate)

    # Convert the WAV output to MP3 using ffmpeg
    mp3_output_path = os.path.splitext(output_path)[0] + ".mp3"
    ffmpeg.input(output_path).output(mp3_output_path, codec='libmp3lame').run(overwrite_output=True)

    # Delete the input audio file
    os.remove(input_file)

if len(sys.argv) < 2:
    print('Usage: python slowed.py "<YouTube URL or video ID>" [slowdown_factor]')
    sys.exit(1)

video_identifier = sys.argv[1]

if len(sys.argv) > 2:
    slowdown_factor = float(sys.argv[2])
else:
    slowdown_factor = 0.8  # Default slowdown factor

# Download the YouTube video
downloaded_file = download_youtube_video(video_identifier)

# Create the output file paths
output_file = os.path.splitext(downloaded_file)[0] + "_slowed.wav"

# Slow down the audio and convert to MP3
slow_down_audio(downloaded_file, output_file, slowdown_factor)

# Delete the downloaded video file and the intermediate files
os.remove(downloaded_file)
os.remove(output_file)

# Move the finished MP3 file to the specified directory
output_directory = os.path.expanduser("~/Downloads/")
os.makedirs(output_directory, exist_ok=True)
mp3_output_file = os.path.splitext(downloaded_file)[0] + "_slowed.mp3"
shutil.move(mp3_output_file, os.path.join(output_directory, os.path.basename(mp3_output_file)))

print("Finished slowing down and converting to MP3. The file is in:", output_directory)