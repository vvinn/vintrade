
import json


class Filedb:
    
    def __init__(self, name):
        self.path = "db\\" + name;
    
    def readData(self):
        file = open(self.path, "r")
        line = file.readline()
        file.close()
        return line
        
    def writeData(self, line):
        file = open(self.path, "w")
        n = file.writelines(line)
        file.close()
        return n
        

def getStocks():
    db = Filedb('stocks.txt')
    return json.loads(db.readData())
    
def storeStocks(l):
    db = Filedb('stocks.txt')
    db.writeData(json.dumps(l))
    
def storeBal(l):
    db = Filedb('bal.txt')
    db.writeData(json.dumps(l))
    
def getBal():
    db = Filedb('bal.txt')
    return json.loads(db.readData())
      
if __name__ == "__main__":
    print(getStocks())
    myfile = Filedb('tmp.txt')
    print(myfile.readData())
    myfile.writeData("now i am here")
    print(myfile.readData())
    