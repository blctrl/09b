
from blcscan import BLCScan1
from device.nct import NCT
from epics import caput, caget 
import time
import threading
import math
import pandas as pd

class ScanRC(BLCScan1):
    '''
    Scan for rocking curve
    DATE: 2018-5

    m: motor, Motor object
    d: detectors, BL09BNCT object
    step > 0
    '''
    def __init__(self, start, step, end, m, d):
        super().__init__(start, step, end, m, d)
        self.change_dn()
        #self.dn = 2
        
    def change_dn(self):
        self.dn = 2
        self.mRA = [0 for i in range(self.npts)]
        self.dRA = [[0 for i in range(self.npts)] for j in range(self.dn)]
        
    def scan_logic(self):
        pos = self.get_pos()
        #caput("X09B1:RC:D0CV", 0, wait=True)
        #caput("X09B1:RC:D1CV", 0, wait=True)
        #caput("X09B1:RC:MCV", 0, wait=True)
        for i in range(self.npts):
            if self.stopped == 1:
                break
            caput("X09B1:RC:Next", pos[i], wait=True)
            self.move_motor(pos[i])
            self.mRA[i] = self.read_motor()
            # detector value list @ current scan position
            dvs = self.read_detectors()
            for j in range(len(dvs)):
                self.dRA[j][i] = dvs[j]
            #print(self.mRA[i], dvs[0], dvs[1])
            #caput("X09B1:RC:D0CV", dvs[0], wait=True)
            #caput("X09B1:RC:D1CV", dvs[1], wait=True)
            #caput("X09B1:RC:MCV", self.mRA[i], wait=True)
            
    def save_data(self, filename):
        table = {"motor readback":self.mRA, "I0":self.dRA[0], "I1":self.dRA[1]}
        tb = pd.DataFrame(table)
        tb.to_csv(filename)
    
    def read_detectors(self):
        return(self.d[0].read_once1())



class ScanXAFS(BLCScan1):
    '''
    Scan for XAFS
    DATE: 2018-5

    m: motor, Motor object
    d: detectors, BL09BNCT object
    step > 0
    '''
    def __init__(self, start, step, end, m, d):
        super().__init__(start, step, end, m, d)
        
    def scan_logic(self):
        pos = self.get_pos()
        for i in range(self.npts):
            if self.stopped == 1:
                break
            caput("X09B1:XAFS:Next", pos[i], wait=True)
            self.move_motor(pos[i])
            self.mRA[i] = self.read_motor()
            # detector value list @ current scan position
            dvs = self.read_detectors()
            for j in range(len(dvs)):
                self.dRA[j][i] = dvs[j]
            lncv = math.log(math.e, dvs[0]/dvs[1])
            caput("X09B1:XAFS:D0CV", dvs[0], wait=True)
            caput("X09B1:XAFS:D1CV", dvs[1], wait=True)
            caput("X09B1:XAFS:LNCV", lncv, wait=True)
            caput("X09B1:XAFS:MCV", self.mRA[i], wait=True)

    #def read_detectors(self):
        #return(self.d.read_once1())

class BL09BNCT(NCT):
    """
    NCT08-01 @ BL09B1
    DATE: 2018-5
    """
    def __init__(self, prefix):
        super().__init__(prefix)
        self.itime = self.p+":SetTimer.A"
        #self.t = 1

    def set_itime(self, t=1):
        caput(self.itime, t, wait=True)
        self.t = t

    # for monitor
    def read_once(self):
        self.trigger()
        time.sleep(self.t)
        self.read()

    # for scan
    def read_once1(self):
        self.trigger()
        time.sleep(caget(self.itime))
        f0, f1, v0, v1 = self.read()
        return [f0, f1]





class BL09BXAFS(object):
    """
    xafs piecewise scan
    DATE: 2018-5
    
    energy: energy list
    step: step list
    itime: itime list
    m: motor, Motor object
    d: detectors, BL09BNCT object
    step > 0
    """
    def __init__(self, energy, step, itime, m, d):
        self.energy = energy
        self.step = step
        self.itime = itime
        self.m = m
        self.d = d
        self.stopped = 0
        self.lock = threading.Lock()

    def scan(self):
        t = threading.Thread(target=self.scan_process, args=())
        t.start()
        
    def scan_process(self):
        self.lock.acquire()
        try:
            self.stopped = 0
        finally:
            self.lock.release()
        self.finished = 0
        self.scan_logic()
        self.finished = 1
        
    def scan_logic(self):
        for i in range(len(self.step)):
            print("Seg", i)
            start = self.energy[i]
            step = self.step[i]
            end = self.energy[i+1]
            print(start, step, end)
            if self.stopped == 1:
                break
            subscan = ScanXAFS(start, step, end, self.m, self.d)
            subscan.set_settlingTime(caget("X09B1:XAFS:SettlingTime"))
            subscan.scan()
            time.sleep(1)
            # wait until subscan finished or button Stop pressed
            while(subscan.finished == 0):
                if self.stopped == 1:
                    subscan.stop()
                    break
                time.sleep(1)
            print(subscan.mRA, subscan.dRA)
            
    def stop(self):
         self.lock.acquire()
         try:
            self.stopped = 1
         finally:
            self.lock.release()

    #def read_detectors(self):
        #return(self.d.read_once1())