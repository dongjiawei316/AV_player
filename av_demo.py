# -*- coding: utf-8 -*-
import av
import sys
from ipywidgets import interact
from matplotlib import pyplot as plt
import ipywidgets as widgets
import numpy as np
import time
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from cv2 import *
import _thread as thread
import threading
import pyaudio
import av.datasets
import queue
from task_ts_stream import *

# udp://192.165.53.18:22000
#probe = ffmpeg.probe('resource/1.ts')
#container = av.open('1.ts')

#for frame in container.decode(video=0):
#    frame.to_image().save('frame-%04d.jpg' % frame.index)

XShow_width = 1280
XShow_height = 720
#resname = 'udp://192.165.53.18:22020'
resname ='h265_aac.sdp'
resname = 'h265_g711A.sdp'
#resname='resource/1.ts'
CHUNK = 1024

#显示界面类
class XShower(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pictureLabel = QLabel()
        init_image = QPixmap("resource/wait.jpg").scaled(XShow_width, XShow_height)
        pictureLabel.setPixmap(init_image)

        layout = QVBoxLayout()
        layout.addWidget(pictureLabel)

        self.pictureLabel = pictureLabel
        self.setLayout(layout)
        self.show()

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

#音频播放类，从queue中接收音频码流，解码并进行播放
class Audio_play(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, audio_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.audio_queue = audio_queue

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print
        "Starting " + self.name
        #fo = open("foo.pcm", "wb+")

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=32000,
                        output=True)
        audio_queue = self.audio_queue
        aud_convert = av.audio.resampler.AudioResampler(format='s16', layout='mono', rate=32000)
        pts = 0
        pts_delta = 0
        #time.sleep(20)
        while True:
            if not audio_queue.empty():
                packet = audio_queue.get()
            else:
                time.sleep(0.030)
                continue

            for frame in packet.decode():
                #print(packet.stream.name)
                if packet.stream.name == 'pcm_alaw' or packet.stream.name == 'pcm_ulaw' :
                    pts_delta = 160
                else:
                    pts_delta = frame.samples * 90000 / frame.rate

            frame.pts = pts
            pts += pts_delta
            frame1 = aud_convert.resample(frame)
            array = frame1.to_ndarray()
            pcm = (
                 np
                    .frombuffer(array, np.int16)
             )

            stream.write(pcm.tobytes())
                #fo.write(pcm)
                #print(pcm.tobytes())

        # 停止数据流
        stream.stop_stream()
        stream.close()

        # 关闭 PyAudio
        p.terminate()

if __name__ == '__main__':
    mapp = QApplication(sys.argv)

    video_queue = queue.Queue(6000000)
    audio_queue = queue.Queue(1000000)

    #ts流解析线程，将一路ts流分离成音频、视频两路，通过queue发出来
    thread_ts = tsk_ts_stream(1, "Thread-1", resname, video_queue, audio_queue)
    thread_ts.start()

    win = XShower()

    # 创建新线程
    thread_vid_play = Video_play(2, "Thread-Video", video_queue, win)
    thread_aud_play = Audio_play(1, "Thread-Audio", audio_queue)

    # 开启线程
    thread_aud_play.start()
    thread_vid_play.start()

    sys.exit(mapp.exec_())
