import requests
import config
import json

def query_species(specie):
    url = f"https://api.ebird.org/v2/ref/taxonomy/ebird?species={specie}&locale=zh_SIM&fmt=json"
    payload={}
    headers = {
        'X-eBirdApiToken': config.token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    return json.loads(res)

def get_species(specie):
    url = f"https://api.ebird.org/v2/ref/taxon/forms/{specie}"
    payload={}
    headers = {
        'X-eBirdApiToken': config.token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    return eval(res)

def get_spplist(regionCode):
    url = f"https://api.ebird.org/v2/product/spplist/{regionCode}"
    payload={}
    headers = {
        'X-eBirdApiToken': config.token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    res = response.text
    return eval(res)

# species database
# online -> offline 
spp_list = get_spplist('CN')
spp_dict = {}
l = []
i = 0
print(len(spp_list))
for spp in spp_list:
    a = query_species(spp)
    l += a
    # print(json.dumps(a,sort_keys=True, indent=4, separators=(',', ': ')))
    print(i, a[0]['comName'],spp,a[0]['sciName'])
    i+=1

# print(l)
# f = open('ebird-CN.json','w+')
# ll = json.dumps(l,sort_keys=True, indent=4, separators=(',', ': '))
# print(ll)
# f.write(ll)
# f.close()