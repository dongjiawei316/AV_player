# -*- coding: utf-8 -*-
import av
from av.dictionary import Dictionary
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

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数, options = ['-i','h265_aac.sdp']
        print
        "Starting " + self.name
        vars = dict(protocol_whitelist='file,udp,rtp')
        print(vars)
        container = av.open(file = self.stream_name, mode = 'r', options=vars)
        video_queue = self.video_queue
        audio_queue = self.audio_queue
        while True:
            for packet in container.demux():
                #print(type(packet.stream))
                #print(packet.is_corrupt)
                if packet.stream.type == 'video':
                    video_queue.put(packet)
                #elif packet.stream.type == 'audio':
                else:
                    #continue
                    audio_queue.put(packet)
                    #print(packet.buffer_size)
                   # print(packet.to_bytes())
                    #print(packet.stream.type)
