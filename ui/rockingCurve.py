
from os import path
from pydm import Display
from epics import Motor, PV, caget
from bl09b import ScanRC, BL09BNCT
import time
import threading


class RockingCurve(Display):
    def __init__(self, parent=None, args=[]):
        super(RockingCurve, self).__init__(parent=parent, args=args)
        self.ui.btnStart.clicked.connect(self.start_rc)
        self.ui.btnStop.clicked.connect(self.stop)
        #self.ui.pushButton.clicked.connect(self.tmp)
        self.m = Motor("IOC:m1")
        #self.d = [PV("IOC:m1.RBV"), PV("417:aiExample")]
        self.d = [BL09BNCT("X09B1:EH:NCT")]

    #def tmp(self):
        #a = self.ui.plotI0.getCurves()
        #print(a)
        #b = self.ui.plotI0.clearCurves()
        #print(a)
        #c = self.ui.plotI0.setCurves(a)
        #print(c)
        #self.ui.plotI0.clear()
        #self.repaint()
        #self.close()
        #self.clearMask()
        #chs=self.ui.plotI0.channels()
        #print(dir(chs))
        #self.ui.plotI0.removeChannelAtIndex(0)
        #self.ui.plotI0.addChannel('IOC:m1.DRBV','IOC:m1.DRBV')
        
        #dtbf = self.ui.plotI0.data_buffer
        #self.ui.plotI0.data_buffer = dtbf*0
        #print(self.ui.plotI0.channel_pairs[('IOC:m1.DRBV','IOC:m1.DRBV')].data_buffer[0])
        #print(self.ui.plotI0.channel_pairs[('IOC:m1.DRBV','IOC:m1.DRBV')].data_buffer[1])
        #self.ui.plotI0.channel_pairs[('IOC:m1.DRBV','IOC:m1.DRBV')].data_buffer *=0
        #self.ui.plotI0.updateAxes()
        


    
    def ui_filename(self):
        return 'rockingCurve.ui'
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
    
    def start_rc(self):
        start = caget("X09B1:RC:Start")
        step = caget("X09B1:RC:Step")
        end = caget("X09B1:RC:End")
        t = caget("X09B1:RC:SettlingTime")
        #self.ui.plotI0.minXRange = start-1
        #self.ui.plotI0.maxXRange = end+1
        self.myscan = ScanRC(start, step, end, self.m, self.d)
        self.myscan.set_settlingTime(t)
        self.myscan.scan()
        self.ui.btnStart.setEnabled(False)
        t = threading.Thread(target=self.wait_finished, args=())
        t.start()
        
    def wait_finished(self):
        while(self.myscan.finished == 0 and self.myscan.stopped==0):
            time.sleep(1)
        self.ui.btnStart.setEnabled(True)
        if self.ui.fileName.text() == "":
            fn = time.asctime() 
        else:
            fn = self.ui.fileName.text()
        fn = "/home/bl09b1/daq-data/"+fn
        self.myscan.save_data(fn)
        
    def stop(self):
        self.myscan.stop()

rc = RockingCurve()
