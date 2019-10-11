# -*- coding: utf-8 -*-
from urllib import request, parse, error
import json
import argparse
import time
import datetime

def get_args(arglist=None):
    parser = argparse.ArgumentParser(description='Sumavision Autotest Tools')

    parser.add_argument('--file', type=str, default='9550A.rpc',
                        help = '待加载json-rpc脚本')
    parser.add_argument('--ip', type=str, default='192.165.53.210',
                        help='待测试的设备IP')
    parser.add_argument('--out', type=str, default='log.txt',
                        help='运行的结果记录，保存成文件')
    parser.add_argument('--count', type=int, default=-1,
                        help='轮询次数，-1为一直运行；运行时可按q键退出，打印统计信息')
    parser.add_argument('--print', type=int, default=1,
                        help='是否从串口打印，非0表示串口打印使能')
    if arglist is None:
        return parser.parse_args()
    else:
        return parser.parse_args(arglist)

def trace_log(fd, log):
    print(log)
    fd.write(log)
    
if __name__ == "__main__":
    """获取输入参数"""
    args = get_args()
    print(args)
    headers = {'Content-Type': 'application/json'}
    if args.count <= 0:
        count = 0
    else :
        count = args.count

    """"读入json文件"""
    with open(args.file) as load_f:
        load_dict = json.load(load_f)
        print(load_dict)

    """打开输出文件"""
    write_f = open(args.out, 'w')

    """遍历输入文件字典，并向目标IP发post"""
    current_count = 0
    while current_count < count or count == 0:

        trace_log(write_f, "loop count " + str(current_count) + ":")
        for rpc in load_dict:
            if rpc['type'] == 'post':
                encoded_data = json.dumps(rpc['data']).encode('utf-8')

                req = request.Request(
                    'http://'+ args.ip +'/goform/form_data',
                    headers=headers,
                    data=encoded_data)
                #读取结果
                try:
                    f = request.urlopen(req)
                except error.URLError as e:
                    trace_log(write_f, datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]  ") + "fail to connect\n")
                    continue

                page = f.read()
                page = page.decode('utf-8')

                log = datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]  ") + "Post :" + str(rpc['data'])+"\n"
                trace_log(write_f, log)
                log = "  result :" + page.strip() + "\n"
                trace_log(write_f, log)

            elif rpc['type'] == 'sleep':
                trace_log(write_f, "sleep "+ str(rpc['data']) + "s \n")
                time.sleep(rpc['data'])

        """计数，休眠5秒重新开始"""
        current_count += 1
        time.sleep(1)
    write_f.close()

"""
    requestData = {
        "jsonrpc": "2.0",
        "method": "network.get",
        "params": {"net": [{"dhcp": 0, "ipaddr": "", "mask": "", "gate": ""},
                           {"dhcp": 0, "ipaddr": "", "mask": "", "gate": ""}]},
        "id": 'NETWORK_CONFIG'
    };

    encoded_data = json.dumps(requestData).encode('utf-8')
    http = urllib3.PoolManager()
    headers = {'Content-Type': 'application/json'}
    request = http.request(
        'POST',
        'http://192.165.53.161/goform/form9630',
        headers=headers,
        body=encoded_data)
    print(request.data.decode())
    print(request.status)

    rpc = request.data.decode()
    print(rpc)
"""