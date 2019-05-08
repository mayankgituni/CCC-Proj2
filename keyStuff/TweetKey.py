#!/usr/bin/env python3

class TweetKey:
    def __init__(self):
        
        self.allKeys = [[], [], [], []]
        
        f=open("keyFile.kf", "r")
        index = 0
        lines = f.readlines()
        for i in range(len(lines)):
            index = i%5
            if(index < 4):
                self.allKeys[index].append(lines[i].strip())
        
        f.close()
        
    def getKeys(self):
        return self.allKeys

    def getKey(self, id):
        keySet = []

        if id < len(self.allKeys[0]):
            for i in range(4):
                keySet.append(self.allKeys[i][id])

        return [keySet]

    def totalKeys(self):
        return len(self.allKeys[0])
