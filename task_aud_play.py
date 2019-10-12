# -*- coding: utf-8 -*-
import numpy as np
import threading
import pyaudio
import av
import time

#音频播放类，从queue中接收音频码流，解码并进行播放
class Audio_play(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, audio_queue, buffering_time):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.audio_queue = audio_queue
        self.buffering_time = buffering_time

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
        buffer_time_in_ms = self.buffering_time
        buffering_nums = 100

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
                    delta_in_ms = pts_delta / 8
                else:
                    pts_delta = frame.samples * 90000 / frame.rate
                    delta_in_ms = pts_delta * 1000 / frame.rate
                buffering_nums = buffer_time_in_ms / delta_in_ms

                frame.pts = pts
                pts += pts_delta
                frame1 = aud_convert.resample(frame)
                array = frame1.to_ndarray()
                pcm = (
                    np
                        .frombuffer(array, np.int16)
                )

                if audio_queue.qsize() > buffering_nums:
                    print("audio buffer too much " + str(audio_queue.qsize()) + " > " + str(buffering_nums))
                    continue;

                stream.write(pcm.tobytes())
                #fo.write(pcm)
                #print(pcm.tobytes())

        # 停止数据流
        stream.stop_stream()
        stream.close()

        # 关闭 PyAudio
        p.terminate()