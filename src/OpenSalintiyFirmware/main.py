import pyb
from SalSense8 import SalSense8

if __name__ == "__main__":

    pyb.LED(2).on()

    sal_sens = SalSens8(i2c=pyb.I2C(1, pyb.I2C.MASTER), mec_addr=77)

    def loop(delay=100):
        start = pyb.micros()
        while True:
            sal_sens.pretty_print(start)
            pyb.delay(delay)

    loop(delay=0)
