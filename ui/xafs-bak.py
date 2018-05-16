
from os import path
from pydm import Display
from epics import Motor, PV
from bl09b import BL09BXAFS
import threading
import time




class XAFS(Display):
    def __init__(self, parent=None, args=[]):
        super(XAFS, self).__init__(parent=parent, args=args)
        self.ui.btnStart.clicked.connect(self.start)
        self.ui.btnStop.clicked.connect(self.stop)
        self.ui.btnPara.clicked.connect(self.set_parameter)
        self.m = Motor("IOC:m1")
        self.d = [PV("IOC:m1.RBV"), PV("417:aiExample")]
        self.energy_pv = [PV("X09B1:XAFS:Energy"+str(i)) for i in range(8)]
        self.step_pv = [PV("X09B1:XAFS:Step"+str(i)) for i in range(7)]
        self.itime_pv = [PV("X09B1:XAFS:ITime"+str(i)) for i in range(7)]
        
    def ui_filename(self):
        return 'xafs.ui'
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
    
    def start(self):
        energy = [self.energy_pv[i].get() for i in range(8)]
        step = [self.step_pv[i].get() for i in range(7)]
        itime = [self.itime_pv[i].get() for i in range(7)]
        self.myscan = BL09BXAFS(energy, step, itime, self.m, self.d)
        self.myscan.scan()
        self.ui.btnStart.setEnabled(False)
        t = threading.Thread(target=self.wait_finished, args=())
        t.start()
        
    def wait_finished(self):
        while(self.myscan.finished == 0 and self.myscan.stopped==0):
            time.sleep(1)
        self.ui.btnStart.setEnabled(True)
        
    def stop(self):
         self.myscan.stop()
         #self.ui.btnStart.setEnabled(True)
        
    def set_parameter(self):
        energy = [0, 2, 5, 8, 10, 15, 18, 20]
        step = [1, 1, 0.5, 0.5, 0.5, 1, 1]
        for i in range(8):
            self.energy_pv[i].put(energy[i])
        for i in range(7):
            self.step_pv[i].put(step[i])
            


x = XAFS()
