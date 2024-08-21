##record each 8 seconds and loop to play
## replace if __name__ == "__main__": x = ?? , then set how many times to repeat.

import cv2
import numpy as np
import syphon
from syphon.utils.numpy import copy_image_to_mtl_texture
from syphon.utils.raw import create_mtl_texture
import time

def main(buffer_count=4):  # Assume you want to create 4 buffers
    cap = cv2.VideoCapture(0)  # Use iPhone camera
    if not cap.isOpened():
        print("Unable to open the camera")
        return
    
    server = syphon.SyphonMetalServer("Camera Stream")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    texture = create_mtl_texture(server.device, width, height)
    
    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

    buffers = [[] for _ in range(buffer_count)]
    buffers_filled = [False] * buffer_count
    max_buffer_frames = 240  # Assuming frame rate is 30fps, 8 seconds correspond to 240 frames
    frame_counter = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Unable to receive frames, exiting...")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgba = cv2.merge((frame_rgb, np.full((frame_rgb.shape[0], frame_rgb.shape[1]), 255, dtype=np.uint8)))
            
            # Play live image
            playback_frame = frame_rgba.copy()  # Initialize with live image
            
            # Calculate the current time segment
            current_time = frame_counter / 30.0
            
            for i in range(buffer_count):
                start_time = i * 8
                end_time = start_time + 8
                if current_time >= start_time and current_time < end_time and not buffers_filled[i]:
                    buffers[i].append(frame_rgba)
                    if len(buffers[i]) >= max_buffer_frames:
                        buffers_filled[i] = True
                        print(f"Buffer {i+1} filled at time: {time.time()} seconds, starts looping")
                elif buffers_filled[i]:
                    buffer_index = frame_counter % max_buffer_frames
                    playback_frame = cv2.addWeighted(buffers[i][buffer_index], 1.0 / (i + 2), playback_frame, 1.0 - 1.0 / (i + 2), 0)
            
            # Display and publish the mixed image
            cv2.imshow('Camera Feed', playback_frame[:, :, :3])  # Display only RGB channels
            copy_image_to_mtl_texture(playback_frame, texture)
            server.publish_frame_texture(texture)
            
            frame_counter += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        server.stop()

if __name__ == "__main__":
    x = 10  # Manually set the number of buffers
    main(buffer_count=x)
