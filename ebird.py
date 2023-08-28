import requests
import json
import time
import config

# url = "https://api.ebird.org/v2/data/obs/CN-11/recent"
# url = "https://api.ebird.org/v2/data/obs/geo/recent?lat=39.85933&lng=116.68708&sort=species&dist=50&back=3"
# url = "https://api.ebird.org/v2/product/spplist/CN-11"

class ebird:
    token = config.token

    def get_recent_obs(self, regionCode='CN-11',back=7):
        url = f"https://api.ebird.org/v2/data/obs/{regionCode}/recent?back={back}&sppLocale=zh_SIM"
        payload={}
        headers = {
            'X-eBirdApiToken': self.token
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.text
        return json.loads(res)

    def get_historic_obs(self, regionCode='CN-11', date=''):
        url = f"https://api.ebird.org/v2/data/obs/{regionCode}/historic/{date}?sppLocale=zh_SIM"
        payload={}
        headers = {
            'X-eBirdApiToken': self.token
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.text
        return json.loads(res)    

    def get_historic_list(self, regionCode='CN-11', date=''):
        url = f"https://api.ebird.org/v2/product/lists/{regionCode}/{date}"
        payload={}
        headers = {
            'X-eBirdApiToken': self.token
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.text
        return json.loads(res)    

    def get_report_detail(self, subId):
        url = f"https://api.ebird.org/v2/product/checklist/view/{subId}"
        payload={}
        headers = {
            'X-eBirdApiToken': self.token
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.text
        return json.loads(res)

    # detail = get_report_detail(token=token, subId='S148184150')
    # taxons = detail['obs']
    # for taxon in taxons:
    #     print(detail["subId"],
    #         detail["locId"],
    #         taxon["speciesCode"],
    #         taxon["howManyStr"])

    # res = get_historic_obs(date='2023/8/27')
    # # res = get_recent_obs()
    # # # print(json.dumps(res,sort_keys=True, indent=4, separators=(',', ': ')))
    # for _list in res:
    #     try:
    #         if "howMany" in _list:
    #             howMany = _list["howMany"]
    #         else:
    #             howMany = 'X'
    #         # print(_list)
    #         print(_list["subId"],
    #             _list["speciesCode"],
    #             _list["comName"],
    #             howMany,
    #             _list["lat"],
    #             _list["lng"],
    #             _list["locName"]
    #             )
    #     except Exception as e:
    #         print(f"{_list} error")
    #         print(e)


    # def get_all_report_url_list():
    #     pass

    # res = get_recent_obs()
    # print(json.dumps(res,sort_keys=True, indent=4, separators=(',', ': ')))
    # print(json.dumps(res,sort_keys=True, indent=4, separators=(',', ': ')))

    def get_back_date(self, n):
        t = int(time.time()) - n*60*60*24
        ta = time.localtime(t)
        return time.strftime("%Y/%m/%d", ta)

    def date_to_ta(self, date):
        return int(time.mktime(time.strptime(date,"%Y/%m/%d")))

    def ta_to_date(self, ta):
        return time.strftime("%Y/%m/%d", time.localtime(ta))

    def search(self, taxonid='', startTime='', endTime='', province='', city='', district='', pointname='', username='', serial_id='', ctime='', taxonname='', state=''):
        id_list = []
        id_detail = {}

        ta_s = self.date_to_ta(startTime)
        ta_e = self.date_to_ta(endTime)
        # print(ta_s, ta_e)
        back = int((ta_e - ta_s) / 86400)
        # print(back)
        date_list = [self.ta_to_date(ta_s+86400*i) for i in range(back+1)]
        print('查询日期\n',date_list)

        print('正在获取日期范围内的checklist id...')

        for _date in date_list:
            res = self.get_historic_list(date=_date)
            # print(json.dumps(res,sort_keys=True, indent=4, separators=(',', ': ')))

            for item in res:
                try:
                    id_detail[item["subId"]] = {
                        'lat':item["loc"]["lat"],
                        'lng':item["loc"]["lng"],
                        'locName':item["loc"]["locName"], 
                        'userDisplayName':item["userDisplayName"]
                    }
                    # print(item["subId"],
                    #     item["loc"]["lat"],
                    #     item["loc"]["lng"],
                    #     item["loc"]["locName"], 'by', 
                    #     item["userDisplayName"]
                    #     )
                    id_list.append(item["subId"])
                except Exception as e:
                    print(f"{item} error")
                    print(e)

        print(id_list)
        print(f'共计{len(id_list)}份报告')
        for _id in id_list:
            detail = self.get_report_detail(subId=_id)
            # print(json.dumps(detail,sort_keys=True, indent=4, separators=(',', ': ')))
            
            taxons = detail['obs']
            for taxon in taxons:
                print(detail["subId"],
                    detail["obsDt"],
                    id_detail[_id]["lat"],
                    id_detail[_id]["lng"],
                    id_detail[_id]["locName"],
                    taxon["speciesCode"],
                    taxon["howManyStr"])
