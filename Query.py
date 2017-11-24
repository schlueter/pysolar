#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 17:36:16 2017

@author: cjct1g14
"""

import numpy as np
from difflib import SequenceMatcher
import signal
import os
import psutil
import hashlib
import getpass
import subprocess

os.system("export DISPLAY=:0")

location = "/home/gacrux/"

last = 0
lastQuery = ""

encrPass = "3c3492e9d98412e9cabb63fde502ff374dd506876824167fd427f8a605a325b29fbc08f8485f02964f265cac61a34787df9f46baff9ab33b0f1afca054580729"

def query(lastQuery, last):
    cpuUsage = psutil.cpu_percent(interval=1)
    memUse = psutil.virtual_memory().percent
    swapUse = psutil.swap_memory().percent
    if max(cpuUsage, memUse, swapUse) > 80:
        print("\nWarning Server Usage Critical")
        print("Use command: 'system' for details")
    Input = input("\nAsk Database: ")
    Input = Input.lower()
    Input += " "
    if "closest" in Input:
        Input = Input.strip("closest").strip(" ")
        last = closest(Input)
        return "closest", last
    if "furthest" in Input:
        Input = Input.strip("furthest").strip(" ")
        last = furthest(Input)
        return "furthest", last
    if ("distance" in Input):
        if "and" not in Input:
            print("ERROR: Need to add 'and' between objects")
            return "error", last
        Input = Input.split("and")
        Input2 = Input[1].strip(" ")
        Input1 = Input[0].strip("distance").strip(" ")
        last = distance(Input1, Input2)
        return "distance", last
    if ("data" in Input):
        Input = Input.strip("data").strip(" ")
        last = data(Input)
        return "data", last
    if ("period" in Input) and (lastQuery == "data"):
        period(last)
        return "period", last
    if ("apoapsis" in Input) and (lastQuery == "data"):
        last = apoapsis(last)
        return "apoapsis", last
    if ("periapsis" in Input) and (lastQuery == "data"):
        last = periapsis(last)
        return "periapsis", last
    if (("km" in Input) or ("kilometres" in Input)) and (lastQuery in ["closest","furthest","distance","apoapsis","periapsis"]):
        convertKM(last)
        return "convert", last
    if "length" in Input:
        length()
        return "length", last
    if "system" in Input:
        system()
        return "system", last
    if (("quit" in Input) or ("leave" in Input) or ("exit" in Input)) and ("SSH_CONNECTION" not in os.environ):
        return "quit", last
    if "admin" in Input:
        if passwordCheck() == True:
            while True:
                command = admin()
                if command == "leave":
                    return "leave", last
                if command == "quit":
                    return command, last
        else:
            print("Incorrect Password for Admin")
            return "error", last
    else:
        print("ERROR: Invalid key word")
        return "error", last

        
def closest(Input):
    File = open(location+"Positions.txt", "r")
    fileOpen = File.read().split("\n")
    File.close()
    lookedList = []
    looked = ""
    for looking in fileOpen[1::]:
        looking = looking.split(",")
        if Input in looking[0].lower():
            lookedList.append(looking)
    if lookedList == []:
        print("Object Not Found")
        return
    ratio0 = 0
    for check in lookedList:
        ratio = SequenceMatcher(None, check[0].lower(), Input).ratio()
        if ratio > ratio0:
            looked = check
            ratio0 = ratio    
    x, y, z = float(looked[2]), float(looked[3]), float(looked[4])
    targeted = ""
    minRange = np.inf
    for target in fileOpen:
        try:
            target = target.split(",")
            xt, yt, zt = float(target[2]), float(target[3]), float(target[4])
            Range = np.sqrt((x-xt)**2. + (y-yt)**2 + (z-zt)**2)
            if (Range < minRange) and (looked[0] != target[0]):
                minRange = Range
                targeted = target[0]
        except:
            pass
    print("Closest Object to",looked[0],"is: ",targeted, " at range:",minRange,"au")
    return minRange

    
def furthest(Input):
    File = open(location+"Positions.txt", "r")
    fileOpen = File.read().split("\n")
    File.close()
    lookedList = []
    looked = ""
    for looking in fileOpen[1::]:
        looking = looking.split(",")
        if Input in looking[0].lower():
            lookedList.append(looking)
    if lookedList == []:
        print("Object Not Found")
        return
    ratio0 = 0
    for check in lookedList:
        ratio = SequenceMatcher(None, check[0].lower(), Input).ratio()
        if ratio > ratio0:
            looked = check
            ratio0 = ratio    
    x, y, z = float(looked[2]), float(looked[3]), float(looked[4])
    targeted = ""
    maxRange = 0
    for target in fileOpen:
        try:
            target = target.split(",")
            xt, yt, zt = float(target[2]), float(target[3]), float(target[4])
            Range = np.sqrt((x-xt)**2. + (y-yt)**2 + (z-zt)**2)
            if (Range > maxRange) and (looked[0] != target[0]):
                maxRange = Range
                targeted = target[0]
        except:
            pass
    print("Furthest Object to",looked[0],"is: ",targeted, " at range:",maxRange,"au")
    return maxRange
    
def distance(Input1, Input2):
    File = open(location+"Positions.txt", "r")
    fileOpen = File.read().split("\n")
    File.close()
    lookedList1, lookedList2 = [], []
    looked1, looked2 = "", ""
    for looking in fileOpen[1::]:
        looking = looking.split(",")
        if Input1 in looking[0].lower():
            lookedList1.append(looking)
        if Input2 in looking[0].lower():
            lookedList2.append(looking)
    if (lookedList1 == []):
        print("First Object Not Found")
        return
    if (lookedList2 == []):
        print("Second Object Not Found")
        return
    ratio0 = 0
    for check in lookedList1:
        ratio = SequenceMatcher(None, check[0].lower(), Input1).ratio()
        if ratio > ratio0:
            looked1 = check
            ratio0 = ratio    
    ratio0 = 0
    for check in lookedList2:
        ratio = SequenceMatcher(None, check[0].lower(), Input2).ratio()
        if ratio > ratio0:
            looked2 = check
            ratio0 = ratio    
    x1, y1, z1 = float(looked1[2]), float(looked1[3]), float(looked1[4])
    x2, y2, z2 = float(looked2[2]), float(looked2[3]), float(looked2[4])
    Range = np.sqrt((x1-x2)**2. + (y1-y2)**2 + (z1-z2)**2)
    print("Distance between:",looked1[0], "and", looked2[0], "is", Range, "au")
    return Range

def data(Input):
    def sunCatch(Input):
        if Input == "sun":
            ans = input("Did you mean Sol? (y/n): ").lower()
            if ans.startswith("y"):
                Input = "sol"
                return Input
            elif ans.startswith("n"):
                Input = "sun"
                return Input
            else:
                print("Please enter either 'y' or 'n'")
                sunCatch(Input)
        else:
            return Input
    sunCatch(Input)
    possibleObjects = []
    selectObj = {}
    try:
        File = open(location+"SolarSystemF.txt")
        fileOpen = File.read().split("\n")
        print("Full Data Available")
    except:
        File = open(location+"SolarSystemO.txt")
        fileOpen = File.read().split("\n")
        print("Only Orbital Data Available")
    PropList = fileOpen[0].split(",")
    if Input != "random":
        for obj in fileOpen[1::]:
            Data = obj.split(",")
            if Input in Data[0].lower():
                possibleObjects.append(Data)
        if len(possibleObjects) == 0:
            print("No Objects Found")
            return
        if len(possibleObjects) > 1:
            print("\nWhich Object Number?")
            for j in range(0, len(possibleObjects)):
                ratio = SequenceMatcher(None, possibleObjects[j][0].lower(), Input).ratio()
                selectObj[j] = possibleObjects[j] 
                print(j, "  ", possibleObjects[j][0], " Match Ratio: %.2f"%(ratio))
            chosenObjNumber = float(input("Number: "))
            chosenObj = selectObj[chosenObjNumber]
        else:
            chosenObj = possibleObjects[0]
    elif Input == "random":
        import random
        data = fileOpen[1::]
        rand = random.randint(0, len(data))
        chosenObj = data[rand].split(",")
    print("\n")
    for i in range(0, len(PropList)):
        print(PropList[i], ":", chosenObj[i])
    return chosenObj
        
def length():
    try:
        full = open(location+"SolarSystemF.txt", "r").readlines()[1::]
        lengthFull = len(full)
    except:
        lengthFull = "Not Available"
    try:
        orbit = open(location+"SolarSystemO.txt", "r").readlines()[1::]
        lengthOrbit = len(orbit)
    except:
        lengthOrbit = "Not Available"
    print("Objects in Full Dataset:",lengthFull)
    print("Objects in Orbit Dataset:",lengthOrbit)
    
def period(LastInput):
    a = float(LastInput[3]) * 149597871 * 1000
    File = open(location+"SolarSystemO.txt", "r")
    fileOpen = File.read().split("\n")
    File.close()
    lookedList = []
    looked = ""
    for looking in fileOpen[1::]:
        looking = looking.split(",")
        if "sol" in looking[0].lower():
            lookedList.append(looking)
    if lookedList == []:
        print("Sol Not Found For Calculation")
        return
    ratio0 = 0
    for check in lookedList:
        ratio = SequenceMatcher(None, check[0].lower(), "sol").ratio()
        if ratio > ratio0:
            looked = check
            ratio0 = ratio
    largest = 0
    for prop in looked:
        try:
            if float(prop) > largest:
                largest = float(prop)
        except:
            pass
    gm = largest
    T = 2*np.pi*np.sqrt((a**3.)/gm)
    T /= (24.0000001987*60*60)
    if T > 720:
        print("Orbital Period:",T/365.2422,"years")
    else:
        print("Orbital Period:",T,"days")
        
def periapsis(LastInput):
    a = float(LastInput[3])
    e = float(LastInput[4])
    rp = (1-e)*a
    print("Periapsis", rp, "au")
    return rp

def apoapsis(LastInput):
    a = float(LastInput[3])
    e = float(LastInput[4])
    ra = (1+e)*a
    print("Apoapsis", ra, "au")
    return ra
        
def convertKM(Input):
    print(Input * 149597871, "km")

if "SSH_CONNECTION" in os.environ:
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    
def system():
    cpuUsage = psutil.cpu_percent(interval=1, percpu=True)
    memUse = psutil.virtual_memory().percent
    swapUse = psutil.swap_memory().percent
    diskUse = psutil.disk_usage("/").percent
    dataWrite = ""
    for i, cpu in enumerate(cpuUsage):
        dataWrite += "CPU%d %%\t %.1f\n"%(i,cpu)
    dataWrite += "RAM  %%\t %.1f\n"%memUse
    dataWrite += "SWAP %%\t %.1f\n"%swapUse
    dataWrite += "HDD  %%\t %.1f\n"%diskUse
    print(dataWrite)

#ADMIN   
def passwordMaker():
    password = hashlib.sha512(getpass.getpass("Please Enter Password: ").encode("utf-8")).hexdigest()
    print(password)

def passwordCheck(ePass = encrPass):
    print("Encrypted with SHA512")
    password = hashlib.sha512(getpass.getpass("Please Enter Password: ").encode("utf-8")).hexdigest()
    if password == ePass:
        return True
    else:
        False

def startUpdate():
    os.system("gnome-terminal -e " + location + "DataGatherFull.py")
    print("Full Data Gather On")
    os.system("gnome-terminal -e " + location + "DataGatherOrbits.py")
    print("Orbit Data Gather On")
    os.system("gnome-terminal -e " + location + "LocationCalc.py")
    print("Location Calculator On")
    
def stopUpdate():
    os.system("pkill -9 -f %sDataGatherFull.py"%(location))
    print("Full Data Gather Off")
    os.system("pkill -9 -f %sDataGatherOrbits.py"%(location))
    print("Orbit Data Gather Off")
    os.system("pkill -9 -f %sLocationCalc.py"%(location))
    print("Location Calculator Off")
    
def admin():
    subprocess.Popen("export DISPLAY=:0", shell=True)
    Input = input("\nAdmin Request: ").lower()
    if "start update" == Input:
        startUpdate()
        return
    if "stop update" == Input:
        stopUpdate()
    if (("quit" in Input) or ("leave" in Input) or ("exit" in Input)):
        return "leave"
    if "kill" in Input:
        return "quit"
    else:
        print("Invalid Entry")


def runner(last = last, lastQuery = lastQuery):
    while True:
        if lastQuery == "quit":
            break
        try:
            lastQuery, last = query(lastQuery, last)
        except:
            print("Unknown Error - Restarting")
            runner()


runner()
        
