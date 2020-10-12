# -*- coding: utf-8 -*-
"""
Version - 1.0 (Binary Tagging) | Date: 24-02-2020
"""
# import libraries
import os
import sys
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop
import pandas as pd
#from datetime import datetime
import time
#import numpy as np

# class Video(object):
#     def __init__(self,path):
#         self.path = path

#     def play(self):
#         from os import startfile
#         startfile(self.path)

# class Movie_MP4(Video):
#     type = "MP4"

# # Get data inputs for reporting
# if (len(sys.argv) == 4):
#     video = sys.argv[1]
#     length_min = sys.argv[2]
#     length_sec = sys.argv[3]
# else:
#     print ("Usage: python video_tagging.py video.mp4(or any other video extenstion) length(mins) length(secs)")
#     print ("Example: python video_tagging.py nets_22_feb_2020_1.mov 34 26")
#     exit (1)

# print("Description - Video tagging - get user tags to generate action-wise sample clips")
# print("Version - 1.0 (Binary Tagging)")
# print("Date - 24-02-2020")
# print("Output - Binary-classified videos clipped and stored in individual folder")

video='2016-0101-000018-005-gaxehhze_PQ0dy2rI.mpeg'
myclip = VideoFileClip(video)
action1 = input("Provide class name for primary class: ")
action2 = input("Provide class name for secondary class: ")
format_list = [action1,action2]

# detect the current working directory and print it
path = os.getcwd()
print ("The current working directory is %s" % path)

print(2*int(myclip.fps))
# folders = [action1, action2]

# for folder in folders:
    
#     os.makedirs(os.path.join(path, folder),exist_ok=True)

# print("Subfolders successfully created, let's start tagging!")

redo = 0
clip_prefix = "clip_"
subfolder_fix = "/"
clip_ext = ".mp4"
count = 1

length_m = int(input('length(mins)'))
length_s = int(input('length(secs)'))
t_last = length_m * 60 + length_s
#t_last = int(length)
i = 0
#batsman_list = []
#bowler_list = []
#foot_list = []
#risk_list = []
#direction_list = []
#line_list = []
#length_list = []
#shot_list = []
start_list = []
end_list = []
label_list = []
frame_start = []
frame_end = []
while True:
    t1_1 = int(input("Action start (min): "))
    t1_2 = int(input("Action start (sec): "))
    t1 = t1_1*60 + t1_2
    t2_1 = int(input("Action end (min): "))
    t2_2 = int(input("Action end (sec): "))
    t2 = t2_1*60 + t2_2
    
    clip_time = str(round(time.time() * 1000))
    
    action_last = int(input("Select type of last action - {}(1)/{}(0): ".format(*format_list)))
    start_list.append(t1)
    end_list.append(t2)
    label_list.append(action_last)
    frame_1 = int(t1*myclip.fps)
    frame_2 = int(t2*myclip.fps)
    frame_start.append(frame_1)
    frame_end.append(frame_2)
    #if action_last == 1:
     
        # clipname = action1 + subfolder_fix + video + clip_prefix + clip_time + clip_ext
        # print(clipname)
        # myclip2 = myclip.subclip(t1, t2)
        # (w, h) = myclip2.size
        # cropped_clip = crop(myclip2, width=320, height=640, x_center=w/4*1.7, y_center=h/2)
        # cropped_clip.write_videofile(clipname, codec="mpeg4")
        
      #  movie = Movie_MP4(os.path.normpath(clipname))
       # movie.play()
           
# =============================================================================
#         batsman = input("Provide batsman name: ")
#         bowler = input("Provide bowler name: ")
#         foot = int(input("Select type of shot - front(1)/back(2): "))
#         risk = int(input("Risk involved in the shot - no(1),yes(2): "))
#         direction = int(input("Select direction of shot - offside(1)/legside(2)/straight(3): "))
#         line = int(input("Select line of bowler - off(1)/stump(2)/leg(3)/wide-off(4)/wide-leg(5): "))
#         length = int(input("Select length of the bowler - short(1)/good(2)/full(3)/toss(4): "))
#         batsman_list.append(batsman)
#         bowler_list.append(bowler)
#         foot_list.append(foot)
#         risk_list.append(risk)
#         direction_list.append(direction)
#         line_list.append(line)
#         length_list.append(length)
#         shot_list.append(clipname)
#         print("Total shots:", len(batsman_list))
#         pre_as = "autosave/"
#         ext_as = "_tags.csv"
#         df_interim_name = pre_as + clip_time + ext_as
#         df_tags_interim = pd.DataFrame({'Clip#' : shot_list, 'Batsman': batsman_list, 'Bowler': bowler_list, 'Foot': foot_list, 'risk': risk_list, 'direction': direction_list, 'line': line_list, 'length': length_list})
#         df_tags_interim.to_csv(df_interim_name,index=False)
# =============================================================================
    #else:
        # clipname = action2 + subfolder_fix + video + clip_prefix + clip_time + clip_ext
        # print(clipname)
        # myclip2 = myclip.subclip(t1, t2)
        # (w, h) = myclip2.size
        # cropped_clip = crop(myclip2, width=320, height=640, x_center=w/4*1.7, y_center=h/2)
        # cropped_clip.write_videofile(clipname, codec="mpeg4")
    
    #count = count + 1
    diff = t2-t1
    i = i + diff
    print("Total time elapsed: {} secs".format(i))
    
    
    #print("Last record: {}".format(t_last))
    #edit_input = int(input("Continue - Yes(1)/No(0): "))
    if i >= t_last:
        break

df_tags = pd.DataFrame({'Start_Time' : start_list, 'End_Time' : end_list, 'Label' : label_list, 'start_frames' : frame_start, 'end_frame' :frame_end})
df_tags.to_csv('tagged.csv', index=False)
# =============================================================================
# tag_time = str(round(time.time() * 1000))
# ext_f = "_tags.csv"
# tags_name = tag_time + ext_f
# df_tags = pd.DataFrame({'Clip#' : shot_list, 'Batsman': batsman_list, 'Bowler': bowler_list, 'Foot': foot_list, 'risk': risk_list, 'direction': direction_list, 'line': line_list, 'length': length_list})
# df_tags.to_csv(tags_name,index=False)
# 
# 
# =============================================================================
