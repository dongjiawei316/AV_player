# -*- coding: utf-8 -*-
import av
import time
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading
import numpy as np

#视频播放类，从queue中接收视频码流，并解码播放
class Video_play(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, video_queue, window):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = video_queue
        self.window = window

    def run(self):
        queue = self.queue
        win = self.window

        show_width = win.pictureLabel.width()
        show_height = win.pictureLabel.height()
        last_pts = 0
        pts_delta = 0
        last_show_time = 0
        sleep_time = 0

        while True:
            if not queue.empty():
                packet = queue.get()
            else:
                time.sleep(0.01)
                continue

            for VideoFrame in packet.decode():

                if VideoFrame.pts == None:
                    continue

                frame_show = VideoFrame.reformat(width=show_width, height=show_height)
                img_array = frame_show.to_ndarray(format='rgb24')

                in_frame = (
                    np
                        .frombuffer(img_array, np.uint8)
                        .reshape([show_height, show_width, 3])
                )

                temp_image = QImage(in_frame, show_width, show_height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)

                pts_delta = VideoFrame.pts - last_pts
                pts_delta = pts_delta/90000.0

                show_time = time.time()

                if show_time < last_show_time + pts_delta - 0.002:
                    sleep_time = last_show_time + pts_delta - show_time - 0.002
                    if sleep_time > 0.1:
                        sleep_time = 0.1
                    #缓冲区超过25帧，则2倍速播放
                    if queue.qsize() > 25:
                        sleep_time = sleep_time/2
                    elif queue.qsize() < 5:
                        sleep_time += 0.003
                    time.sleep(sleep_time)

                win.pictureLabel.setPixmap(temp_pixmap)
                last_pts = VideoFrame.pts
                time_now = time.time()
                print("bufferring" + str(queue.qsize()) + "  pts : " + str(last_pts) + "  sleep_time : " + str(sleep_time) + " real frame interval : "+str(time_now - last_show_time))
                sleep_time = 0
                last_show_time = time_now
