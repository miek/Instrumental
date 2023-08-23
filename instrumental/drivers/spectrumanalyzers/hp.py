# -*- coding: utf-8  -*-
"""
Driver for HP Spectrum Analyzers
"""

from . import SpectrumAnalyzer
from .. import VisaMixin, SCPI_Facet
import numpy as np

def _check_visa_support(visa_rsrc):
    try:
        model = visa_rsrc.query('ID?')
    except:
        return None
    supported_models = [
            'HP8561E', 'HP8561EC',
            'HP8562E', 'HP8562EC',
            'HP8563E', 'HP8563EC',
            'HP8564E', 'HP8564EC',
            'HP8565E', 'HP8565EC',
    ]
    if model.rstrip() in supported_models:
        return 'HP856x'
    else:
        return None

class HP856x(SpectrumAnalyzer, VisaMixin):
    _INST_PARAMS_ = ['visa_address']

    def _initialize(self):
        self._rsrc.read_termination = '\n'
        self._rsrc.write_termination = '\n'
        self._rsrc.timeout = 5000

    center = SCPI_Facet('CF', units='Hz', convert=float)
    span = SCPI_Facet('SP', units='Hz', convert=float)
    start = SCPI_Facet('FA', units='Hz', convert=float)
    stop = SCPI_Facet('FB', units='Hz', convert=float)
    reference = SCPI_Facet('RL', convert=float)
    sweep_time = SCPI_Facet('ST', units='s', convert=float)
    vbw = SCPI_Facet('VB', units='Hz', convert=float)
    rbw = SCPI_Facet('RB', units='Hz', convert=float)
    averages = SCPI_Facet('VAVG', convert=int)

    def get_trace(self, channel='A'):
        """Get the trace for a given channel

        Returns a tuple (frequencies, power)

        """
        if channel == 'A':
            command = 'TRA?'
        elif channel == 'B':
            command = 'TRB?'
        else:
            raise ValueError

        data_string = self.query(command)
        power = np.array(data_string.split(',')).astype(float)
        frequency = np.linspace(self.start.m, self.stop.m, len(power))
        return frequency, power
