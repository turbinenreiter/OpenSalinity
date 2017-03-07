import pyb
from SalSense8 import SalSens8

pyb.LED(2).on()
sal_sens = SalSens8(i2c=pyb.I2C(1, pyb.I2C.MASTER),
                    mec_addr=pyb.I2C(1, pyb.I2C.MASTER).scan()[0])

def loop(delay=100):
    start = pyb.micros()
    while True:
        sal_sens.pretty_print(start)
        pyb.delay(delay)

loop(delay=0)
