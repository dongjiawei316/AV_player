# -*- coding: utf-8 -*-
import av
import threading
import queue

#从网络上接收TS流，分离出音视频数据，发给对应的解码线程
class tsk_ts_stream(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, stream_name, video_queue, audio_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stream_name = stream_name
        self.video_queue = video_queue
        self.audio_queue = audio_queue
        print("thread " + str(stream_name) + "  started")

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print
        "Starting " + self.name
        container = av.open(self.stream_name, 'r')
        video_queue = self.video_queue
        audio_queue = self.audio_queue
        while True:
            for s in container.streams:
                if s.type == 'video':
                    for packet in container.demux(s):
                        video_queue.put(packet)
                elif s.type == 'audio':
                    for packet in container.demux(s):
                        audio_queue.put(packet)

        print
        "Exiting " + self.name



#for s in container.streams