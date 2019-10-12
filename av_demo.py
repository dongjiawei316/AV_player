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
import json
from task_ts_stream import *
from task_aud_play import *
from task_vid_play import *
from task_vid_play import *
from sdp import  *
from device_9550Av3 import  *

# udp://192.165.53.18:22000
#probe = ffmpeg.probe('resource/1.ts')
#container = av.open('1.ts')

XShow_width = 1280
XShow_height = 720
resname = 'udp://192.165.53.18:22020'
#resname ='h265_aac.sdp'
#resname = 'h265_g711A.sdp'
#resname='resource/1.ts'
dev_list_file = 'configs/dev_list.json'
config_file = 'configs/local.json'

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

if __name__ == '__main__':
    mapp = QApplication(sys.argv)

    #创建对话框
    win = XShower()

    """"读入json文件"""
    with open(dev_list_file, encoding='UTF-8') as load_f:
        dev_list = json.load(load_f)
        print(dev_list)

    channel = 2
    resname,config = sdp_generate(config_file, channel)
    device_9550Av3_start(dev_list[channel - 1], config, channel)

    video_queue = queue.Queue(1000000)
    audio_queue = queue.Queue(1000000)

    # 创建音视频解码线程
    thread_vid_play = Video_play(2, "Video-dec", video_queue, win)
    thread_aud_play = Audio_play(1, "Audio-dec", audio_queue, 100)

    #ts流解析线程，将一路ts流分离成音频、视频两路，通过queue发出来
    thread_stream = tsk_ts_stream(1, "parse-stream", resname, video_queue, audio_queue)

    # 启动线程
    thread_aud_play.start()
    thread_vid_play.start()
    thread_stream.start()

    sys.exit(mapp.exec_())
