# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:09:37 2021

@author: mak
"""

"""
def sichern über return  und eingabe typen
datei durchreichen
"""


import os
import pandas as pd
import time
import shutil
import numpy as np
import tkinter  as tk
from tkinter.messagebox import showinfo
from tkinter import messagebox





"""

pfad in txt fehlt handeling 

"""
def popup_window():
    window = tk.Toplevel()

    label = tk.Label(window, text="Hello World!")
    label.pack(fill='x', padx=50, pady=5)

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')

def popup_showinfo():
    showinfo("ShowInfo", "Hello World!")
    

def errorPop(error):
    
    messagebox.showwarning("warning", error)



def pathArr():
    datei = open(r'/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung/logcsv.txt','w+')
    firstLine = datei.readline()
    if firstLine[:4] != 'Path':
        timeCur = time.time()
        stringTimeCur = str(timeCur)
        newDatei = open (r'/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung/logcsv_'+ stringTimeCur + '_.txt','wb')
        firstLine = "Path = /Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung"
        shutil.copyfileobj(datei, newDatei)
        newDatei.close()
        time.sleep(1)
        newDatei = open (r'/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung/logcsv_'+ stringTimeCur + '_.txt','r')

        datei.write(firstLine + "\n")
        for zeile in newDatei:
            datei.write(zeile + "\n")
        newDatei.close()
    dirPath = firstLine[7:]
    dirPath = "/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung"
    result = [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f)) and f[-3:] == 'csv']   
    datei.close()
    return (result)
   
def logKollision (path):
    datei = open('/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung/logcsv.txt','r')
    cleanPath = path
    for zeile in datei:
        x = zeile.split('.csv ', -1)
        for elem in x:
            if not elem.endswith('.csv'):
                elem += '.csv'
            while elem in cleanPath:
                cleanPath.remove(elem) 
    datei.close()
    return cleanPath        
        
            
def log(cleanPath):
    datei = open('/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung/logcsv.txt','a')
    datei.write(' '.join([str(elem) for elem in cleanPath]))
    datei.write("\n" )
    datei.close()


def frameArr(cleanPath):
    frames = []
    for elem in cleanPath:
        try:
            df = pd.read_csv(os.path.join ("/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung" , elem))
            activity_list = df["activity name"].tolist()
            activity_list_sort = list(dict.fromkeys(activity_list))
            df = auswertung(activity_list_sort,df)
            frames.append(df)
        except:
            errorPop('vermutlich csv mit falschem Inhalt: ' + elem)
    return frames

def addTime(x, y):
    if len(x) < 4:
        x.insert(0, 0)
    if len(y) < 4:
        y.insert(0, 0)
    days = float(int(x[0]) + int(y[0]))
    hours = float(int(x[1]) + int(y[1]))
    days += hours // 24
    hours %=24
    minutes = float(int(x[2]) + int(y[2]))
    hours += minutes // 60
    minutes %= 60
    secondes = float(int(x[3]) + int(y[3]))
    minutes += secondes // 60
    secondes %= 60
    new_time = [days, hours, minutes, secondes]
    return new_time


def auswertung(list, df):
    
    df2 = df[['activity name', 'note', 'duration']]
    df3 = df2.dropna()
    zeitListe = df["duration"].tolist()
    gesammt = [0,0,0,0]
    for zeit in zeitListe:
        splitZeit = zeit.split(':', -1)
        gesammt = addTime(gesammt, splitZeit)
    summeZeit = gesammt[3]+(gesammt[2]*60)+(gesammt[1]*60*60)+(gesammt[0]*24*60*60)
    for comName in list:
        slect = df.loc[df['activity name']== comName]
        dauer = slect['duration']
        result = [0,0,0,0]
        for elem in dauer:
            x = elem.split(':', -1)
            result = addTime(result, x)
        tempString = str(int(result[1]+(result[0]*24))) + ':'
        tempString += str(int(result[2])) + ':'
        tempString += str(int(result[3]))
        summeDuration = result[3]+(result[2]*60)+(result[1]*60*60)+(result[0]*24*60*60)
        prozentInfo = str(((summeDuration/summeZeit)*100)) + '%'
        dic = {'day' : 'Summe Aktivität', 'start time': np.nan, 'stop time': np.nan, 'hierarchy path' : np.nan, 'note' : prozentInfo, 'tags' : np.nan,'activity name' : comName, 'duration' : tempString}
        df = df.append(dic , ignore_index = True)
    notelist = df3['note'].tolist()
    
    bstlist = []
    for string in notelist:
        zeiger = 0
        while zeiger < len(string):
            if (string[zeiger:zeiger+4]).isdigit():
                bstlist.append (string[zeiger:zeiger+4])
                zeiger +=3
            zeiger+= 1
    bstset = (set(bstlist))
    df3 = df3.reset_index()
    
    for bst in bstset:
        dauer = [0,0,0,0]
        posinlist = 0
        for string in notelist:
            zeiger = 0
            counter = 0
            while zeiger < len(string):
                if (string[zeiger:zeiger+4]).isdigit():
                    bstlist.append (string[zeiger:zeiger+4])
                    counter = counter + 1
                    zeiger +=3
                zeiger+= 1
            if str(int(bst)) in string:
                d_temp = df3['duration'][posinlist]
                d_temp = d_temp.split(':', -1)
                if len(d_temp) < 4:
                    d_temp.insert(0, 0)
                sec = int(d_temp[0])*24*60*60
                sec += int(d_temp[1])*60*60
                sec += int(d_temp[2])*60
                sec += int(d_temp[3])
                sec = sec//counter
                d_temp[0] = sec//(24*60*60)
                d_temp[1] = (sec%(24*60*60))//3600
                d_temp[2] = (sec%(60*60))//60
                d_temp[3] = (sec%60)
                dauer = addTime(d_temp, dauer)
            posinlist += 1
        tempString = str(int(((dauer[1]+(dauer[0]*24))))) + ':'
        tempString += str(int((dauer[2]))) + ':'
        tempString += str(int((dauer[3])))
        summeDauer = (dauer[3]+(dauer[2]*60)+(dauer[1]*60*60)+(dauer[0]*24*60*60))/counter
        prozentbst = str(((summeDauer/summeZeit)*100)) + '%'
        dic = {'day' : 'Summe Baustein' , 'start time': str(int(bst)), 'stop time': np.nan, 'hierarchy path' : np.nan, 'note' : prozentbst, 'tags' : np.nan,'activity name' : '% von gesammt Zeit', 'duration' : tempString}    
        df = df.append(dic , ignore_index = True)        
    return df


"""
Error Handling: xlsx bereits vorhanden  - popup
"""

def dfAuswertung (frames, cleanPath):
    names = []
    dfs = []
    for i in range (0, len(frames)):
        dfName = cleanPath[i][11:37]
        dfA = frames[i]
        dfC = dfA
        dfA = dfA.loc[dfA['day']== 'Summe Aktivität']
        dfB = dfC.loc[dfC['day'] == 'Summe Baustein']
        dfC = dfA.append(dfB)
        
        if dfName in names:
            pos = names.index(dfName)
            dfAdd = dfs[pos]
            dfAalt = dfAdd.loc[dfAdd['day']== 'Summe Aktivität']
            for i in dfAalt.index:
                dftemp = dfA[dfA['activity name'].str.contains(dfAalt['activity name'][i])]
                if not dftemp.empty:
                    dftemp.reset_index(inplace = True)
                    duration1 = dftemp['duration'][0]
                    duration1 = duration1.split(':', -1)
                    duration2 = dfAalt['duration'][i]
                    duration2 = duration2.split(':', -1)
                    durationf = addTime(duration1, duration2)
                    tempString = str(int(((durationf[1]+(durationf[0]*24))))) + ':'
                    tempString += str(int((durationf[2]))) + ':'
                    tempString += str(int((durationf[3])))
                    dfAalt['duration'][i] = tempString
                    indexNames = dfA[ dfA['activity name'] == dfAalt['activity name'][i] ].index
                    tempCount = dfAalt['tags'][i]
                    tempCount = tempCount [-3:]
                    tempCount = int(tempCount) + 1
                    tempCount = str(tempCount)
                    while len(tempCount) < 4:
                        tempCount = '0' + tempCount
                    dfAalt ['tags'][i] = 'Sample size:    ' + tempCount
                    dfA.drop(indexNames , inplace=True)
            dfAalt.append(dfA)
            dfBalt = dfAdd.loc[dfAdd['day']== 'Summe Baustein']
            for i in dfBalt.index:
                dftemp = dfB[dfB['activity name'].str.contains(dfBalt['activity name'][i])]
                if not dftemp.empty:
                    dftemp.reset_index(inplace = True)
                    duration1 = dftemp['duration'][0]
                    duration1 = duration1.split(':', -1)
                    duration2 = dfBalt['duration'][i]
                    duration2 = duration2.split(':', -1)
                    durationf = addTime(duration1, duration2)
                    tempString = str(int(((durationf[1]+(durationf[0]*24))))) + ':'
                    tempString += str(int((durationf[2]))) + ':'
                    tempString += str(int((durationf[3])))
                    dfBalt['duration'][i] = tempString
                    indexNames = dfB[ dfB['activity name'] == dfBalt['activity name'][i] ].index
                    tempCount = dfBalt['tags'][i]
                    tempCount = tempCount [-3:]
                    tempCount = int(tempCount) + 1
                    tempCount = str(tempCount)
                    while len(tempCount) < 4:
                        tempCount = '0' + tempCount
                    dfBalt ['tags'][i] = 'Sample size:    ' + tempCount
                    dfB.drop(indexNames , inplace=True)
            dfBalt.append(dfB)
            dfZusammen = dfAalt.append(dfBalt)
            dfs[pos] = dfZusammen
            
            
        else:
            names.append(dfName)
            for i in dfC.index:
                dfC['tags'][i] = 'Sample size:    001'
            dfs.append(dfC)
    for i in range(0,len(names)):
        names[i] = 'Wochenauswertung' + names[i] + '....'
    dfToXlsx(dfs, names)
    
def dfToXlsx (frames, cleanPath):
    
    for i in range (0, len(frames)):
        xlsxName = cleanPath[i][:-4] + ".xlsx"
        frames[i].to_excel(os.path.join ("/Users/hlsmitarbeiter/Documents/REFA VZ Daten und Auswertung" , xlsxName), index = False)

        


def main():
    path = pathArr()
    clearpath = logKollision(path)
    log(clearpath)
    frames = frameArr(clearpath)
    dfAuswertung(frames, clearpath)
    dfToXlsx(frames, clearpath)

if __name__ == "__main__":
    main() 










