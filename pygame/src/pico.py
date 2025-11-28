import machine
import time
import sys
import select
import random

pot = machine.ADC(26)

red = machine.PWM(machine.Pin(15))
green = machine.PWM(machine.Pin(14))
blue = machine.PWM(machine.Pin(13))

red.freq(1000)
green.freq(1000)
blue.freq(1000)

def set_color(r, g, b):
    red.duty_u16(r)
    green.duty_u16(g)
    blue.duty_u16(b)

CORES = [
    (65535, 0, 0),      
    (0, 65535, 0),      
    (0, 0, 65535),      
    (65535, 65535, 0), 
    (65535, 0, 65535), 
    (0, 65535, 65535),  
    (65535, 10000, 0)  
]

set_color(0, 0, 0) 

while True:
    pot_value = pot.read_u16()
    image_size = int(30 + (pot_value / 65535) * 270)
    print(f"SIZE:{image_size}")
    
    if select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        
        if cmd == "WIN":
           
            cor_escolhida = CORES[random.randint(0, len(CORES) - 1)]
            
            for _ in range(5):
                set_color(cor_escolhida[0], cor_escolhida[1], cor_escolhida[2])
                time.sleep(0.3)
                set_color(0, 0, 0)
                time.sleep(0.3)
            
            set_color(0, 0, 0)
            
        elif cmd == "OFF":
            set_color(0, 0, 0)
    
    time.sleep(0.05)
