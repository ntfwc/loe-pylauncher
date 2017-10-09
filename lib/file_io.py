def readFile(filePath):
    with open(filePath, "r") as f:
        return f.read()

def writeFile(filePath, text):
    with open(filePath, "w") as f:
        return f.write(text)
