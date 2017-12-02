#!/usr/bin/python
# -*- coding: utf-8 -*-

# http://imageio.readthedocs.io/en/latest/userapi.html

import imageio
from PIL import Image,ImageChops,ImageDraw
import numpy
import os, glob,random,math

snowArray      = None
maxSnowFlace   = 1
maxFrame       = 1
fallArray      = []
backgroundFile = '/home/ruslan/Рабочий стол/Transfer/004.Проекты/проекты/jpg2gif/002.jpg'

def loadSnowFlace():
    sa = []
    for file in glob.glob('./snowflace/*.png'):
        i = Image.open(file).resize((40,40))
        sa.append(i)
    return sa

snowArray = loadSnowFlace()

img    = Image.open(backgroundFile)
width  = img.size[0] 
height = img.size[1] 
print(width,height)

maxSnowFlace = width / 10
maxFrame     = (height + 40) / 3 + 1
print(maxSnowFlace,maxFrame)
#exit()
#maxSnowFlace = 10

for i in range(maxSnowFlace):
    id     = random.randint(0, len(snowArray)-1)
    speed  = random.randint(1, 5)
    x      = random.randint(10, width-10)
    y      = random.randint(-20, height)
    rotate = random.randint(0,360)
    fallArray.append({
        "img"   : snowArray[id].copy().resize((40/speed,40/speed)),
        "speed" : speed,
        "x"     : x, 
        "y"     : y, 
        "rotate": rotate,
    })

fps = 24
writer = imageio.get_writer('test.gif', fps=fps)

for frame in range(maxFrame):
    print("Frame %s of %s" % (frame,maxFrame))
    newFrame = img.copy()
    for s in fallArray:
        s['y']      = s['y']+s['speed']*3
        w = s['img'].size[0] 
        h = s['img'].size[1]
        r = float(s['y']) / height * 360 * s['speed'] + s['rotate']

        #s['rotate'] = s['rotate']+s['speed']*3
        #if s['rotate'] > 360: s['rotate'] = s['rotate'] - 360
        
        ah = int(h / 2)
        
        if (r//90) % 2 == 0:
            h  = int(round(ah + ah*(float(r % 90) / 90)))
        else:
            h  = int(round(ah*2 - ah*(float(r % 90) / 90)))

        #print(s['y'],s['rotate'])
        #ax = int(20*math.sin(math.radians(s['rotate'])))
        ax = int(30/s['speed']*math.sin(math.radians(r)))
        
        newFrame.paste(s['img'].resize((h,w)).rotate(r, expand=True), (s['x']+ax, s['y']), s['img'].resize((h,w)).rotate(r, expand=True))
        if s['y'] > (height+20):
            s['y'] = -20

    frameArray = numpy.array(newFrame)
    writer.append_data(frameArray)
writer.close()


