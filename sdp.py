# -*- coding: utf-8 -*-
import json

def sdp_get_audio_desp(audio_type):
    if(audio_type == 'mpd'):
        desp = 'MPEG4-GENERIC/90000/1'
    elif(audio_type == 'pcma'):
        desp = "pcma/8000/1"
    else:
        desp = "pcmu/8000/1"
    return desp

def sdp_generate(config_file, channel):
    sdp_name = str(channel)+".sdp"
    """"读入json文件"""
    with open(config_file, "r", encoding='UTF-8') as load_f:
        config_json = json.load(load_f)
        print(config_json)
        audio_desp = sdp_get_audio_desp(config_json['audio_type'])
        with open(sdp_name,"w") as sdp_f:
            sdp_str= "v=0\n"
            sdp_str += "c=IN IP4 "+ config_json['ip']+"\n"
            sdp_str += "m=video "+ str(int(config_json['port_base']) + 20 * channel) + "  RTP/AVP  " + config_json['video_pt'] + "\n"
            sdp_str += "a=rtpmap:"+ config_json['video_pt'] + " " + config_json['video_type']+"/90000" + "\n"
            sdp_str += "v=0\n"
            sdp_str += "m=audio " + str(int(config_json['port_base']) + 20 * channel + 2) + " RTP/AVP " + config_json['audio_pt'] + "\n"
            sdp_str += "c=IN IP4 " + config_json['ip'] + "\n"
            sdp_str += "a = ptime:20\n"
            sdp_str += "a=rtpmap:" + config_json['audio_pt'] + " " + audio_desp + "\n"
            print(sdp_str)
            sdp_f.write(sdp_str)
    return sdp_name,config_json