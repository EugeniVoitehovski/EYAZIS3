from printDocumets import printExpectation
from readFromFile import readFromFile
from saveInFile import SaveFile


def classicDocument():
    result = 'В разработке!'
    print(result)
    readFromFile()
    SaveFile(result, type)
    printExpectation()

def listDocument():
    result = 'В разработке!'
    print(result)
    readFromFile()
    SaveFile(result, type)
    printExpectation()