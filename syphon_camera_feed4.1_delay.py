## 10 seconds delay,keep play live

import cv2
import numpy as np
import syphon
from syphon.utils.numpy import copy_image_to_mtl_texture
from syphon.utils.raw import create_mtl_texture

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    server = syphon.SyphonMetalServer("Camera Stream")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    texture = create_mtl_texture(server.device, width, height)
    
    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

    buffer_frames = []
    max_buffer_frames = 150  # 假设帧率为30fps，则5秒对应150帧
    frame_counter = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("无法接收帧，退出...")
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgba = cv2.merge((frame_rgb, np.full((frame_rgb.shape[0], frame_rgb.shape[1]), 255, dtype=np.uint8)))
            
            # 累积前5秒的影像到缓冲区
            if frame_counter < max_buffer_frames:
                buffer_frames.append(frame_rgba)
            else:
                # 超过5秒后，交替播放缓冲区和实时影像
                buffer_index = frame_counter % max_buffer_frames
                blended_frame = cv2.addWeighted(buffer_frames[buffer_index], 0.5, frame_rgba, 0.5, 0)
                buffer_frames[buffer_index] = frame_rgba  # 更新缓冲区的帧
                
                cv2.imshow('Camera Feed', blended_frame[:, :, :3])  # 仅显示RGB通道
                copy_image_to_mtl_texture(blended_frame, texture)
                server.publish_frame_texture(texture)
            
            frame_counter += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        server.stop()

if __name__ == "__main__":
    main()
