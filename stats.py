import json
import sys
import os
import time
import math
import configparser

DEBUG = False

latestUpdate = ''
latestRuns = []
resultData = [[], [], [], []]
streakData = []

def main():
    #get the config file data
    path, fileOutput, historySize, tick, charCount, charNames = readConfig()

    initRunData(charCount, path, charNames, historySize)
    readStreakData(charCount)

    #update loop
    while True:
        checkUpdate(charCount, path, charNames, historySize)
        winrates = calcWinrates(historySize, charCount)
        outToFile('streaks.txt', streakData, charCount, winrates)
        if fileOutput:
            outToFile('winrates.txt', winrates, charCount, winrates)
        else:
            print('\tWinrates:')
            printWinrates(charNames, charCount, winrates)
            print('\tWinstreaks:')
            printStreaks(charNames, charCount)
            print()
        time.sleep(tick)


def printWinrates(charNames, charCount, winrates):
    print('Rotating: ', winrates[0])
    for i in range(charCount):
        print(charNames[i], ': ', winrates[i+1])

def printStreaks(charNames, charCount):
    print('Rotating: ', streakData[0])
    for i in range(charCount):
        print(charNames[i], ': ', streakData[i+1])


def outToFile(filename, data, charCount, winrates):
    with open(filename, mode='w') as f:
        for i in range(charCount+1):
            print(data[i], file=f)


def readStreakData(charCount):
    with open('streaks.txt') as f:
        line = f.read().split('\n')
        for i in range(charCount+1):
            streakData.append(int(line[i]))


def calcWinrates(historySize, charCount):
    winrates = [0]
    rotating = []
    skim = math.floor(historySize/charCount)
    for i in range(charCount):
        rotating.extend(resultData[i][-skim:])
        rate = getWinrate(resultData[i])
        winrates.append(rate)
    rate = getWinrate(rotating)
    winrates[0] = rate
    return winrates


def getWinrate(list):
    wins = sum(list)
    total = len(list)
    return format(wins/total * 100, '.1f') + '%'


def initRunData(charCount, path, charNames, historySize):
    for i in range(charCount):
        update, runs = getRunNames(os.path.join(path, charNames[i]), i)
        latestRuns.append(runs[-1])
        for filename in runs[-historySize:]:
            resultData[i].append(processRun(filename))


def checkUpdate(charCount, path, charNames, historySize):
    detected = False
    for i in range(charCount):
        update, runs = getRunNames(os.path.join(path, charNames[i]), i)
        if update and runs[-1] != latestRuns[i]:
            detected = True
            if DEBUG:
                print('New Run Detected')
            latestRuns[i] = runs[-1]
            new = processRun(runs[-1])
            if new:
                if DEBUG:
                    print('A ', charNames[i], ' run won')
                streakData[i+1] += 1
                streakData[0] += 1
            else:
                if DEBUG:
                    print('A ', charNames[i], ' run lost')
                streakData[i+1] = 0
                streakData[0] = 0
            resultData[i].append(new)
            if len(resultData[i]) > historySize:
                if DEBUG:
                    print('Deleting item from ', i, '\'s history')
                del resultData[i][0]
    if DEBUG and not detected:
        print('No New Run Detected')


def processRun(file):
    #Open new run file for processing
    with open(file) as f:
    	data = json.load(f)
    floor = data['floor_reached']
    hp = data['current_hp_per_floor'][-1]
    return floor == 57 and hp != 0


def getRunNames(runPath, charIdx):
    global latestUpdate
    stat = os.stat(runPath)
    time = stat.st_mtime
    if time != latestUpdate:
        latestUpdate = time
        runs = []
        with os.scandir(runPath) as dir:
            for entry in dir:
                if not entry.name.startswith('.') and entry.is_file():
                    runs.append(entry.path)
        runs.sort()
        return True, runs
    else:
        return False, []


def readConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    path = config['USER']['path']
    out = config['USER']['fileOutput']
    fileOutput = out == 'True'

    historySize = int(config['USER']['historySize'])
    tick = int(config['USER']['tick'])

    global DEBUG
    DEBUG = config['OTHER']['debug'] == 'True'
    charCount = int(config['OTHER']['charCount'])
    names = config['OTHER']['charNames']
    charNames = names.split('|')

    return path, fileOutput, historySize, tick, charCount, charNames


if __name__ == "__main__":
    main()
