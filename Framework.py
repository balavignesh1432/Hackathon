import yaml
import datetime
import time
import threading
import csv
from collections import OrderedDict
from PIL import Image
logs = []
shared = {}

def timeFunc(parent, times):
    if times['FunctionInput'][0] != '$':
        currTime = datetime.datetime.now()
        string = str(currTime) + ';' + parent + ' Executing TimeFunction(' + times['FunctionInput'] + ', ' + times['ExecutionTime'] + ')'
        logs.append(string)
        time.sleep(int(times['ExecutionTime']))
    else:
        currTime = datetime.datetime.now()
        key = times['FunctionInput'][2:len(times['FunctionInput']) - 1]
        keyList = key.split('.')
        key = ".".join(keyList[:len(keyList) - 1])
        print(key)
        print(shared)
        while key not in shared.keys():
            pass
        string = str(currTime) + ';' + parent + ' Executing TimeFunction(' + str(shared[key][keyList[-1]]) + ', ' + times[
            'ExecutionTime'] + ')'
        logs.append(string)
        time.sleep(int(times['ExecutionTime']))

def dataLoad(parent, data):
    fileName = data['Filename']
    file = open(fileName, 'r')
    csvreader = csv.reader(file)
    dataTable = []

    currTime = datetime.datetime.now()
    string = str(currTime) + ';' + parent + ' Executing DataLoad(' + fileName + ')'
    logs.append(string)

    for row in csvreader:
        dataTable.append(row)
    shared[parent] = {"DataTable":dataTable, "NoOfDefects":len(dataTable) - 1}
    file.close()

def writeSkipped(parent):
    currTime = datetime.datetime.now()
    logs.append(str(currTime) + ';' + parent + ' Entry')
    logs.append(str(currTime) + ';' + parent + ' Skipped')
    logs.append(str(currTime) + ';' + parent + ' Exit')

def writeEntry(parent):
    currTime = datetime.datetime.now()
    logs.append(str(currTime) + ';' + parent + ' Entry')

def writeExit(parent):
    currTime = datetime.datetime.now()
    logs.append(str(currTime) + ';' + parent + ' Exit')

def performTask(parent, task):
    if task['Function'] == "TimeFunction":
        if "Condition" not in task.keys():
            currTime = datetime.datetime.now()
            logs.append(str(currTime) + ';' + parent + ' Entry')
            timeFunc(parent, task['Inputs'])
            currTime = datetime.datetime.now()
            logs.append(str(currTime) + ';' + parent + ' Exit')
        else:
            items = task['Condition'].split()
            condition = items[0][2:len(items[0]) - 1]
            conditionList = condition.split('.')
            condition = ".".join(conditionList[:len(conditionList) - 1])
            while condition not in shared.keys():
                pass
            if items[1] == ">=":
                if shared[condition][conditionList[-1]] >= int(items[2]):
                    writeEntry(parent)
                    timeFunc(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == "<=":
                if shared[condition][conditionList[-1]] <= int(items[2]):
                    writeEntry(parent)
                    timeFunc(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == ">":
                if shared[condition][conditionList[-1]] > int(items[2]):
                    writeEntry(parent)
                    timeFunc(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == "<":
                if shared[condition][conditionList[-1]] < int(items[2]):
                    writeEntry(parent)
                    timeFunc(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == "=":
                if shared[condition][conditionList[-1]] == int(items[2]):
                    writeEntry(parent)
                    timeFunc(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)

    if task['Function'] == 'DataLoad':
        if "Condition" not in task.keys():
            currTime = datetime.datetime.now()
            logs.append(str(currTime) + ';' + parent + ' Entry')
            dataLoad(parent, task['Inputs'])
            currTime = datetime.datetime.now()
            logs.append(str(currTime) + ';' + parent + ' Exit')
        else:
            items = task['Condition'].split()
            condition = items[0][2:len(items[0]) - 1]
            conditionList = condition.split('.')
            condition = ".".join(conditionList[:len(conditionList) - 1])
            while condition not in shared.keys():
                pass
            if items[1] == ">=":
                if shared[condition][conditionList[-1]] >= int(items[2]):
                    writeEntry(parent)
                    dataLoad(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == "<=":
                if shared[condition][conditionList[-1]] <= int(items[2]):
                    writeEntry(parent)
                    dataLoad(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == ">":
                if shared[condition][conditionList[-1]] > int(items[2]):
                    writeEntry(parent)
                    dataLoad(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == "<":
                if shared[condition][conditionList[-1]] < int(items[2]):
                    writeEntry(parent)
                    dataLoad(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)
            if items[1] == "=":
                if shared[condition][conditionList[-1]] == int(items[2]):
                    writeEntry(parent)
                    dataLoad(parent, task['Inputs'])
                    writeExit(parent)
                else:
                    writeSkipped(parent)

def performFlow(parent, values, flow):
    threadArr = []
    flowThreads = []
    for k in values.keys():
        if values[k]['Type'] == "Flow":
            if parent == '':
                currTime = datetime.datetime.now()
                logs.append(str(currTime) + ';' + parent + k + ' Entry')
                performFlow(parent + k, values[k]['Activities'], values[k]['Execution'])
            else:
                currTime = datetime.datetime.now()
                logs.append(str(currTime) + ';' + parent + '.' + k + ' Entry')
                if flow == "Sequential":
                    performFlow(parent + '.' + k, values[k]['Activities'], values[k]['Execution'])
                if flow == "Concurrent":
                    thread = threading.Thread(target=performFlow, args=(parent + '.' + k, values[k]['Activities'], values[k]['Execution'],))
                    thread.start()
                    flowThreads.append(thread)
        if values[k]['Type'] == 'Task':
            if flow == 'Sequential':
                performTask(parent + '.' + k, values[k])
            if flow == 'Concurrent':
                thread = threading.Thread(target=performTask, args=(parent + '.' + k, values[k],))
                thread.start()
                threadArr.append(thread)
    for thread in threadArr:
        thread.join()
    for flowThread in flowThreads:
        flowThread.join()
    currTime = datetime.datetime.now()

    if parent != '':
        logs.append(str(currTime) + ';' + parent + ' Exit')

if __name__ == '__main__':
    yamlFile = open('Milestone2A.yaml')
    yamlParsed = yaml.load(yamlFile, Loader=yaml.FullLoader)
    yamlParsed = OrderedDict(yamlParsed)
    yamlFile.close()

    logFile = open("Milestone2A_Log.txt", 'w')
    performFlow("", yamlParsed, None)
    for log in logs:
        logFile.write(log)
        logFile.write('\n')
    logFile.close()

