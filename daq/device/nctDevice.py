from ophyd.status import *
from ophyd import Device, Signal,Component as Cpt
from ophyd.status import *
from ophyd import EpicsSignal
import time as tt
from epics import caget, caput

class Nct(Device):
    '''prfix = X09B1:EH:NCT:'''
    clear_all = Cpt(EpicsSignal,'ClearAll.PROC')
    clear_all.trigger_value=1
    
    #clearAll = 
    start = Cpt(EpicsSignal,'Start.PROC')
    itime =  Cpt(EpicsSignal,'TimerPreset')
    read_once = Cpt(EpicsSignal,'readonce.PROC')
    ch0_proc = Cpt(EpicsSignal,'CH0.PROC')
    ch1_proc = Cpt(EpicsSignal,'CH1.PROC')
    ch0 = Cpt(EpicsSignal,'CH0')
    ch1 = Cpt(EpicsSignal,'CH1')
    v0 =  Cpt(EpicsSignal,'V0')
    v1 =  Cpt(EpicsSignal,'V1')
    def nctproc(self):
        itime = self.itime.get()
        print(itime)
        #self.ch0_proc.set(1,settle_time=0.1)
        caput('X09B1:EH:NCT:'+'CH0.PROC',1,wait = True)
        caput('X09B1:EH:NCT:'+'CH1.PROC',1,wait = True)
        #self.ch1_proc.set(1,settle_time=0.1)
        c0 = self.ch0.get()
        c1 = self.ch1.get()
        print(c0)
        print(c1)
        vv0 = c0/(itime*1e5)
        vv1 = c1/(itime*1e5)
        self.v0.set(vv0)
        self.v1.set(vv1)
        
    def trigger(self):
        """Start acquisition"""
        signals = self.trigger_signals
        if len(signals) > 1:
            raise NotImplementedError('More than one trigger signal is not '
                                      'currently supported')
        status = DeviceStatus(self)
        if not signals:
            status._finished()
            return status

        acq_signal, = signals

        self.subscribe(status._finished,
                       event_type=self.SUB_ACQ_DONE, run=False)
        def done_acquisition(**ignored_kwargs):
        #def done_acquisition():
            # Keyword arguments are ignored here from the EpicsSignal
            # subscription, as the important part is that the put completion
            # has finished
            print(222)
            self._done_acquiring()

        #acq_signal.set(1,settle_time=0.1)
        caput('X09B1:EH:NCT:'+'ClearAll.PROC',1,wait = True)
        caput('X09B1:EH:NCT:'+'Start.PROC',1,wait = True)
        #self.read_once.put(1)
        #self.start.set(1,settle_time=0.1)
        itime = self.itime.get()
        #print(itime)
        tt.sleep(itime)
        self.nctproc()
        #self.read_once.set(1,settle_time=0.1)
        #self.read_once.set(1,settle_time=0.1)
        #self.v0.put(100)
        #self.v1.put(200)
        
        self._done_acquiring()
        return status
