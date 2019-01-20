from PIL import ImageStat, Image
from PIL import ImageEnhance
import numpy as np
import cv2

def merge_windows(windows):
    ret = windows[0]
    
    for i in range(1, len(windows)):
        ret = np.append(ret, windows[i][9])
    print(ret)
    return ret

def enhance_video(real_brightness, predicted_brightness, anomaly_frame_chunk_ids, vid_frames, win_size):
    #convert chunk ids into their frames
    frames_to_edit = []
    
    for i in range(len(anomaly_frame_chunk_ids)-1):
        if(anomaly_frame_chunk_ids[i+1]-anomaly_frame_chunk_ids[i] < win_size):
            for j in range(anomaly_frame_chunk_ids[i+1]-anomaly_frame_chunk_ids[i]):
                frames_to_edit.append(anomaly_frame_chunk_ids[i]+j)
        else:
            for j in range(win_size):
                frames_to_edit.append(anomaly_frame_chunk_ids[i] + j)
    for i in range(win_size):
        frames_to_edit.append(anomaly_frame_chunk_ids[len(anomaly_frame_chunk_ids)-1] + i)
    
    real_brightness = merge_windows(real_brightness)
    predicted_brightness = merge_windows(predicted_brightness)
    
    for frame_num in frames_to_edit:
        factor = .5
        frame = Image.fromarray(cv2.cvtColor(vid_frames[frame_num], cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Brightness(frame)
        enhanced_frame = enhancer.enhance(factor)
        vid_frames[frame_num] = enhanced_frame
        
        
    return vid_frames

def make_video(frames, outimg=None, fps=24, size=None,
               is_color=True, format="MP4V"):

    fourcc = cv2.VideoWriter_fourcc(*format)
    vid = None
    for frame in frames:
        if vid is None:
            if size is None:
                size = frame.shape[1], frame.shape[0]
            vid = cv2.VideoWriter('safe.mp4', fourcc, float(fps), size, is_color)
        if size[0] != frame.shape[1] and size[1] != frame.shape[0]:
            frame = cv2.resize(frame, size)
        vid.write(frame)
    vid.release()
    return vid