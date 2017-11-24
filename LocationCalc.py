#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 16:39:12 2017

@author: cjct1g14
"""

au = 1.496e+11

import numpy as np
import gc
import time


def MAcheck(MA):
    while True:
        if MA >= 360*2:
            divFac = int((MA/360))
            MA /= float(divFac)
        if MA >= 360:
            MA -= 360
        if MA < 0:
            MA += 360
        if (MA <= 360) and (MA >= 0):
            return MA

def waitCounter():
    for i in range(1, 6):
        print("\rWaiting for Orbit File %d"%(i), end = "")
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
    gc.collect()
    print("\r                                ", end = "")
    dataset = []
    File = openFile("SolarSystemO.txt")
    FileRead = File.readlines()
    count = 1
    per = 0
    length = len(FileRead)
    for line in FileRead[1::]:
        line = line.split(",")
        Name = str(line[0])
        if Name == "Sol":
            GMSol = float(line[10])
            continue
        Type = str(line[1])
        Parent = str(line[2])
        try:
            a = float(line[3]) * au
        except:
            a = np.inf
        e = float(line[4])
        i = np.radians(float(line[5]))
        AoP = np.radians(float(line[6]))
        LoAN = np.radians(float(line[7]))
        Epoch = float(line[8])
        MA0 = float(line[9])
        MA0 = np.radians(MAcheck(MA0))
        dataset.append([Name,Type,Parent,a,e,i,AoP,LoAN,Epoch,MA0])
        per1 = int((count/length)*100)
        if per1 != per:
            print("\r Reading File",per1,"%",end="")
        per = per1
        count += 1
    
    File.close()
    
    dataset = np.array(dataset)
    
    def NewtonRaphson(MA, e):
        EA = MA
        while True:
            EA1 = EA - (EA-e*np.sin(EA)-MA)/(1-e*np.cos(EA))
            EAdiff = abs(EA1-EA)
            if EAdiff <= 0.0001:
                return EA1
            EA = EA1
    
    #https://downloads.rene-schwarz.com/download/M001-Keplerian_Orbit_Elements_to_Cartesian_State_Vectors.pdf
    
    def locations(t):
        length = len(dataset)
        print("\r                                ", end = "")
        count = 1
        per = 0
        for obj in dataset:
            try:
                Name, Type = obj[0], obj[1]
                a = float(obj[3])
                if a == np.inf:
                    continue
                e = float(obj[4])
                i = float(obj[5])
                AoP = float(obj[6])
                LoAN = float(obj[7])
                MA0 = float(obj[9])
                dt = 86400*(t-float(obj[8]))
                MA = MA0 + dt*np.sqrt(GMSol/(a**3.))
                MA = np.radians(MAcheck(np.degrees(MA)))
                EA = NewtonRaphson(MA, e)
                VA = 2*(np.arctan2(np.sqrt(1+e)*np.sin(EA/2.), np.sqrt(1-e)*np.cos(EA/2.)))
                r = a*(1-e*np.cos(EA))
                ox, oy = r*np.cos(VA), r*np.sin(VA)
                x = ox*(np.cos(AoP)*np.cos(LoAN) - np.sin(AoP)*np.cos(i)*np.sin(LoAN)) - oy*(np.sin(AoP)*np.cos(LoAN) + np.cos(AoP)*np.cos(i)*np.sin(LoAN))
                y = ox*(np.cos(AoP)*np.sin(LoAN) + np.sin(AoP)*np.cos(i)*np.cos(LoAN)) + oy*(np.cos(AoP)*np.cos(i)*np.cos(LoAN) - np.sin(AoP)*np.sin(LoAN))
                z = ox*(np.sin(AoP)*np.sin(i)) + oy*(np.cos(AoP)*np.sin(i))
                objPos.append([Name, Type, x/au, y/au, z/au, r/au, VA])
                per1 = int((count/length)*100)
                if per1 != per:
                    print("\rCalculating Positions",per1,"%", end = "")
                per = per1
            except:
                pass
            count += 1
            
    
    def gregToJD(greg):
        Year, Month, Day, Hour, Minute, Second = greg
        a = int((14-Month)/12)
        y = Year + 4800 - a
        m = Month + 12*a - 3
        JDN = Day + int((153*m+2)/5) +365*y + int(y/4) - int(y/1000) + int(y/400) - 32045
        JD = JDN + (Hour-12)/24. + Minute/1440.0 + Second/86400
        return JD
    
    def dataWrite(List, File):
        fileopen = open(File, "w")
        output = ""
        for line in List:
            for item in line[0:-1]:
                output += (str(item) + ",")
            output += (str(line[-1]) + "\n")
        fileopen.write(output)
        fileopen.close()
    
    from datetime import datetime
    
    greg = datetime.utcnow()
    year, month, day, hour, minute, second = greg.year, greg.month, greg.day, greg.hour, greg.minute, greg.second
    
    objPos = ["Name,Type,X(au),Y(au),Z(au),OrbitalRadius(AU),TrueAnomaly(Rad)", ["Sol", "Star", 0, 0, 0, 0, 0]]
    JD = gregToJD((year, month, day, hour, minute, second))
    locations(JD)
    dataWrite(objPos, "Positions.txt")
    
    info = open("infoLC.txt", "w")
    info.write("Updated on UTC    : " + str(datetime.utcnow()))
    info.close()

    gc.collect()

run()
