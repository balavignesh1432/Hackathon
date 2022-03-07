import yaml
import csv
from PIL import Image

if __name__ == '__main__':
    yamlFile = open('Sample.yaml')
    YamlParsed = yaml.load(yamlFile, Loader=yaml.FullLoader)

    # Yaml Parsed Dictionary
    print(YamlParsed)
    yamlFile.close()

    image = Image.open('Sample.png')

    # Black and White
    image = image.convert('1')

    # Pixel Data
    print(list(image.getdata()))
    image.close()

    csvFile = open('Sample.csv', 'w', encoding='UTF-8', newline="")
    csvwriter = csv.writer(csvFile)

    # Write Entities as a List into csv
    csvwriter.writerows([])
    csvFile.close()
