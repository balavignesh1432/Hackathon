import yaml
import datetime
import csv
from PIL import Image

def timeFunc(parent, secs):
    currTime = datetime.datetime.now()
    string = str(currTime) + ';' + parent + ' Executing TimeFunction(' + secs + ')'
    print(string)

def performTask(parent, task):
    if task['Function'] == "TimeFunction":
        currTime = datetime.datetime.now()
        string = str(currTime) + ';' + parent + ' Entry'
        print(string)
        timeFunc(parent, task['Inputs']['ExecutionTime'])
        print(str(currTime) + ';' + parent + ' Exit')

def performFlow(parent, values):
    for k in values.keys():
        # Add M1A_Workflow Entry to Output
        if values[k]['Type'] == "Flow":
            if parent == '':
                currTime = datetime.datetime.now()
                print(str(currTime) + ';' + parent + k + ' Entry')
                performFlow(parent + k, values[k]['Activities'])
                print(str(currTime) + ';' + parent + k + ' Exit')
            else:
                currTime = datetime.datetime.now()
                print(str(currTime) + ';' + parent + '.' + k + ' Entry')
                performFlow(parent + '.' + k, values[k]['Activities'])
                print(str(currTime) + ';' + parent + '.' + k + ' Exit')

        if values[k]['Type'] == 'Task':
            performTask(parent + '.' + k, values[k])

if __name__ == '__main__':
    yamlFile = open('Milestone1A.yaml')
    yamlParsed = yaml.load(yamlFile, Loader=yaml.FullLoader)

    # Yaml Parsed Dictionary
    # print(YamlParsed)
    yamlFile.close()
    performFlow("", yamlParsed)

    # csvFile = open('Sample.csv', 'w', encoding='UTF-8', newline="")
    # csvwriter = csv.writer(csvFile)
    #
    # # Write Entities as a List into csv
    # csvwriter.writerows([])
    # csvFile.close()
