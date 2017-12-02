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
backgroundFile = '/home/ruslan/python/SnowGen/P71118-135320(1).jpg'
maxHeigth      = 40
maxLongSide    = 1200

def loadSnowFlace():
    sa = []
    for file in glob.glob('./snowflace/*.png'):
        i = Image.open(file).resize((maxHeigth,maxHeigth))
        sa.append(i)
    return sa

def generateSnow(count,size):
    ret = []
    for i in range(count):
        id     = random.randint(0, len(snowArray)-1)
        #speed  = random.randint(1, 5)
        speed  = size
        x      = random.randint(10, width-10)
        y      = random.randint(-20, height)
        rotate = random.randint(0,360)
        ret.append({
            "img"   : snowArray[id].copy().resize((maxHeigth/speed,maxHeigth/speed)),
            "speed" : speed,
            "x"     : x, 
            "y"     : y, 
            "rotate": rotate,
        })
    return ret
    

snowArray = loadSnowFlace()

img     = Image.open(backgroundFile)
width   = img.size[0] 
height  = img.size[1] 
aw,ah=1,1
if width>maxLongSide:
    aw = float(maxLongSide) / width
if height>maxLongSide:
    ah = float(maxLongSide) / height
a      = min(aw,ah)
width  = int(width*a)
height = int(height*a)
img = img.resize((width,height))


height4 = float(height)*0.6
print(width,height)

maxSnowFlace = width / 8
maxFrame     = (height + maxHeigth) / 3 + 1
print(maxSnowFlace,maxFrame)
#exit()
#maxSnowFlace = 10

fallArray.extend(generateSnow(int(maxSnowFlace*0.20),1))
fallArray.extend(generateSnow(int(maxSnowFlace*0.15),2))
fallArray.extend(generateSnow(int(maxSnowFlace*0.15),3))
fallArray.extend(generateSnow(int(maxSnowFlace*0.20),4))
fallArray.extend(generateSnow(int(maxSnowFlace*0.30),5))

fps = 30
writer = imageio.get_writer('test.mp4', fps=fps)

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
        if s['speed'] > 3 and s['y'] > height4:
            s['y'] = -20

    frameArray = numpy.array(newFrame)
    writer.append_data(frameArray)
writer.close()


