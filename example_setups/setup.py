

class setup:

    def __init__(self, frequency: list, amplitude: list) -> None:
        self.f = frequency
        self.amp = amplitude

    @property
    def amplitude(self):
        """

        :rtype: The amplitude in dBFS for the configuration
        :type self:
        """
        return self.amp

    @property
    def frequency(self):
        """

        :rtype: Frequency given in Hz as a number
        """
        return self.f
