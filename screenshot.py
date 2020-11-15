from PIL import Image#, ImageGrab
import pyscreenshot as ImageGrab
from time import time


import io
from colorthief import ColorThief


import os
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


ims = [None, None, None]

def screenshot(index):
	im2 = ImageGrab.grab(bbox = None)
	
	
	ims[index] = im2
	
	
	return True
	

def finalizeScreenshot(name):
	
	dst = Image.new('RGB', (ims[0].width, ims[0].height+ims[1].height+ims[2].height))	
	dst.paste(ims[0], (0,0))
	dst.paste(ims[1], (0, ims[0].height))
	dst.paste(ims[2], (0, ims[0].height+ims[1].height))
	
	
	if name is not None:
		dst.save(f'screenshots/{name}.png')
	
	b = io.BytesIO()
	dst.save(b, "PNG")
	b.seek(0)
	
	color_thief = ColorThief(b)
	dominant_color = color_thief.get_color(quality=1)
	
	return dominant_color
