from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
import time

#Initialize max7219 devie
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

max_matrix_sleep_seconds = 0.01
max_matrix_start_position = 0


while True:
    for trailing_count in range(8):
            with canvas(device) as draw:
                #IR Display
                for x in range(7,0,-1):
                    draw.point((x,7), fill = "white")
                    draw.point((x,6), fill = "white")
                    draw.point((x,5), fill = "white")
                    draw.point((x,4), fill = "white")
                    draw.point((x,3), fill = "white")
                    draw.point((x,2), fill = "white")
                    draw.point((x,1), fill = "white")
                    draw.point((x,0), fill = "white")


                #Motor Display
                draw.point((max_matrix_start_position,trailing_count), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-1), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-2), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-3), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-4), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-5), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-6), fill="white")
                time.sleep(max_matrix_sleep_seconds)
                draw.point((max_matrix_start_position,trailing_count-7), fill="white")
                time.sleep(max_matrix_sleep_seconds)
         
    


        
        

        



