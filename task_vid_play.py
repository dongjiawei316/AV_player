# -*- coding: utf-8 -*-
import av
import time
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading
import numpy as np

XShow_width = 1280
XShow_height = 720

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

        while True:
            if not queue.empty():
                packet = queue.get()
            else:
                time.sleep(0.030)
                continue

            for VideoFrame in packet.decode():
                frame_show = VideoFrame.reformat(width=XShow_width, height=XShow_height)
                img_array = frame_show.to_ndarray(format='rgb24')

                in_frame = (
                    np
                        .frombuffer(img_array, np.uint8)
                        .reshape([XShow_height, XShow_width, 3])
                )

                temp_image = QImage(in_frame, XShow_width, XShow_height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                win.pictureLabel.setPixmap(temp_pixmap)