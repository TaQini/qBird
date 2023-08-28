import ebird
import birdreport

x = ebird.ebird()
x.search(startTime=x.get_back_date(0),endTime=x.get_back_date(0))

y = birdreport.birdreport()
province = '北京市'
y.search(startTime=y.get_back_date(0), endTime=y.get_back_date(0), province=province)

