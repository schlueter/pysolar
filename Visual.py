#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 21:03:22 2017

@author: cjct1g14
"""

import matplotlib
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

matplotlib.rc('font', **font)

nameM,xM,yM,zM,rM,vM = [], [], [], [], [], []
nameD,xD,yD,zD,rD,vD = [], [], [], [], [], []
nameMa,xMa,yMa,zMa,rMa,vMa = [], [], [], [], [], []
nameC,xC,yC,zC,rC,vC = [], [], [], [], [], []

import time
import numpy as np
import gc
from datetime import datetime
import imageio

def waitCounter():
    for i in range(1, 6):
        print("\rWaiting for Location File %d"%(i), end = "")
        time.sleep(1)
    return None

def openFile(Name):
    while True:
        try:
            File = open(Name, "r")
            return File
        except:
            waitCounter()
            pass    

def run():
    import LocationCalc
    nameM,xM,yM,zM,rM,vM = [], [], [], [], [], []
    nameD,xD,yD,zD,rD,vD = [], [], [], [], [], []
    nameMa,xMa,yMa,zMa,rMa,vMa = [], [], [], [], [], []
    nameC,xC,yC,zC,rC,vC = [], [], [], [], [], []
    gc.collect()
    time.sleep(5)
    file = openFile("Positions.txt")
    fileOpen = file.readlines()
    print("\r                                                         ",end="")
    lengthFile = len(fileOpen)
    for counter, line in enumerate(fileOpen[1::]):
        line = line.split(",")
        NAME = line[0]
        X = float(line[2])
        Y = float(line[3])
        Z = float(line[4])
        R = float(line[5])
        V = float(line[6])
        if line[1] == "Minor Planet":
            xM.append(X); yM.append(Y); zM.append(Z)
            nameM.append(NAME); rM.append(R); vM.append(V)
        if line[1] == "Dwarf Planet":
            xD.append(X); yD.append(Y); zD.append(Z)
            nameD.append(NAME); rD.append(R); vD.append(V)
        if line[1] == "Major Planet":
            xMa.append(X); yMa.append(Y); zMa.append(Z)
            nameMa.append(NAME); rMa.append(R); vMa.append(V)
        if line[1] == "Comet":
            xC.append(X); yC.append(Y); zC.append(Z)
            nameC.append(NAME); rC.append(R); vC.append(V)
        percentage = int((counter/lengthFile)*100)
        print("\rReading File %d %%"%(percentage), end ="")
    
    import matplotlib.pyplot as plt
    
    def frameRateCalc(fps, time):
        frameTime = 1/fps
        rangeList = []
        frames = fps*time
        maxR = max(rM + rD + rMa + rC) * 1.1
        minR = min(rM + rD + rMa + rC) * 0.9
        a = (np.log(maxR) - np.log(minR))/frames
        frameList = np.linspace(0, frames, frames)
        for i in frameList:
            rangeList.append(minR*np.exp(a*i))
        return rangeList, frameTime
    
    greg = datetime.utcnow()
    Year, Month, Day = greg.year, greg.month, greg.day
    timeNow = "UTC: %d/%d/%d"%(Year, Month, Day)
    
    startTime = time.time()
    frameRange, frameTime = frameRateCalc(frameRate, playTime)
    count = 1
    for j in frameRange:
        plt.figure(figsize=((1920*4)/100, (1080*4)/100), dpi=100)
        ax = plt.subplot(111, projection='polar')
        ax.set_facecolor('black')
        ax.set_ylim([0, j])
        ax.scatter(vM, rM, s=4, c = 'blue', lw=0, alpha=.7, label = "Minor")
        ax.scatter(vMa, rMa, s=40, c = 'r', lw=0, label = "Major")
        ax.scatter(vD, rD, s=30, c = 'yellow',lw=0, label = "Dwarf")
        ax.scatter(vC, rC, s=4, c = 'g',lw=0, alpha=.7, label = "Comet")
        ax.text(0.0, 1, timeNow, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', color = 'black')
        ax.text(0.0, 0.95, "Frame %d of %d"%(count, len(frameRange)), transform=ax.transAxes, fontsize=8,
        verticalalignment='bottom', color = 'black')
        ax.set_ylabel("Heliocentric Distance (au)", color = 'black')
        ax.xaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(True)
        plt.savefig("Frames/Location%d.png"%count, dpi = 100)
        plt.close()
        TimeEl = time.time() - startTime
        AvTime = TimeEl/count
        TimeLeft = (len(frameRange) - count)*AvTime
        print("\r%d Frames Rendered from %d, %.2f Hours Left, Range %.2f"%(count, len(frameRange), TimeLeft/(60*60), j), end = "")
        count += 1
    plt.close()
    
    print("\r                                                            ",end="")
    
    
    startTime = time.time()
    writer = imageio.get_writer('Frames4k/Movie.mp4', fps=frameRate)
    for i in range(1,count):
        TimeEl = time.time() - startTime
        AvTime = TimeEl/i
        filename = "Frames/Location%d.png"%i
        image = imageio.imread(filename)
        writer.append_data(image)
        TimeLeft = (3600 - count)*AvTime
        print("\r%d Frames To mp4, %.2f Hours Left"%(i, TimeLeft/(60*60)), end = "")
    writer.close()

    gc.collect()
    
    time.sleep(100)

def inputs():
    try:
        playTime = float(input("Playback Time (s): "))
        frameRate = float(input("Frame Rate  (s^-1): "))
        return playTime, frameRate
    except:
        print("Enter Integers Only")
        inputs()

playTime, frameRate = inputs()

while True:
    run()
