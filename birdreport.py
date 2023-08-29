import hashlib
import json

import execjs
import pandas as pd
import requests

import urllib
import time
import sys

class birdreport:
    with open("./jQuertAjax.js", "r", encoding="utf-8") as f:
        node_path = "./node_modules"
        ctx = execjs.compile(f.read(), cwd=node_path)

    def get_back_date(self, n):
        t = int(time.time()) - n*60*60*24
        # ta_now = time.localtime(now)
        ta = time.localtime(t)
        return time.strftime("%Y-%m-%d", ta)

    def md5(self, text):
        hl = hashlib.md5()
        hl.update(text.encode(encoding='utf-8'))
        return hl.hexdigest()

    def getTimestamp(self):
        return self.ctx.call("getTimestamp")

    def getRequestId(self):
        return self.ctx.call("getUuid")

    def encrypt(self, text):
        return self.ctx.call("encrypt", text)

    def decrypt(self, text):
        return self.ctx.call("decode", text)

    def format(self, text):
        return self.ctx.call("format", text)

    def get_headers(self, request_id, timestamp, sign):
        # sign = md5(format_param + request_id + str(timestamp))
        return {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://www.birdreport.cn',
            'Referer': 'http://www.birdreport.cn/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'requestId': request_id,
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sign': sign,
            'timestamp': str(timestamp),
        }

    def get_request_info(self, _data):
        format_data = self.format(_data)
        encrypt_data = self.encrypt(format_data)
        timestamp = self.getTimestamp()
        request_id = self.getRequestId()
        sign = self.md5(format_data + request_id + str(timestamp))
        headers = self.get_headers(request_id, timestamp, sign)
        return headers, encrypt_data

    def get_report_detail(self, aid):
        format_params = f"activityid={str(aid)}"
        # print(format_params)
        a = self.get_decrypted_data(format_params, "https://api.birdreport.cn/front/activity/get")
        # print(a)
        return a

    def get_taxon(self, aid):
        format_params = f"page=1&limit=1500&activityid={aid}"
        return self.get_decrypted_data(format_params, "https://api.birdreport.cn/front/activity/taxon")

    def get_report_url_list(self, page, limit, data):
        # format_params = f"page={page}&limit={limit}&taxonid=&startTime=&endTime=&province=&city=&district=&pointname=&username=&serial_id=&ctime=&taxonname=&state=&mode=0&outside_type=0"
        params = {
            "page":f"{page}",
            "limit":f"{limit}",
            "taxonid":f"{data['taxonid']}",
            "startTime":f"{data['startTime']}",
            "endTime":f"{data['endTime']}",
            "province":f"{data['province']}",
            "city":f"{data['city']}",
            "district":f"{data['district']}",
            "pointname":f"{data['pointname']}",
            "username":f"{data['username']}",
            "serial_id":f"{data['serial_id']}",
            "ctime":f"{data['ctime']}",
            "taxonname":f"{data['taxonname']}",
            "state":f"{data['state']}",
            "mode":'0',
            "outside_type":'0'
        }

        # format_params = f"page={page}&limit={limit}&taxonid=&startTime={start}&endTime={end}&province=%E5%8C%97%E4%BA%AC%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&district=&pointname=&username=&serial_id=&ctime=&taxonname=&state=2&mode=0&outside_type=0"
        # print(format_params)
        a = self.get_decrypted_data(urllib.parse.urlencode(params), 
            "https://api.birdreport.cn/front/record/activity/search")
        # print(a)
        return a

    def get_decrypted_data(self, format_param, url):
        # 构造请求头，和请求参数加密
        headers, encrypt_data = self.get_request_info(format_param)

        response = requests.post(url, headers=headers, data=encrypt_data)
        encrypt_res = response.json()
        # 解密数据
        _data = self.decrypt(encrypt_res['data'])
        return json.loads(_data)

    def get_all_report_url_list(self, data):
        _data_list = []
        # with open("./aid.txt", "r+", encoding="utf-8") as _f:
        #     lines = _f.readlines()
        #     for line in lines:
        #         _data_list.append(json.loads(line.replace("\n", "")))
        # if len(_data_list) > 0:
        #     # print(_data_list)
        #     return _data_list
        page = 1
        limit = 100
        _data_list = []
        while 1:
            try:
                report_list = self.get_report_url_list(page, limit, data)
                for report in report_list:
                    if report["state"] == 1:
                        continue
                    _data_list.append(report)
                print(f"获取第{page}页")
            except Exception as e:
                continue
            if len(report_list) == 0:
                break
            page += 1
        print(f"共获取到{len(_data_list)}份报告")
        # with open("aid.txt", "w+", encoding="utf-8") as _f:
        #     for _item in _data_list:
        #         _f.write(json.dumps(_item))
        #         _f.write("\n")
        return _data_list

    def search(self, taxonid='', startTime='', endTime='', province='', city='', district='', pointname='', username='', serial_id='', ctime='', taxonname='', state=''):
        # df = {"位置": [], "坐标": [], "名称": [], "数量": []}

        data = {
            "taxonid":f"{taxonid}",
            "startTime":f"{startTime}",
            "endTime":f"{endTime}",
            "province":f"{province}",
            "city":f"{city}",
            "district":f"{district}",
            "pointname":f"{pointname}",
            "username":f"{username}",
            "serial_id":f"{serial_id}",
            "ctime":f"{ctime}",
            "taxonname":f"{taxonname}",
            "state":f"{state}"
        }

        res = self.get_all_report_url_list(data)

        id_list = []
        checklists = []
        for item in res:
            id_list.append(item["id"])

        print(id_list)

        for _id in id_list:
            try:
                # print(_id)
                detail = self.get_report_detail(_id)
                # print('detail',detail)
                taxons = self.get_taxon(_id)
                # print(json.dumps(taxons,sort_keys=True, indent=4, separators=(',', ': ')))
                # print('taxons',taxons)
                detail["obs"] = taxons
                checklists.append(detail)
                # print(json.dumps(detail,sort_keys=True, indent=4, separators=(',', ': ')))
                for taxon in taxons:
                    # df["位置"].append(detail["point_name"])
                    print(detail["serial_id"],
                        detail["point_name"],
                        detail["location"],
                        taxon["taxon_name"],
                        taxon["latinname"],
                        taxon["taxon_count"])
                    # df["坐标"].append(detail["location"])
                    # df["地址"].append(detail["address"])
                    # df["名称"].append(taxon["taxon_name"])
                    # df["数量"].append(taxon["taxon_count"])
                    # {'outside_type': 0, 
                    # 'englishname': 'Mallard', 
                    # 'taxon_count': 1, 
                    # 'activity_id': 489541, 
                    # 'taxonordername': '雁形目', 
                    # 'taxon_id': 90, 
                    # 'taxon_name': '绿头鸭', 
                    # 'taxonfamilyname': '鸭科', 
                    # 'latinname': 'Anas platyrhynchos', 
                    # 'record_image_num': 0}
                # break
            except Exception as e:
                print(f"{_id} error")
                print(e)
        return checklists
        # data_frame = pd.DataFrame(df)
        # data_frame.to_excel("info.xlsx", index=False)
    def show(self, checklists):
        for item in checklists:
            lng, lat = item['location'].split(',')        
            print(lat, lng, item['point_name'])
            obs = item['obs']
            for taxon in obs:
                sciName = taxon['latinname']
                comName = taxon['taxon_name']
                howManyStr = taxon["taxon_count"]
                print(sciName, comName, howManyStr)

    def spp_info(self, checklists):
        info = {}
        for item in checklists:
            lng, lat = item['location'].split(',')        
            obs = item['obs']
            obsDt = item['timebegin']
            for taxon in obs:
                sciName = taxon['latinname']
                comName = taxon['taxon_name']
                howManyStr = taxon["taxon_count"]
                if comName not in info:
                    info[comName] = []
                info[comName].append((obsDt, howManyStr, lat, lng, item['point_name'],1))
        return info
