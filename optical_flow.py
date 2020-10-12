import cv2
import numpy as np
import pandas as pd
import os
import math

df = pd.read_csv('tagged.csv')

#(df[(df['start_frames']<50) & (df['end_frame']>50)]['Label'].values[0])

# Get a VideoCapture object from video and store it in vs
vc = cv2.VideoCapture("2016-0101-000018-005-gaxehhze_PQ0dy2rI.mpeg")
# Read first frame
ret, first_frame = vc.read()
# Scale and resize image
resize_dim = 600
max_dim = max(first_frame.shape)
scale = resize_dim/max_dim
first_frame = cv2.resize(first_frame, None, fx=scale, fy=scale)
# Convert to gray scale 
height, width = first_frame.shape[:2]
first_frame = first_frame[0:height, math.floor(width/4):math.floor(3*(width/4))]
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# Create mask
mask = np.zeros_like(first_frame)
# Sets image saturation to maximum
mask[..., 1] = 255
# cv2.imshow('a',first_frame)
# cv2.waitKey(5000)
# cv2.destroyAllWindows()

#out = cv2.VideoWriter('video.mp4',-1,1,(600, 600))
images = []
labels = []
success = True
fps = int(vc.get(cv2.CAP_PROP_FPS))
count = 1
prev_frame = count
curr_frame = count
folders = ["shots", "non_shots"]
clip_prefix = "clip_"
subfolder_fix = "/"
clip_ext = ".jpg"
loc = 0
path = os.getcwd()
for folder in folders:
    if not os.path.exists(os.path.join(path, folder)):
        os.makedirs(os.path.join(path, folder),exist_ok=True)
while(success):
    # Read a frame from video
    succes, frame = vc.read()
    if success == False:
        break
    elif count%(fps/2) == 0:
    # Convert new frame format`s to gray scale and resize gray frame obtained
        loc= loc+1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=scale, fy=scale)
        gray = gray[0:height, math.floor(width/4):math.floor(3*(width/4))]
        #prev_gray = prev_gray[0:height, math.floor(width/4):math.floor(3*(width/4))]
        # Calculate dense optical flow by Farneback method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowfarneback
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale =0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
        # Compute the magnitude and angle of the 2D vectors
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        # Set image hue according to the optical flow direction
        mask[..., 0] = angle * 180 / np.pi
        # Set image value according to the optical flow magnitude (normalized)
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        # Convert HSV to RGB (BGR) color representation
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        
        # Resize frame size to match dimensions
        frame = cv2.resize(frame, None, fx=scale, fy=scale)
        frame =frame[0:height, math.floor(width/4):math.floor(3*(width/4))]
        # Open a new window and displays the output frame
        dense_flow = cv2.addWeighted(frame, 1,rgb, 2, 0)
        #images.append(dense_flow)
        prev_frame = curr_frame
        curr_frame = count
        prev_label = df[(df['start_frames']<=prev_frame) & (df['end_frame']>=prev_frame)]['Label'].values[0]
        curr_label = df[(df['start_frames']<=curr_frame) & (df['end_frame']>=curr_frame)]['Label'].values[0]
        if prev_label == 1 or curr_label == 1:
            #labels.append(1)
            clipname = "shots" +subfolder_fix+ str(loc) + clip_ext
            cv2.imwrite(clipname, dense_flow );
        else:
            #labels.append(0)
            clipname = "non_shots"+ subfolder_fix+ str(loc) + clip_ext
            cv2.imwrite(clipname, dense_flow );
        #cv2.imshow("Dense optical flow", dense_flow)
        #out.write(dense_flow)
        # Update previous frame
        prev_gray = gray
        
        # Frame are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break
    count+=1
# The following frees up resources and closes all windows
vc.release()
cv2.destroyAllWindows()
len(images)
len(labels)
labels
df1 = pd.DataFrame({'images' : images, 'labels' : labels})
df1.to_csv('img.csv', index=False)
for image in images:
    cv2.imshow('a',image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
