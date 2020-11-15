from PIL import Image#, ImageGrab
import pyscreenshot as ImageGrab
from time import time


import io
from colorthief import ColorThief


import os
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")
	
def screenshot(name, recording):
	im2 = ImageGrab.grab(bbox = None)
	
	
	if recording:
		im2.save(f'screenshots/{name}.png')
	
	
	b = io.BytesIO()
	im2.save(b, "PNG")
	b.seek(0)
	
	color_thief = ColorThief(b)
	dominant_color = color_thief.get_color(quality=1)
	
	return dominant_color
	
	
