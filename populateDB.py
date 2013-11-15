# Kavin Autar
# 2013/11/11
# Version 1.2
# Checks stocks


import logger
import sys
import db
import csv

file = sys.argv[1]



def populateIndustry(file):
    print "Getting Industries From File: %s" % file
    industryList = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        companies = [ x for x in reader ]
        for company in companies:
            industryList.append(company[2])
            
    industryList = list(set(industryList))

    for industry in industryList:
        print "Industry: %s" % industry

    print type(industryList)
    sqlList = []

    for i in industryList:
        tmpList = []
        tmpList.append(i)   
        sqlList.append(tmpList)

    print sqlList

    db.insertFromList("INSERT INTO industry (name) VALUES (%s)", sqlList)


def main():
    global file
    populateIndustry(file)


if __name__ == "__main__":
    main()





"""
with open (file, 'r') as f:
    reader = csv.reader(f)
    companies = [ x for x in reader ]

    for company in companies:
        print company
        print type(company), len(company)
        print company[1]

def

"""
