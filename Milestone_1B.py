import yaml
import datetime
import time
import threading
import csv
from PIL import Image
logs = []
def timeFunc(parent, times):
    currTime = datetime.datetime.now()
    string = str(currTime) + ';' + parent + ' Executing TimeFunction(' + times['FunctionInput'] + ', ' + times['ExecutionTime'] + ')'
    logs.append(string)
    time.sleep(int(times['ExecutionTime']))


def performTask(parent, task):
    if task['Function'] == "TimeFunction":
        currTime = datetime.datetime.now()
        logs.append(str(currTime) + ';' + parent + ' Entry')
        timeFunc(parent, task['Inputs'])
        currTime = datetime.datetime.now()
        logs.append(str(currTime) + ';' + parent + ' Exit')

def performFlow(parent, values, flow):
    threadArr = []
    flowThreads = []
    # flowThreadArr = []
    for k in values.keys():
        # Add M1A_Workflow Entry to Output
        if values[k]['Type'] == "Flow":
            if parent == '':
                currTime = datetime.datetime.now()
                logs.append(str(currTime) + ';' + parent + k + ' Entry')
                performFlow(parent + k, values[k]['Activities'], values[k]['Execution'])
                # currTime = datetime.datetime.now()
                # logs.append(str(currTime) + ';' + parent + k + ' Exit')
            else:
                currTime = datetime.datetime.now()
                logs.append(str(currTime) + ';' + parent + '.' + k + ' Entry')
                if flow == "Sequential":
                    performFlow(parent + '.' + k, values[k]['Activities'], values[k]['Execution'])
                    # currTime = datetime.datetime.now()
                    # logs.append(str(currTime) + ';' + parent + '.' + k + ' Exit')
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
    yamlFile = open('Milestone1B.yaml')
    yamlParsed = yaml.load(yamlFile, Loader=yaml.FullLoader)

    # Yaml Parsed Dictionary
    # print(YamlParsed)
    yamlFile.close()
    logFile = open("Milestone1B_Log.txt", 'w')
    performFlow("", yamlParsed, None)
    for log in logs:
        logFile.write(log)
        logFile.write('\n')
    logFile.close()
