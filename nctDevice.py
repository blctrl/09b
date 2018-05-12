from ophyd.status import *
from ophyd import EpicsSignal
import time as tt
class c(Device):
    clear_all = Cpt(Signal,value=111)
    clear_all.trigger_value=1
    start = Cpt(Signal,value=222)
    itime =  Cpt(Signal,value=3)
    read_once = Cpt(Signal,value=444)
    v0 =  Cpt(Signal,value=555)
    v1 =  Cpt(Signal,value=666)
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

        acq_signal.put(1, wait=True)
        self.start.put(11,wait=True)
        tt.sleep(self.itime.get())
        self.read_once.put(1,wait=True)
        self.v0.put(100)
        self.v1.put(200)
        
        self._done_acquiring()
        return status