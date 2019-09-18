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
resname = 'udp://192.165.53.18:22000'
#resname='resource/1.ts'
CHUNK = 1024

#显示界面类
class XShower(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pictureLabel = QLabel()
        init_image = QPixmap("resource/cat.jpeg").scaled(XShow_width, XShow_height)
        pictureLabel.setPixmap(init_image)

        layout = QVBoxLayout()
        layout.addWidget(pictureLabel)

        self.pictureLabel = pictureLabel
        self.setLayout(layout)
        self.show()

def decode_stream(in_filename, **input_kwargs):

    container = av.open(in_filename, 'r')
   # print(container)
   # video_data = container.streams.video
        #stream_input=ffmpeg.input(in_filename, **input_kwargs)

        #video = stream_input.output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(XShow_width, XShow_height))
        #audio = stream_input.output('pipe:', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')


        #process2 = video.run_async(pipe_stdout=True)
        #process1 = audio.run_async(pipe_stdout=True)


    return container
#process1,

def extract_frame(win, queue):
    count = 1
    while True:

        if not queue.empty():
            packet = queue.get()
        else:
            time.sleep(0.030)
            continue
        count = count + 1
#"""
        for VideoFrame in packet.decode():
            frame_show= VideoFrame.reformat(width=XShow_width, height=XShow_height)
            img_array = frame_show.to_ndarray(format='rgb24')

            in_frame = (
                 np
                    .frombuffer(img_array, np.uint8)
                    .reshape([XShow_height, XShow_width,3])
            )

            temp_image = QImage(in_frame, XShow_width, XShow_height, QImage.Format_RGB888)
            temp_pixmap = QPixmap.fromImage(temp_image)
            win.pictureLabel.setPixmap(temp_pixmap)
#"""
        #time.sleep(1/60)

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, audio_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.audio_queue = audio_queue

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print
        "Starting " + self.name
        fo = open("foo.pcm", "wb+")
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        output=True)
        audio_queue = self.audio_queue
        aud_convert = av.audio.resampler.AudioResampler(format='s16', layout='mono', rate=16000)
        pts = 0
        count = 0
        #time.sleep(20)
        while True:
            if not audio_queue.empty():
                packet = audio_queue.get()
            else:
                time.sleep(0.030)
                continue

            for frame in packet.decode():
                frame.pts = pts
                pts += 2880
                frame1 = aud_convert.resample(frame)
                array = frame1.to_ndarray()
                pcm = (
                    np
                        .frombuffer(array, np.int16)
                )

                stream.write(pcm.tobytes())
                #fo.write(pcm)
                #print(pcm.tobytes())


        print
        "Exiting " + self.name

        # 停止数据流
        stream.stop_stream()
        stream.close()

        # 关闭 PyAudio
        p.terminate()

if __name__ == '__main__':
    mapp = QApplication(sys.argv)

    video_queue = queue.Queue(6000000)
    audio_queue = queue.Queue(1000000)
    #video_data = decode_stream(resname)
    thread_ts = tsk_ts_stream(1, "Thread-1", resname, video_queue, audio_queue)
    thread_ts.start()

    win = XShower()

    thread.start_new_thread( extract_frame, (win, video_queue, ) )

    # 创建新线程
    thread1 = myThread(1, "Thread-1", audio_queue)

    # 开启线程
    thread1.start()


   # time.sleep(1000)



    sys.exit(mapp.exec_())
