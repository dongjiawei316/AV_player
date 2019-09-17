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
        count = 1
        while True:
            for packet in container.demux():
                if packet.stream.type == 'video':
                    video_queue.put(packet)
                elif packet.stream.type == 'audio':
                    audio_queue.put(packet)
"""
            for frame in container.decode():
                #print(frame.__class__.__name__)
                if frame.__class__.__name__ == 'VideoFrame':
                    video_queue.put(frame)
                elif frame.__class__.__name__ == 'AudioFrame':
                    audio_queue.put(frame)
"""
"""
            for packet in container.demux():
                #print(str(packet.stream_index))
                if packet.stream_index == 0:
                    video_queue.put(packet)
                elif packet.stream_index == 1:
                    audio_queue.put(packet)
            for s in container.streams:

                if s.type == 'video':
                    print(s)
                    for packet in container.demux(s):
                        print(packet)
                        video_queue.put(packet)
                        count += 1
                        if count >= 10:
                            count = 1
                            break
                elif s.type == 'audio':
                    print(s)
                    for packet in container.demux(s):
                        audio_queue.put(packet)
                        count += 1
                        if count >= 10:
                            count = 1
                            break
"""




#for s in container.streams