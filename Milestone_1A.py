import yaml
import datetime
import time
import csv
from PIL import Image
logs = []
def timeFunc(parent, times):
    currTime = datetime.datetime.now()
    string = str(currTime) + ';' + parent + ' Executing TimeFunction(' + times['FunctionInput'] + ', ' + times['ExecutionTime'] + ')'
    print(string)
    logs.append(string)
    time.sleep(int(times['ExecutionTime']))

def performTask(parent, task):
    if task['Function'] == "TimeFunction":
        currTime = datetime.datetime.now()
        string = str(currTime) + ';' + parent + ' Entry'
        print(string)
        logs.append(str(currTime) + ';' + parent + ' Entry')
        timeFunc(parent, task['Inputs'])
        currTime = datetime.datetime.now()
        print(str(currTime) + ';' + parent + ' Exit')
        logs.append(str(currTime) + ';' + parent + ' Exit')

def performFlow(parent, values):
    for k in values.keys():
        # Add M1A_Workflow Entry to Output
        if values[k]['Type'] == "Flow":
            if parent == '':
                currTime = datetime.datetime.now()
                print(str(currTime) + ';' + parent + k + ' Entry')
                logs.append(str(currTime) + ';' + parent + k + ' Entry')
                performFlow(parent + k, values[k]['Activities'])
                currTime = datetime.datetime.now()
                print(str(currTime) + ';' + parent + k + ' Exit')
                logs.append(str(currTime) + ';' + parent + k + ' Exit')
            else:
                currTime = datetime.datetime.now()
                print(str(currTime) + ';' + parent + '.' + k + ' Entry')
                logs.append(str(currTime) + ';' + parent + '.' + k + ' Entry')
                performFlow(parent + '.' + k, values[k]['Activities'])
                currTime = datetime.datetime.now()
                print(str(currTime) + ';' + parent + '.' + k + ' Exit')
                logs.append(str(currTime) + ';' + parent + '.' + k + ' Exit')

        if values[k]['Type'] == 'Task':
            performTask(parent + '.' + k, values[k])

if __name__ == '__main__':
    yamlFile = open('Milestone1A.yaml')
    yamlParsed = yaml.load(yamlFile, Loader=yaml.FullLoader)

    # Yaml Parsed Dictionary
    # print(YamlParsed)
    yamlFile.close()
    logFile = open("Milestone1A_Log.txt", 'w')
    performFlow("", yamlParsed)
    for log in logs:
        logFile.write(log)
        logFile.write('\n')
    logFile.close()
