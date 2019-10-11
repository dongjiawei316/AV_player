# -*- coding: utf-8 -*-
from urllib import request, parse, error
import json

import time
import datetime

def device_9550Av3_start(dev_inf, config, channel):
    headers = {'Content-Type': 'application/json'}
    rpc_dic = {}
    rpc_dic['jsonrpc'] = "2.0"
    rpc_dic['method'] = "encoder.set"
    rpc_dic['id'] = "testid"
    cmd_snd = {}

    cmd_snd['ctrl'] ='1'
    cmd_snd['ip_send_addr'] = config['ip']
    cmd_snd['ip_send_port'] = str(int(config['port_base']) + 20 * channel)
    cmd_snd['pack_type'] = '0'
    cmd_params={}
    cmd_params['send']=cmd_snd

    rpc_dic['params'] = cmd_params

    print(rpc_dic)
    encoded_data = json.dumps(rpc_dic).encode('utf-8')

    req = request.Request(
        'http://' + dev_inf['ip'] + '/goform/form_data',
        headers=headers,
        data=encoded_data)
    try:
        f = request.urlopen(req)
    except error.URLError as e:
        print(datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]  ") + "fail to connect\n")

    page = f.read()
    page = page.decode('utf-8')
    print(page)

    #查询
    rpc_dic['method'] = "encoder.get"
    encoded_data = json.dumps(rpc_dic).encode('utf-8')

    req = request.Request(
        'http://' + dev_inf['ip'] + '/goform/form_data',
        headers=headers,
        data=encoded_data)
    try:
        f = request.urlopen(req)
    except error.URLError as e:
        print(datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]  ") + "fail to connect\n")

    page = f.read()
    page = page.decode('utf-8')
    print(page)

def device_9550Av3_stop(dev_inf):
    headers = {'Content-Type': 'application/json'}
    rpc_dic = {}
    rpc_dic['jsonrpc'] = "2.0"
    rpc_dic['method'] = "encoder.set"
    rpc_dic['id'] = "testid"
    cmd_snd = {}
    cmd_snd['ctrl'] = '0'
    cmd_params={}
    cmd_params['send']=cmd_snd
    rpc_dic['params'] = cmd_params

    encoded_data = json.dumps(rpc_dic).encode('utf-8')

    req = request.Request(
        'http://' + dev_inf['ip'] + '/goform/form_data',
        headers=headers,
        data=encoded_data)
    try:
        f = request.urlopen(req)
    except error.URLError as e:
        print(datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]  ") + "fail to connect\n")

