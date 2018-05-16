
from os import path
from pydm import Display
import threading
from bl09b import BL09BNCT


class BeamMonitor(Display):
    def __init__(self, parent=None, args=[]):
        super(BeamMonitor, self).__init__(parent=parent, args=args)
        self.ui.BtnMonitor.clicked.connect(self.start_monitor)
        self.ui.BtnStop.clicked.connect(self.stop)
        self.stopped = 0
        self.nct = BL09BNCT("X09B1:EH:NCT")
        self.nct.set_itime(1)
        self.lock = threading.Lock()

    def ui_filename(self):
        return 'beamMonitor.ui'
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
    
    def start_monitor(self):
        t = threading.Thread(target=self.monitor, args=())
        t.start()
        
    def monitor(self):
        self.lock.acquire()
        try:
            self.stopped = 0
        finally:
            self.lock.release()
        while(1):
            if(self.stopped == 1):
                break
            else:
                self.nct.read_once()
                
    def stop(self):
        self.lock.acquire()
        try:
            self.stopped = 1
        finally:
            self.lock.release()            

bm09b = BeamMonitor()


