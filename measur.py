from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import re


class MeasType(Enum):
    SPO2 = 1
    HR = 2
    TEMP = 3


@dataclass
class Measurement:
    measurementTime: datetime = datetime.min
    measurementType: MeasType = MeasType.SPO2
    value: float = 0.0


class Realisesampling:
    inputtext = ("{2024-01-03T10:11:50, TEMP, 39.11}"
                 "{2024-01-03T10:01:10, SPO2, 99.11}"
                 "{2024-01-03T10:04:11, SPO2, 98.78}"
                 "{2024-01-03T10:06:18, SPO2, 95.08}")
    dtstart = '2000-01-03T10:04:45'
    dicttypes = {}
    outputlines = ""

    def samplemeasurements1(self, startofsampling: datetime):
        datalines = re.findall("\{(.*?)\}", self.inputtext)
        datalines.sort()
        m2 = Measurement()
        for x in datalines:
            x1 = x.replace(" ", "")
            l3 = x1.split(",")
            m2.measurementTime = datetime.fromisoformat(l3[0])
            if m2.measurementTime < startofsampling:
                break
            m2.measurementType = eval("MeasType."+l3[1])
            m2.value = l3[2]
            tminperiod = m2.measurementTime.timetuple()
            minperiod = tminperiod[4]
            fordelta = minperiod//5*5
            timewithdelta = m2.measurementTime.replace(minute=fordelta, second=0)
            timewithdelta = timewithdelta + timedelta(minutes=5)
            ind_dict = m2.measurementType.name
            self.dicttypes[ind_dict, timewithdelta] = \
                (timewithdelta.isoformat(), m2.measurementType.name, m2.value)


r = Realisesampling()
r.samplemeasurements1(datetime.fromisoformat(r.dtstart))
for line1 in r.dicttypes.values():
    r.outputlines += (str(line1).replace("'", "").replace("(", "{").replace(")", "}")+"\n")
print(r.outputlines)