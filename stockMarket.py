#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:08:22 2020

@author: niccolodiana
"""

import math, random, datetime

class Market:
    
    def __init__(self):
        self.transactionsHistory = list()
        self.numTotalUsers = list()
        self.numOnlineUsers = list()
        self.stocksArray = list()
        self.usersArray = list()
    
    def __str__(self):
        print('List of users:\n', self.usersArray)
        print('List of stocks:\n', self.stocksArray)
    
    def addCompany(self, company):
        if type(company) == Company:
            self.stocksArray.append(company)
        else:
            print('This is not a company, and hence cannot be listed')
    def addUser(self, user):
        if type(user) == User:
            self.usersArray.append(user)
        else:
            print('This is not a valid user')
        
class Company:
    #Pps stands for price per share for brevity
    
    def __init__(self, market, name, pps, stockCode):
        if type(name) != str or type(pps) != float:
            return
        self.market=market
        self.name = name
        self.pps = pps
        self.stockCode = stockCode
        #self.amount = 100000000 #100 million shares
        #new params
        self.opening= None
        self.closing= None
        
    def __str__(self):
        return f'Name: {self.name}\Price per share: {self.pps}\nstockCode: {self.stockCode}\nAmount of shares: {self.amount}'
    
    def changePps(self, amountSold=0, amountBought=0):
        #Formula to change the pps depending on whether stocks were sold or bought, simple linear form (should change it)
        if amountSold:
            if self.pps <= 10:
                change = amountSold/100000
            if self.pps > 10:
                change = amountSold/50000
            multiplyer = 1 - change
            self.pps = multiplyer * self.pps
        if amountBought:
            change = amountBought/50000
            multiplyer = 1 + change
            self.pps = multiplyer * self.pps
            
            

class Transaction:
    
    def __init__(self, market, user, stockCode, time, quantity, price):
        self.market = market
        self.user = user
        self.stockCode = stockCode
        self.time = time
        self.quantity = quantity
        self.price = price

class User:
    
    def __init__(self, market, username, password, bankAccount=100000):
        self.market = market
        self.username = username
        self.password = password
        self.bankAccount = bankAccount
        self.portfolio = dict()
        self.id = datetime.datetime.now()
        self.transactionsHistory = dict()
        
    def __str__(self):
        return f'Username: {self.username}\nBankAccound: {self.bankAccount}\nPortfolio: {self.portfolio}'
    
    def getInfo(self):
        return (self.username, self.password, self.bankAccount)
        
    def changePassword(self, newPass):
        self.password = newPass
    
    def buyShares(self, stockCode, amountShares):
        
        if type(stockCode) != str or type(amountShares) != int:
            return
        
        foundCompany = False
        
        for stock in market.stocksArray:
            if stock.stockCode == stockCode:
                foundCompany = True
                moneyNecessary = stock.pps * amountShares
                if moneyNecessary <= self.bankAccount:
                    #purchase is happening
                    self.bankAccount -= moneyNecessary
                    
                    #records the purchase in portfolio
                    if stockCode not in self.portfolio.keys():
                        self.portfolio[stockCode] = amountShares
                    else:
                        oldAmount = self.portfolio[stockCode]
                        self.portfolio[stockCode] = oldAmount + amountShares
                        
                    transaction = Transaction(
                            self.market,
                            self.username, 
                            stockCode, 
                            datetime.datetime.now(), 
                            amountShares, 
                            stock.pps
                            )
                    market.transactionsHistory.append(transaction)
                    stock.changePps(amountBought=amountShares)
                else: 
                    print('You do not have enough money to buy them')
                    return
            if not foundCompany:
                print('This company stockCode does not exist')
        
    def sellShares(self, stockCode, amountShares):
        
        if type(stockCode) != str or type(amountShares) != int:
            return
        
        foundCompany = False
        
        for stock in market.stocksArray:
            if stock.stockCode == stockCode:
                foundCompany = True
                moneyReceived = stock.pps * amountShares
                if amountShares <= self.portfolio[stockCode]:
                    #purchase is happening
                    self.bankAccount += moneyReceived
                    newAmountShares = self.portfolio[stock.stockCode] - amountShares
                    self.portfolio[stock.stockCode] = newAmountShares
                    transaction = Transaction(
                            self.market,
                            self.username,
                            stockCode,
                            datetime.datetime.now(),
                            amountShares,
                            stock.pps
                            )
                    market.transactionsHistory.append(transaction)
                    stock.changePps(amountSold=amountShares)
                else: 
                    print('You do not have enough money to buy them')
            if not foundCompany:
                print('This company stockCode does not exist')

                    

market = Market()

panzarotti = Company(market, 'Panzarotti', 5.61, 'PNZ')
market.addCompany(panzarotti)

mario = User(market, 'mario', '123', 40000000)
market.addUser(mario)


        