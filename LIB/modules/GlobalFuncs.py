# -*- coding: utf-8 -*-
from pygame import display
from sys import exit as SYSEXIT

def check_user_monitor():
    MAX_RESOLUTION = (display.Info().current_w-70, display.Info().current_h-60)
    avail_x = [i for i in (1820, 1250, 1200) if i < MAX_RESOLUTION[0]]
    avail_y = [i for i in (1000, 950, 700) if i < MAX_RESOLUTION[1]]
    if avail_x and avail_y:
        return (avail_x, avail_y)
    else:
        print("Your monitor has too small resolution! We can't provide a good interface for it :(")
        SYSEXIT()
