from moviepy import VideoFileClip
import os

def mp4_to_gif(folder, fps=30):
    for file in os.listdir(folder):
        filename, extension = file.split('.')
        if extension != 'mp4': continue

        clip = VideoFileClip(os.path.join(folder, file))
        clip.write_gif(os.path.join(folder, f'{filename}.gif'), fps=fps)

