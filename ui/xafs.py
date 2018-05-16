
from os import path
from pydm import Display
from epics import Motor, PV
#from bl09b import BL09BXAFS
import threading
import time

from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt
from bluesky import RunEngine
from device.nctDevice import Nct
#import device.startup
from ophyd.sim import motor
from databroker import Broker
from bluesky.plans import list_scan
from PyQt5.QtCore import QThread


#m1 = EpicsMotor("IOC:m1", name = "m1")
#m1.settle_time = 2

#nct = Nct("X09B1:EH:NCT:",name="nct", read_attrs=["v0","v1"])

class re(QThread):
    def __init__(self):
        super(re,self).__init__()
        '''
        self.energy_pv = [PV("X09B1:XAFS:Energy"+str(i)) for i in range(8)]
        self.step_pv = [PV("X09B1:XAFS:Step"+str(i)) for i in range(7)]
        self.RE = RunEngine({})
        self.db = Broker.named('temp')
        self.RE.subscribe(self.db.insert)
        #self.m1 = EpicsMotor("m1", name = "m1")
        #print(self.m1.connected)
        #self.m1.wait_for_connection()
        #print(self.m1.connected)
        self.m1 = motor'''
        print("re init")
        
    def get_scan_pos(self):
        energy = [self.energy_pv[i].get() for i in range(8)]
        step = [self.step_pv[i].get() for i in range(7)]
        scan_pos = []
        for i in range(7):
            pos = self.positions(energy[i], step[i], energy[i+1])
            scan_pos.extend(pos)
        return scan_pos
    
    def positions(self, start, step, end):
        pos = []
        x = start
        while x<end:
            pos.append(x)
            x = x+step
        return pos
        
    def run(self):
        i=0
        while(1):
            time.sleep(1)
            i=i+1
            print(i)
        '''
        #li = [0,1,2,3,4,5]
        li = self.get_scan_pos()
        self.RE(list_scan([self.m1], self.m1, li))
        print(li)
        dt = self.db[-1]
        data = dt.table()
        data.to_csv("xxx.csv")'''
        print("save")

class XAFS(Display):
    def __init__(self, parent=None, args=[]):
        super(XAFS, self).__init__(parent=parent, args=args)
        self.ui.btnStart.clicked.connect(self.start)
        self.ui.btnStop.clicked.connect(self.stop)
        self.ui.btnPara.clicked.connect(self.set_parameter)
        #self.m = Motor("m1")
        #self.d = [PV("IOC:m1.RBV"), PV("417:aiExample")]
        #self.m1 = EpicsMotor("m1", name = "m1")
        #self.m1.settle_time = 0
        self.energy_pv = [PV("X09B1:XAFS:Energy"+str(i)) for i in range(8)]
        self.step_pv = [PV("X09B1:XAFS:Step"+str(i)) for i in range(7)]
        #self.itime_pv = [PV("X09B1:XAFS:ITime"+str(i)) for i in range(7)]
        
        
    def ui_filename(self):
        return 'xafs.ui'
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
    


    def start(self):
        myre = re()
        myre.run()

        
    def wait_finished(self):
        print('a')

        #while(self.myscan.finished == 0 and self.myscan.stopped==0):
            #time.sleep(1)
        #self.ui.btnStart.setEnabled(True)
        
    def stop(self):
        print('a')
        self.myre.RE.stop()
        

    
    def set_parameter(self):
        energy = [0, 2, 5, 8, 10, 15, 18, 20]
        step = [1, 1.5, 1.5, 0.5, 0.5, 1, 1]
        for i in range(8):
            self.energy_pv[i].put(energy[i])
        for i in range(7):
            self.step_pv[i].put(step[i])


xafs= XAFS()

'''
while(aa):
    print(1)
    #self.ui.btnStart.setEnabled(False)
    db = Broker.named('temp')
    RE.subscribe(db.insert)
    #li = self.get_scan_pos()
    li = [0,1,2,3,4,5]
    m1 = EpicsMotor("m1", name = "m1")
    RE(list_scan([nct], m1, li))
    dt = db[-1]
    data = dt.table()
    data.to_csv("xxx.csv")
    print(2)
    aa=0
'''
