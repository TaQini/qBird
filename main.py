import ebird
import birdreport
import json
import config
x = ebird.ebird(config.token)
checklists = x.search(startTime=x.get_back_date(3),endTime=x.get_back_date(0))
# x.show(checklists)
info = x.spp_info(checklists)
# print(info)

y = birdreport.birdreport()
province = '北京市'
checklists2 = y.search(startTime=y.get_back_date(0), endTime=y.get_back_date(0), province=province)
# y.show(checklists)
info2 = y.spp_info(checklists2)
# print(info2)

# 整合观测数据
merge = info2
for i in info:
    if i not in merge:
        merge[i] = info[i]
    else:
        merge[i] += info[i]

f = open('./test.db','w+')
f.write(str(merge))
f.close()
print(merge)

# sp = 'lewduc1'
# sciName = x.get_sciName_from_speciesCode(sp)
# comName = x.get_comName_from_speciesCode(sp)
# print(sciName,comName)
# sp1 = x.get_speciesCode_from_sciName(sciName)
# comName1 = x.get_comName_from_sciName(sciName)
# print(sp1,comName1)
