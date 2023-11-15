from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
import time

#Initialize max7219 devie
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

x_components =  [7,7,7,6,5,4,3,2,1,0,7,6,5,4,3,2,1,0,0,0]
y_components = [2,1,6,6,6,6,6,6,6,6,3,3,3,3,3,3,3,3,5,4]
while True:
    for x in range(len(x_components)):
        with canvas(device) as draw:
            draw.point((x_components[x],y_components[x]), fill="white")
            time.sleep(0.1)

        
        

        



