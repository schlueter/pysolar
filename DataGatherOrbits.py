#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 14:28:05 2017

@author: cjct1g14
"""

# http://www.minorplanetcenter.net/iau/MPCORB.html
# https://github.com/mommermi/callhorizons


import urllib.request as request
import datetime
import callhorizons
import wolframalpha
from shutil import copyfile
import time
import gc

def run():
    gc.collect()
    time.sleep(10)
    client = wolframalpha.Client("AJ353H-T462U2W84X")
    extra = False
    
    """
    Des - Name
    Type
    Parent 
    a - SemiMajor au 
    e - Eccen
    i - Incl Deg
    AoP - Arg Per Deg
    LoAN - Long Asc Node Deg
    Epoch for MA 
    MA - Mean Anom
    GM - Grav Param x Mass (km, s)
    RAD - radius km
    ROTPER - rotational period Earth Hours
    OBL - Obliquity deg
    """
    
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
    
    file = open("OutputO.txt", "w", newline='\r\n')
    file.write("")
    file.close()
    
    file = open("OutputO.txt", "a", newline='\r\n')
    file.write("Name,Type,Parent,Semi-Major Axis (au),Eccentricity,Inclination (Deg),Argument of Periapsis (Deg),Longitude of the Ascending Node (Deg),Epoch (Julian Day Number),Mean Anomaly (Deg)\n")
    file.close()
    
    SolarSystem =\
    {"Mercury":199,
     "Venus":299,
     "Earth":399,
     "Mars":499,
     "Jupiter":599,
     "Saturn":699,
     "Uranus":799,
     "Neptune":999}
    
    def MPunpackProvDes(ProvDesPack):
        try:
            float(ProvDesPack[-1])
            number = ProvDesPack[3:7]
            firstChar = ProvDesPack[0]
            secondChar = ProvDesPack[1]
            return number + " " + firstChar + "-" + secondChar
        except:
            FirstYearDigitsLetter = ProvDesPack[0]
            FirstYearDigitsDic = {"I":"18", "J": "19", "K":"20", "L":"21"}
            FirstYearDigits = FirstYearDigitsDic[FirstYearDigitsLetter]
            LastYearDigits = ProvDesPack[1:3]
            Year = FirstYearDigits + LastYearDigits
            HalfMonth1 = ProvDesPack[3]
            HalfMonth2 = ProvDesPack[6]
            HalfMonth = HalfMonth1 + HalfMonth2
            CompactingNumberDic =\
            {"A":100,
             "B":110,
             "C":120,
             "D":130,
             "E":140,
             "F":150,
             "G":160,
             "H":170,
             "I":180,
             "J":190,
             "K":200,
             "L":210,
             "M":220,
             "N":230,
             "O":240,
             "P":250,
             "Q":260,
             "R":270,
             "S":280,
             "T":290,
             "U":300,
             "V":310,
             "W":320,
             "X":330,
             "Y":340,
             "Z":350,
             "a":360,
             "b":370,
             "c":380,
             "d":390,
             "e":400,
             "f":410,
             "g":420,
             "h":430,
             "i":440,
             "J":450,
             "k":460,
             "l":470,
             "m":480,
             "n":490,
             "o":500,
             "p":510,
             "q":520,
             "r":530,
             "s":540,
             "t":550,
             "u":560,
             "v":570,
             "w":580,
             "x":590,
             "y":600,
             "z":610}
            try:
                float(ProvDesPack[4])
                number = ProvDesPack[4:6]
                numberfloat = float(number)
                if numberfloat == 0:
                    return Year + " " + HalfMonth
                if numberfloat != 0:
                    return Year + " " + HalfMonth + number
            except(ValueError):
                number1 = int(CompactingNumberDic[ProvDesPack[4]])
                number2 = int(ProvDesPack[5])
                number = str(number1 + number2)
                return Year + " " + HalfMonth + number
            
    def epochUnpack(EpochPack):
        YearDic =\
        {"I":18, "J":19, "K":20, "L":21}
        MonthDic =\
        {"1":1,
         "2":2,
         "3":3,
         "4":4,
         "5":5,
         "6":6,
         "7":7,
         "8":8,
         "9":9,
         "A":10,
         "B":11,
         "C":12}
        DayDic =\
        {"1":1,
         "2":2,
         "3":3,
         "4":4,
         "5":5,
         "6":6,
         "7":7,
         "8":8,
         "9":9,
         "A":10,
         "B":11,
         "C":12,
         "D":13,
         "E":14,
         "F":15,
         "G":16,
         "H":17,
         "I":18,
         "J":19,
         "K":20,
         "L":21,
         "M":22,
         "N":23,
         "O":24,
         "P":25,
         "Q":26,
         "R":27,
         "S":28,
         "T":29,
         "U":30,
         "V":31,}
        Year = int(YearDic[EpochPack[0]])*100 + float(EpochPack[1:3])
        Month = int(MonthDic[EpochPack[3]])
        Day = int(DayDic[EpochPack[4]])
        try:
            timeFrac = EpochPack[5::]
            Day = float(str(Day) + "." + timeFrac)
        except:
            timeFrac = 0
        return Year, Month, Day
    
    def gregToJD(greg):
        Year, Month, Day = greg
        a = int((14-Month)/12)
        y = Year + 4800 - a
        m = Month + 12*a - 3
        JDN = Day + int((153*m+2)/5) +365*y + int(y/4) - int(y/100) + int(y/400) - 32045
        JD = JDN + ((Day%1) - 12/24.)
        return JD
    
    def JDepoch(EpochPack):
        UnpackedEpoch = epochUnpack(EpochPack)
        JDepoch = gregToJD(UnpackedEpoch)
        return str(JDepoch)
    
    def MPproperties(Des):
        try:
            try:
                q = callhorizons.query(Des)
                UTC = datetime.datetime.utcnow()
                Year = UTC.year
                Month = UTC.month
                Day = UTC.day + int(UTC.hour/24) + int(UTC.minute/1440) + int(UTC.second/86400)
                Epoch = gregToJD((Year, Month, Day))
                q.set_discreteepochs(str(Epoch))
                q.get_elements()
                web = q.url
            except:
                try:
                    DesParts = Des.strip("(").split(") ")
                    Des = DesParts[0] + " " + DesParts[1]
                    q = callhorizons.query(Des)
                    UTC = datetime.datetime.utcnow()
                    Year = UTC.year
                    Month = UTC.month
                    Day = UTC.day + int(UTC.hour/24) + int(UTC.minute/1440) + int(UTC.second/86400)
                    Epoch = gregToJD((Year, Month, Day))
                    q.set_discreteepochs(str(Epoch))
                    q.get_elements()
                    web = q.url
                except:
                    return "n.a.", "n.a.", "n.a."
            req = request.urlopen(web)
            data = req.read().decode("utf-8")
            req.close()
            GMloc = data.find("GM=")
            for i in range(5, 30):
                GM = data[GMloc + 4: GMloc + i]
                if GM[-1] == " ":
                    GM = data[GMloc + 4: GMloc + i - 1]
                    break
            RADloc = data.find("RAD=")
            for i in range(6, 30):
                RAD = data[RADloc + 5: RADloc + i]
                if RAD[-1] == " ":
                    RAD = data[RADloc + 5: RADloc + i - 1]
                    break
            ROTPERloc = data.find("ROTPER=")
            for i in range(9, 30):
                ROTPER = data[ROTPERloc + 8: ROTPERloc + i]
                if ROTPER[-1] == " ":
                    ROTPER = data[ROTPERloc + 8: ROTPERloc + i -1]
                    break
            return GM.strip(" "), RAD.strip(" "), ROTPER.strip(" ")
        except:
            return "n.a.", "n.a.", "n.a."
    
    def SSproperties(Des):
        res = client.query(('mass of %s * G')%(Des))
        if (res == "(data not available)") or (res == "(insufficient data available)"):
            MG = "n.a."
        else:
            working = str(next(res.results).text).split(" ")[0]
            working2 = working.split("×")[0]
            working3 = working.split("×")[1].split("^")
            working4 = working3[1]
            MG = working2 + "E" + working4
        if Des == "Sun":
            res = client.query(('average radius of %s in km')%(Des))
        else:
            res = client.query(('average radius of Planet %s in km')%(Des))
        if (res == "(data not available)") or (res == "(insufficient data available)"):
            RAD = "n.a."
        else:
            RAD = str(next(res.results).text).split(" ")[0]
        res = client.query(('%s sidereal day in hours')%(Des))
        if (res == "(data not available)") or (res == "(insufficient data available)"):
            ROTPER = "n.a."
        else:
            ROTPER = str(next(res.results).text).split(" ")[0]
        res = client.query(('%s obliquity in degrees')%(Des))
        if (res == "(data not available)") or (res == "(insufficient data available)"):
            OBL = "n.a."
        else:
            OBL = str(next(res.results).text).split("°")[0]
        return MG, RAD, ROTPER, OBL
       
    def COMproperties(Des):
        try:
            try:
                q = callhorizons.query(Des)
                UTC = datetime.datetime.utcnow()
                Year = UTC.year
                Month = UTC.month
                Day = UTC.day + int(UTC.hour/24) + int(UTC.minute/1440) + int(UTC.second/86400)
                Epoch = gregToJD((Year, Month, Day))
                q.set_discreteepochs(str(Epoch))
                q.get_elements()
                web = q.url
            except:
                try:
                    DesParts = Des.split(" ")
                    if len(Des) != 1:
                        Des = DesParts[0] + " " + DesParts[1]
                        q = callhorizons.query(Des)
                        UTC = datetime.datetime.utcnow()
                        Year = UTC.year
                        Month = UTC.month
                        Day = UTC.day + int(UTC.hour/24) + int(UTC.minute/1440) + int(UTC.second/86400)
                        Epoch = gregToJD((Year, Month, Day))
                        q.set_discreteepochs(str(Epoch))
                        q.get_elements()
                        web = q.url
                    else:
                        DesParts = Des.split("/")
                        Des = DesParts[0] + " " + DesParts[1]
                        q = callhorizons.query(Des)
                        UTC = datetime.datetime.utcnow()
                        Year = UTC.year
                        Month = UTC.month
                        Day = UTC.day + int(UTC.hour/24) + int(UTC.minute/1440) + int(UTC.second/86400)
                        Epoch = gregToJD((Year, Month, Day))
                        q.set_discreteepochs(str(Epoch))
                        q.get_elements()
                        web = q.url
                except:
                    print("error")
                    return "n.a.", "n.a."
            req = request.urlopen(web)
            data = req.read().decode("utf-8")
            req.close()
            GMloc = data.find("  GM=")
            for i in range(7, 30):
                GM = data[GMloc + 6: GMloc + i]
                if GM[-1] == " ":
                    RAD = data[GMloc + 6: GMloc + i - 1]
                    break
            RADloc = data.find("  RAD=")
            for i in range(8, 30):
                RAD = data[RADloc + 7: RADloc + i]
                if RAD[-1] == " ":
                    RAD = data[RADloc + 7: RADloc + i - 1]
                    break
            return GM.strip(" "), RAD.strip(" ")
        except:
            return "n.a.", "n.a."
    
    #Epoch Code http://www.minorplanetcenter.net/iau/info/PackedDates.html
    #Minor Object Properties http://www.minorplanetcenter.net/iau/info/MPOrbitFormat.html
    #Provisional Designation Decode http://www.minorplanetcenter.net/iau/info/PackedDes.html
    
    
    try:
        responseMP = request.urlopen("http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT")
        datapackageMP = responseMP.read().decode("utf-8").split("\n")
        responseMP.close()
        datapackageMPlength = len(datapackageMP)
        count = 1
    except:
        pass
    startTime = time.time()
    Dwarfs = ["(1) Ceres", "(136472) Makemake", "(136108) Haumea", "(134340) Pluto", "(136199) Eris"]
    for MPobject in datapackageMP[43::]:
        try:
            ProvDesPack = MPobject[0:7].strip(" ")
            EpochPack = MPobject[20:25].strip(" ")
            MA = MPobject[26:35].strip(" ")
            MA = str(MAcheck(float(MA)))
            AoP = MPobject[37:46].strip(" ")
            LoAN = MPobject[48:57].strip(" ")
            i = MPobject[59:68].strip(" ")
            e = MPobject[70:79].strip(" ")
            a = MPobject[92:103].strip(" ")
            Des = MPobject[166:194].strip(" ")
            if Des[0] != "(":
                Des = MPunpackProvDes(ProvDesPack)
            Epoch = JDepoch(EpochPack)
            Type = "Minor Planet"
            Parent = "Sol"
            if Des in Dwarfs:
                Type = "Dwarf Planet"
            if (extra == True) and (MPobject not in Dwarfs):
                GM, RAD, ROTPER = MPproperties(Des)
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA, GM, RAD, ROTPER)
            elif (extra == True) and (MPobject in Dwarfs):
                GM, RAD, ROTPER, OBL, RA = SSproperties(Des)
                Type = "Dwarf Planet"
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA, GM, RAD, ROTPER, OBL, RA)
            else:
                if MPobject in Dwarfs:
                    Type = "Dwarf Planet"
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA)
            DataStruct = (("%s,"*len(datalist))[0:-1] + "\n")%datalist
            output = open("OutputO.txt", "a", newline='\r\n')
            output.write(DataStruct)
            output.close()
            elaspseTime = time.time() - startTime
            averageTimeIteration = elaspseTime/count
            TimeLeft = (datapackageMPlength - count)*averageTimeIteration
            infoOut = "\rGathering Minor Planet Data " + Des + " %.2f                        "%(TimeLeft/(60*60))
            print(infoOut, end = "")
            count += 1
        except:
            continue
    
#     http://www.minorplanetcenter.net/iau/info/CometOrbitFormat.html
    
    try:
        responseCOM = request.urlopen("http://www.minorplanetcenter.net/iau/MPCORB/CometEls.txt")
        datapackageCOM = responseCOM.read().decode("utf-8").split("\n")
        responseCOM.close()
        datapackageCOMlength = len(datapackageCOM)
        count = 1
    except:
        pass
    startTime = time.time()
    for COMobject in datapackageCOM:
        try:
            Des = COMobject[102:158].strip(" ")
            AoP = COMobject[51:59].strip(" ")
            LoAN = COMobject[61:69].strip(" ")
            i = COMobject[71:79].strip(" ")
            e = COMobject[41:49].strip(" ")
            rp = float(COMobject[30:39].strip(" "))
            if float(e) >= 1:
                a = "n.a."
            else:
                a = rp/(1-float(e))
            EpochDay = float(COMobject[22:29].strip(" "))
            EpochMonth = float(COMobject[19:21].strip(" "))
            EpochYear = float(COMobject[14:18].strip(" "))
            Epoch = gregToJD((EpochYear, EpochMonth, EpochDay))
            MA = 0
            Type = "Comet"
            Parent = "Sol"
            if extra == True:
                GM, RAD = COMproperties(Des)
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA, GM, RAD)
            else:
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA)
            DataStruct = (("%s,"*len(datalist))[0:-1] + "\n")%datalist
            output = open("OutputO.txt", "a", newline='\r\n')
            output.write(DataStruct)
            output.close()
            elaspseTime = time.time() - startTime
            averageTimeIteration = elaspseTime/count
            TimeLeft = (datapackageCOMlength - count)*averageTimeIteration
            infoOut = "\rGathering Comet Data " + Des + " %.2f                        "%(TimeLeft/(60*60))
            print(infoOut, end = "")
            count += 1
        except:
            continue
    
#    #http://callhorizons.readthedocs.io/en/latest/

    def solSys(Des):
            try:
                time.sleep(1)
                q = callhorizons.query(int(SolarSystem[Des]), smallbody=False)
                UTC = datetime.datetime.utcnow()
                Year = UTC.year
                Month = UTC.month
                Day = UTC.day + float(UTC.hour/24) + float(UTC.minute/1440) + float(UTC.second/86400)
                Epoch = gregToJD((Year, Month, Day))
                Type = "Major Planet"
                Parent = "Sol"
                q.set_discreteepochs(str(Epoch))
                q.get_elements()
                a = q["a"][0]
                e = q["e"][0]
                i = q["incl"][0]
                AoP =  q["argper"][0]
                LoAN = q["node"][0]
                MA = q["meananomaly"][0]
                MA = str(MAcheck(float(MA)))
                if extra == True:
                    GM, RAD, ROTPER, OBL, RA = SSproperties(Des)
                    datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA, GM, RAD, ROTPER, OBL)
                else:
                    datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA)
                DataStruct = (("%s,"*len(datalist))[0:-1] + "\n")%datalist
                output = open("OutputO.txt", "a", newline='\r\n')
                output.write(DataStruct)
                output.close()
                infoOut = "\rGathering Planet Data " + Des + "                         "
                print(infoOut, end = "")
            except:
                time.sleep(5)
                solSys(Des)
                
    for Des in SolarSystem:
        solSys(Des)
        
    MG, RAD, ROTPER, OBL = SSproperties("Sun")
    Des, Type, Parent, a, e, i, AoP, LoAN, MA = "Sol", "Star", "Galactic_Centre", "n.a.", "n.a.", "n.a.", "n.a.", "n.a.", "n.a."
    datalist = Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA, MG, RAD, ROTPER, OBL
    DataStruct = (("%s,"*len(datalist))[0:-1] + "\n")%datalist
    output = open("OutputO.txt", "a", newline='\r\n')
    output.write(DataStruct)
    output.close()

    
    """ObjectsWithMoons = ["Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
    for Item in ObjectsWithMoons:
        data = open("%sMoon.txt"%Item)
        readdata = data.readlines()
        for line in readdata:
            linesplit = line.split(" ")
            for obj in linesplit:
                if obj != "":
                    Name = obj
                    break
            for obj in linesplit:
                if obj != "":
                    try:
                        Number = float(obj)
                        break
                    except:
                        pass
            q = callhorizons.query(Number, smallbody=False)
            UTC = datetime.datetime.utcnow()
            Year = UTC.year
            Month = UTC.month
            Day = UTC.day + float(UTC.hour/24) + float(UTC.minute/1440) + float(UTC.second/86400)
            Epoch = gregToJD((Year, Month, Day))
            q.set_discreteepochs(str(Epoch))
            q.get_elements()
            a = q["a"][0]
            e = q["e"][0]
            i = q["incl"][0]
            AoP =  q["argper"][0]
            LoAN = q["node"][0]
            MA = q["meananomaly"][0]
            Des, Type, Parent = Name, "Moon", Item
            if extra == True:
                GM, RAD, ROTPER, OBL, RA = MOONproperties(Des)
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA, GM, RAD, ROTPER, OBL, RA)
            else:
                datalist = (Des, Type, Parent, a, e, i, AoP, LoAN, Epoch, MA)
            print(Name, Number)"""
    
    # http://astronomical.wikia.com/wiki/List_of_Jupiter_Moons?action=edit&section=1
    
    copyfile("OutputO.txt", "SolarSystemO.txt")
    
    Main = open("SolarSystemO.txt", "r")
    Objs = Main.readlines()
    NumberObjects = len(Objs) - 1
    Main.close()
    
    if extra == False:
        Notes = "No moons or phys. prop. yet"
    else:
        Notes = "No moons yet"
    
    info = open("infoO.txt", "w")
    info.write("Updated on UTC    : " + str(datetime.datetime.utcnow()) + "\n"
              +"Number of Objects : " + str(NumberObjects) + "\n"
              +"Notes             : " + Notes)
    info.close()
    
    
    del Objs
    gc.collect()
    time.sleep(10)
    

while True:
    try:
        run()
    except:
        run()
    time.sleep(60*60*5)
