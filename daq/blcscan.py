
import time
import threading

class BLCScan1(object):
    """
    1d step by step scan
    one motor, multiple detectors
    DATE: 2018-5

    m: motor, Motor object
    d: detectors, PV object list
    step > 0
    """
    def __init__(self, start, step, end, m, d):
        self.start = start
        self.step = step
        self.end = end
        self.m = m
        self.d = d
        self.init()
        
    def init(self):
        # number of scan points
        self.npts = self.get_npts()
        # number of detectors
        self.dn = len(self.d)
        self.mRA = [0 for i in range(self.npts)]
        self.dRA = [[0 for i in range(self.npts)] for j in range(self.dn)]
        self.stopped = 0
        self.finished = 0
        self.settlingTime = 0
        self.lock = threading.Lock()

    # get number of points
    def get_npts(self):
        return int(abs(self.end-self.start)/self.step)+1

    # get scan position array
    def get_pos(self):
        pos = []
        if self.end<self.start:        # reverse direction
            self.step = -self.step
        for i in range(self.npts):
            pos.append(self.start+self.step*i)
        return pos

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
        pos = self.get_pos()
        for i in range(self.npts):
            if self.stopped == 1:
                break
            self.move_motor(pos[i])
            self.mRA[i] = self.read_motor()
            # detector value list @ current scan position
            dvs = self.read_detectors()
            for j in range(len(dvs)):
                self.dRA[j][i] = dvs[j]

    def move_motor(self, value):
        self.m.put('DVAL', value, wait=True)
        while self.m.get('MOVN')==1:
            time.sleep(1)

    def read_motor(self):
        time.sleep(self.settlingTime)
        return self.m.get('DRBV')

    def read_detectors(self):
        tmp = [self.d[i].get() for i in range(self.dn)]
        return tmp
    
    def set_settlingTime(self, t):
        self.settlingTime = t

    def stop(self):
         self.lock.acquire()
         try:
            self.stopped = 1
         finally:
            self.lock.release()






class BLCScan1a(object):
    """
    1d position-array scan
    one motor, multiple detectors
    DATE: 2018-5
    
    m: motor, Motor object
    d: detectors, PV object list
    pos: position list
    """
    def __init__(self, pos, m, d):
        self.pos = pos
        self.m = m
        self.d = d
        self.init()
    
    def init(self):
        # number of scan points
        self.npts = self.get_npts()
        # number of detectors
        self.dn = len(self.d)
        self.mRA = [0 for i in range(self.npts)]
        self.dRA = [[0 for i in range(self.npts)] for j in range(self.dn)]
        self.stopped = 0
        self.finished = 0
        self.settlingTime = 0
        self.lock = threading.Lock()
    
    # get number of points
    def get_npts(self):
        return len(self.pos)
    
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
        for i in range(self.npts):
            if self.stopped == 1:
                break
            self.move_motor(self.pos[i])
            self.mRA[i] = self.read_motor()
            # detector value list @ current scan position
            dvs = self.read_detectors()
            for j in range(len(dvs)):
                self.dRA[j][i] = dvs[j]

    def move_motor(self, value):
        self.m.put('DVAL', value, wait=True)
        while self.m.get('MOVN')==1:
            time.sleep(1)

    def read_motor(self):
        return self.m.get('DRBV')

    def read_detectors(self):
        tmp = [self.d[i].get() for i in range(self.dn)]
        return tmp
    
    def set_settlingTime(self, t):
        self.settlingTime = t

    def stop(self):
         self.lock.acquire()
         try:
            self.stopped = 1
         finally:
            self.lock.release()



