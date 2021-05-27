# -*- coding: utf-8 -*-
"""
Created on Thu May  6 16:45:26 2021

@author: rimes
"""


import openpyxl
from tqdm import tqdm

class InputHandler:
    def __init__(self):
        self.properties = {}
    
    def getInput(self, file):            
        wb = openpyxl.load_workbook(file)
        sheet = wb['Sheet1']
        
        for row in tqdm(range(3,sheet.max_row + 1)):
            name = self.parseName(sheet['B' + str(row)].value)
            if name == None or sheet['A' + str(row)].value == None:
                continue
            address = sheet['A' + str(row)].value
            self.properties[address] = name
        

       
    def parseName(self, name):
        if name == None:
            return None
        if '&' in name:
            i = name.rfind("&")
            return name[i + 2:]
        elif 'c/o' in name:
            i = name.index('c/o')
            if 'Conservator' in name:
                j = name.index('Conservator')
                return name[i + 4:j -2]
            return [name[i + 4:]]
        elif any(not i.isalnum() and not i == '-' and not i == ' ' for i in name):
            return None
        return name
    
    
    def countSpaces(self, string):
        count = 0
        for i in string:
            if i == ' ':
                count += 1
        return count
    

    def getLastName(self, string):
        for i in range(len(string)):
            if string[i] == ' ':
                return string[i + 1:]
        return None
    
    #if the name is in form last, first
    def commaCheck(self, string):
        for i in range(len(string)):
            if string[i] == ",":
                return string[i + 2:] + string[:i]
        return string
    
    #if there are any parenthesis in the name
    def parenthesisCheck(self, string):
        for i in range(len(string)):
            if '(' == string[i]:
                i = string.index("(")
                return string[:i]
        return string
    
    def middleInitialCheck(self, string):
        for i in range(1, len(string) - 1):
            if string[i - 1] == ' ' and string[i + 1] == ' ':
                return string[:i - 1] + string[i + 2:]
        return string
    
    def getZipCode(self, string):
        j = string.rfind(",")
        for i in range(j, len(string)):
            if string[i].isnumeric():
                j = i
                break
        return string[j:]
    
    def getAdress(self, string):
        i = string.index(",")
        return string[:i].lower()
    
    def getCityState(self, string):
        j = string.index(",")
        for i in range(j, len(string)):
            if string[i].isnumeric():
                break
        return string[j + 2:i - 1]
    
    


    
if __name__ == "__main__":
    IO = InputHandler()
    IO.getInput('2 26 19 Skip Tracing.xlsx')
    print(IO.properties)         
    

                
        
                
    