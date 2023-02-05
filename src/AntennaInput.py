#import .BaseInput
import numpy as np

class AntennaInput:
    """#- - - ANTENNA INPUT PARAMETERS - - -
#
#   TAG   SEG.    VOLTAGE (VOLTS)         CURRENT (AMPS)         IMPEDANCE (OHMS)        ADMITTANCE (MHOS)      POWER
#   NO.   NO.    REAL        IMAG.       REAL        IMAG.       REAL        IMAG.       REAL        IMAG.     (WATTS)
#     0 *   5 1.00000E+00 0.00000E+00 6.64451E-03-3.86651E-03 1.12429E+02 6.54238E+01 6.64451E-03-3.86651E-03 3.32225E-03
#
#                       --------- ANTENNA INPUT PARAMETERS ---------
#  TAG   SEG       VOLTAGE (VOLTS)         CURRENT (AMPS)         IMPEDANCE (OHMS)        ADMITTANCE (MHOS)     POWER
#  NO.   NO.     REAL      IMAGINARY     REAL      IMAGINARY     REAL      IMAGINARY    REAL       IMAGINARY   (WATTS)
#    0     5  1.0000E+00  0.0000E+00  6.6443E-03 -3.8666E-03  1.1243E+02  6.5428E+01  6.6443E-03 -3.8666E-03  3.3222E-03

    Read antenna inputs as formatted above.
    Assume the file might have multiples of these records
    """

    def __init__(self):
        self.n_items = 0
        self.ant_inputs = []

    def ingest_records(self, lines):
        startcue = "ANTENNA INPUT PARAMETERS"
        endcue = "(WATTS)"
        reading_header=False
        reading_inputs=False
        for thisline in lines:
            if startcue in thisline:
                reading_header=True
            
            if endcue in thisline:
                reading_header=False
                reading_inputs=True

            if reading_inputs:
                splitput = thisline.split()
                if len(splitput)!=9:
                    print('Warning: input line incorrect length')          
                self.ant_inputs.append(AntennaInput(thisline))
                self.n_items += 1
    
    def _as_matrix(self):
        themat=[xx._asvect() for xx in self.ant_inputs]
        return np.array(themat)

    def __dif__(self, other):
        if self.n_items != other.n_items:
            return None
        else:
            thediffs = self._as_matrix() - other._as_matrix()
            return np.sum(thediffs)

    def __eq__(self, other):
        if self._as_matrix() == other._as_matrix():
            return True
        else:
            return False   
    
    def equalto(self, other): # ported from original
        if max(self-other) < 1e-4:
            return True
        else:
            return False          


class AntennaInputRow:
    def __init__(self, thestr):
        self.datastring = thestr
        self._parse_antenna_data_line(self.datastring)

    def _parse_antenna_data_line(self, thestr):
        dp=str.split(thestr.replace('*',''))

        self.tag =  float(dp[0])
        self.seg =  float(dp[1])
        self.vRe =  float(dp[2])
        self.vIm =  float(dp[3])
        self.iRe =  float(dp[4])
        self.iIm =  float(dp[5])
        self.zRe =  float(dp[6])
        self.zIm =  float(dp[7])
        self.power= float(dp[8])

    def _asvect(self):
        thevect = np.array([self.tag,
                            self.seg,
                            self.vRe,
                            self.vIm,
                            self.iRe,
                            self.iIm,
                            self.zRe,
                            self.zIm,
                            self.power])
        return thevect
                    
    def __eq__(self, other):
        if self._asvect() == other._asvect():
            return True
        else:
            return False

    def __sub__(self, other):
        thediff = self._asvect() - other._asvect()
        return thediff

