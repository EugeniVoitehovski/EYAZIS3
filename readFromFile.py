def readFromFile():
    file = open('texts/text1.txt', "r")
    content = file.read()
    print(content)