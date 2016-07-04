from struct import unpack as unp
import pyb

class SalSens8:
    '''
    SalSens8 implements reading salinity measurements from an ueC Interface
    combined with 2 Matrix Switches. The Matrix Switch allows to connect 8
    electrodes to 1 ueC Interface.
    '''

    def __init__(self, i2c=pyb.I2C(1, pyb.I2C.MASTER), mec_addr=79):
        '''
        initializes the ueC Interface and Matrix Switches
        i2c = I2C bus
        mec_addr = I2C address of the ueC Interface ADC
        '''

        self.MEC_ADDR = mec_addr

        self.bus_i2c = i2c
        self.sync = pyb.Pin('B1', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.sync.high()
        self.sck = pyb.Pin('A5', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.sck.high()
        self.mosi = pyb.Pin('A7', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.mosi.low()
        self.reset = pyb.Pin('B10', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
        self.reset.high()

    def read_sal(self):
        '''
        reads the ADC and returns an int between 0 and 4096
        '''
        return unp('>h', self.bus_i2c.recv(2, self.MEC_ADDR))[0]

    def switch_to(self, sw):
        '''
        switches to sw and returns sw
        '''

        self.reset.low()
        self.reset.high()

        self.sync.low()

        for i in range(1,9):
            if i == 9-sw: self.mosi.high()
            self.sck.low()
            self.mosi.low()
            self.sck.high()

        self.sync.high()

        return sw

    def read_sal_from(self, sw):
        '''
        switches to sw, reads ADC and returns int between 0 and 4096
        '''
        self.switch_to(sw)
        return self.read_sal()

    def read_sal_from_all(self, start):
        '''
        switches to and reads ADC for all, returns one tuple with the times
        of reads in us and values between 0 and 4096
        '''
        times = [0]*8
        values = [0]*8
        for i in range(1, 9):
            times[i-1] = pyb.micros() -start
            values[i-1] = self.read_sal_from(i)
        return times, values

    def pretty_print(self):
        '''
        pretty print
        format:
        te1 e1 te2 e2 .. te8 e8
        '''
        times, values = self.read_sal_from_all(pyb.micros())
        for (time, value) in zip(times, values):
            print(time, value, end=' ')
        print()

if __name__ == "__main__":

    sal_sens = SalSens8(i2c=pyb.I2C(1, pyb.I2C.MASTER), mec_addr=79)

    def loop(delay=100):
        while True:
            sal_sens.pretty_print()
            pyb.delay(delay)
