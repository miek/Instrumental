# -*- coding: utf-8  -*-
"""
Driver for HP Spectrum Analyzers
"""

from . import SpectrumAnalyzer
from .. import VisaMixin, SCPI_Facet
import numpy as np
import re

def _check_visa_support(visa_rsrc):
    visa_rsrc.read_termination = '\n'
    visa_rsrc.write_termination = '\n'

    try:
        idn_response = visa_rsrc.query('*IDN?')
    except:
        return None

    model = idn_response.split(',')[1]
    if re.match('^N932[1234]C$', model):
        return 'N932xC'
    else:
        return None


class N932xC(SpectrumAnalyzer, VisaMixin):
    _INST_PARAMS_ = ['visa_address']

    def _initialize(self):
        self._rsrc.read_termination = '\n'
        self._rsrc.write_termination = '\n'
        self._rsrc.timeout = 5000

    # Frequency
    center  = SCPI_Facet(':SENS:FREQ:CENT', units='Hz', convert=float)
    span    = SCPI_Facet(':SENS:FREQ:SPAN', units='Hz', convert=float)
    start   = SCPI_Facet(':SENS:FREQ:START', units='Hz', convert=float)
    stop    = SCPI_Facet(':SENS:FREQ:STOP', units='Hz', convert=float)

    reference = SCPI_Facet(':DISP:WIND:TRAC:Y:RLEV', units='dBm', convert=float)

    # Sweep
    sweep_time = SCPI_Facet(':SWE:TIME', units='s', convert=float)

    # Bandwidth
    vbw = SCPI_Facet(':BAND:VID', units='Hz', convert=float)
    rbw = SCPI_Facet(':BAND', units='Hz', convert=float)

    def get_trace(self, trace=1):
        """Get the given trace number

        Returns a tuple (frequencies, power)

        """
        if trace not in (1, 2, 3, 4):
            raise ValueError

        data_string = self.query(f':TRAC? TRACE{trace}')
        power = np.array(data_string.split(',')).astype(float)
        frequency = np.linspace(self.start.m, self.stop.m, len(power))
        return frequency, power
