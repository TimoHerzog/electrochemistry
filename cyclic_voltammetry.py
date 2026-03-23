import numpy as np

# Define a class representing a single Cyclic Voltammetry (CV) dataset
class CV:
    def __init__(self, volts, amps):
        # volts: array of potential values (in Volts)
        # amps: array of current values (in Amperes)
        if volts.ndim != 1 or amps.ndim != 1 or volts.shape != amps.shape:
            raise ValueError("volts and amps must be 1d numpy arrays of same size")

        self.volts = volts
        self.amps = amps


    def getPotentialAt(self, current: float, maxCurrentDist: float = 0.01) -> float:
        """
        Returns the potential (voltage) value that corresponds most closely 
        to a given current value.
        """
        ampsDiffs = np.abs(self.amps - current)        # Difference between each current and the target
        closestAmpsIndex = np.argmin(ampsDiffs)        # Find the index of the closest current value

        if np.abs(self.amps[closestAmpsIndex] - current) >= maxCurrentDist + 1e-5:  # check if current value is close enough
            raise ValueError("No current value is close enough")

        return self.volts[closestAmpsIndex]
    

    def getCurrentAt(self, voltage: float, maxVoltageDist: float = 0.01) -> float:
        """
        Returns the current value that corresponds most closely to a given voltage.
        """
        voltDiffs = np.abs(self.volts - voltage)
        closestVoltIndex = np.argmin(voltDiffs)

        if np.abs(self.volts[closestVoltIndex] - voltage) >= maxVoltageDist + 1e-5:  # check if current value is close enough
            raise ValueError("No voltage value is close enough")
        
        return self.amps[closestVoltIndex]
    

    def iRCompensate(self, resistance):
        """
        Applies iR compensation to correct for potential drop due to internal resistance.
        New voltage = measured voltage - (resistance * current)
        """
        
        if resistance < 0:
            raise ValueError("iR compensation resistance cannot be negative")

        compensatedVolts = self.volts - resistance * self.amps
        return CV(compensatedVolts, self.amps)
    
    
    def shiftPotential(self, offsetPotential: float):
        """
        Shifts the entire potential (voltage) curve by a given overpotential value.
        Returns a new CV object with adjusted voltages.
        """
        corrected_potential = np.array(self.volts) + offsetPotential
        return CV(corrected_potential, self.amps)

    def afterLeftVertex(self):
        """
        Returns a subset of the datapoints starting from the left vertex
        """
        vertexIndex = np.argmin(self.volts)

        if vertexIndex == len(self.volts)-1:
            raise ValueError("Left vertex is at end of CV scan")
        
        if np.count_nonzero(self.volts == self.volts[vertexIndex]) > 1:
            raise ValueError("Left vertex is ambiguous")
        
        return CV(self.volts[vertexIndex:], self.amps[vertexIndex:])

    def beforeLeftVertex(self):
        """
        Returns a subset of the datapoints up to the left vertex

        """
        vertexIndex = np.argmin(self.volts)

        if vertexIndex == 0:
            raise ValueError("Left vertex is at beginning of CV scan")
        
        if np.count_nonzero(self.volts == self.volts[vertexIndex]) > 1:
            raise ValueError("Left vertex is ambiguous")
        
        return CV(self.volts[:(vertexIndex+1)], self.amps[:(vertexIndex+1)])
    
    def afterRightVertex(self):
        """
        Returns a subset of the datapoints up to the right vertex
        """
        vertexIndex = np.argmax(self.volts)

        if vertexIndex == len(self.volts)-1:
            raise ValueError("Right vertex is at end of CV scan")
        
        if np.count_nonzero(self.volts == self.volts[vertexIndex]) > 1:
            raise ValueError("Right vertex is ambiguous")

        return CV(self.volts[vertexIndex:], self.amps[vertexIndex:])

    def beforeRightVertex(self):
        """
        Returns a subset of the datapoints starting from the right vertex
        """
        vertexIndex = np.argmax(self.volts)
        return CV(self.volts[:(vertexIndex+1)], self.amps[:(vertexIndex+1)])