
from epics import caget, caput

class NCT(object):
    def __init__(self,prefix):
        self.p = prefix
        self.clear=self.p+":ClearAll.PROC"
        self.start=self.p+":Start.PROC"
        self.ch0=self.p+":CH0"
        self.ch1=self.p+":CH1"
        self.timer=self.p+":TimerPreset"
        self.v0 = self.p+":V0"
        self.v1 = self.p+":V1"
        self.f0 = self.p+":F0"
        self.f1 = self.p+":F1"
    def trigger(self):
        caput(self.clear,1,wait=True)
        caput(self.start,1,wait=True)
    def read(self):
        caput(self.ch0+".PROC",1,wait=True)
        cnt0=caget(self.ch0)
        caput(self.ch1+".PROC",1,wait=True)
        cnt1=caget(self.ch1)
        itime = caget(self.timer)
        ff0 = cnt0/itime
        ff1 = cnt1/itime
        vv0 = ff0*1E-5
        vv1 = ff1*1E-5
        caput(self.v0, vv0, wait=True)
        caput(self.v1, vv1, wait=True)
        caput(self.f0, ff0, wait=True)
        caput(self.f1, ff1, wait=True)
        return ff0, ff1, vv0, vv1


