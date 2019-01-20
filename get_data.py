import math
from PIL import ImageStat, Image
import pafy
import youtube_dl
import cv2
import numpy as np

def brightness(frame):
    frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    stat = ImageStat.Stat(frame)
    r,g,b = stat.mean
    return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def stream_data1(url):
    vPafy = pafy.new(url)
    play = vPafy.getbest(preftype="webm")

    #start the video
    cap = cv2.VideoCapture(play.url)
    frames = []
    brightness_vals = [] #avg brightness for each frame

    while (True):
        ret,frame = cap.read()
        if type(frame) == type(None):
            break
        frames.append(frame)
        brightness_vals.append(brightness(frame))
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break    

    cap.release()
    return brightness_vals, frames;

def stream_data2(url):
    vPafy = pafy.new(url)
    play = vPafy.getbest(preftype="webm")

    #start the video
    cap = cv2.VideoCapture(play.url)
    brightness_vals = [] #avg brightness for each frame

    while (True):
        ret,frame = cap.read()
        if type(frame) == type(None):
            break
        brightness_vals.append(brightness(frame))
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break    

    cap.release()
    return brightness_vals