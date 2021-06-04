# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:59:34 2021

@author: rimes
"""


import openpyxl
from tqdm import tqdm
from Person import Person

class OutputHandler:
    def __init__(self, results):
        self.results = results
        
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb['Sheet']
        self.sheet['A1'] = 'First Name'
        self.sheet['B1'] = 'Last Name'
        self.sheet['C1'] = 'Phone 1'
        self.sheet['D1'] = 'Phone 2'
        self.sheet['F1'] = 'Property'
        self.sheet['G1'] = 'Address (Mailing)'
        self.sheet['H1'] = 'City'
        self.sheet['I1'] = 'State'
        self.sheet['J1'] = 'ZIP Code'
        
    
    def postResults(self):
        for row in range(2, len(self.results)):
            person = self.results[row]
            self.inputName(str(row), person.getName())
            self.inputNumbers(str(row), person.getNumbers())
            self.sheet['E' + str(row)] = person.getProperty()
            self.inputAddress(str(row), person.getMailAddress())
            
            

    def inputName(self, row, name):
        i = name.index(" ")
        self.sheet["A" + row] = name[:i]
        self.sheet["B" + row] = name[i + 1:]
    
    def inputNumbers(self, row, numbers):
        if len(numbers) == 1:
            self.sheet["C" + row] = numbers[0]
        elif len(numbers) == 2:
            self.sheet["C" + row] = numbers[0]
            self.sheet["D" + row] = numbers[1]
            
        
    def inputAddress(self, row, address):
        index = 0
        for i in range(len(address) - 1, -1, -1):
            if not address[i].isnumeric():
                index = i
                break
        self.sheet["J" + row] = address[index + 1:]
        
        temp = address[:index]
        index = temp.rfind(",")
        self.sheet['G' + row] = temp[:index]
        l = len(temp)
        self.sheet['I' + row] = temp[l - 2:]
        self.sheet['H' + row] = temp[index + 1:l - 3]
        
          
    
       
            
        