# -*- coding: utf-8 -*-
"""
Created on Wed May 19 22:07:12 2021

@author: rimes
"""


class Person:
    def __init__(self):
        self.name = ''
        self.property = ''
        self.mailAddress = ''
        self.numbers = []
        self.email = ''
        
    def getName(self):
        return self.name
    
    def getProperty(self):
        return self.property
    
    def getMailAddress(self):
        return self.property
    
    def getNumbers(self):
        return self.property
    
    def getEmail(self):
        return self.property
    
    def setName(self, newName):
        self.name = newName
        
    def setProperty(self, newProperty):
        self.property = newProperty
    
    def setMailAddress(self, newAddress):
        self.mailAddress = newAddress
    
    def setNumbers(self, newNum):
        self.numbers.append(newNum)
    
    def setEmail(self, newEmail):
        self.email = newEmail
        
    def printInfo(self):
        print("Name: " + self.name)
        print("Property: " + self.property)
        print("Mailing Address: " + self.mailAddress)
        if len(self.numbers) > 0:
            print('Numbers: ')
            for i in self.numbers:
                print("     " + i)
        
    
        