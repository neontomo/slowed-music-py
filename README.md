# slowed music generator

I love listening to my favourite songs slowed down a bit, it adds some emotion and can give new life to music that I've played way too many times. there are websites that automate this process, but none of them allow me to download the music from youtube.

this script helps me by doing both tasks - downloading and slowing down music.

## screenshot
<img width="973" alt="image" src="https://github.com/neontomo/slowed-music-py/assets/105588693/62c198df-8f86-4b43-8fcf-f521d28d00af">

## what I learned
I needed to iterate many times to find the right libraries that slows down music without making it choppy, and some libraries slow music down without changing the pitch, resulting in a bizarre output. the final solution was trial and error, which is what coding often looks like, and I got more experience using python to solve a problem that I had! :-)

## requirements
- python3
  
## python imports

- yt_dlp
- ffmpeg
- soundfile
- interp1d
- numpy
- shutil
- os
