import ebird
import birdreport
import json
import config
x = ebird.ebird(config.token)
sp = 'lewduc1'
sciName = x.get_sciName_from_speciesCode(sp)
comName = x.get_comName_from_speciesCode(sp)
print(sciName,comName)
sp1 = x.get_speciesCode_from_sciName(sciName)
comName1 = x.get_comName_from_sciName(sciName)
print(sp1,comName1)

checklists = x.search(startTime=x.get_back_date(3),endTime=x.get_back_date(1))
x.show(checklists)


# y = birdreport.birdreport()
# province = '北京市'
# y.search(startTime=y.get_back_date(0), endTime=y.get_back_date(0), province=province)

