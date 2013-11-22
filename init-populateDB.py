# Kavin Autar
# 2013/11/11
# Last modified 2013/11/17
# Version 1.3
# Checks stocks

# Imports
import logger as log
import sys
import db
import csv
import historicData

def populateIndustry(file):
    log.info("populating INDUSTRY table with data from %s" % file)
    industryList = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        companies = [ x for x in reader ]
        for company in companies:
            industryList.append(company[2])
            
    industryList = list(set(industryList))
    log.info("unique industries: %s" % ", ".join(industryList))

    sqlQuery = "INSERT INTO INDUSTRY (NAME) VALUES (%s);"
    
    for industry in industryList:
        log.debug("trying to populate industry with value %s" % industry)
        sqlValue = [industry]
        db.insertSingle(sqlQuery, sqlValue)

def populateCountry(name, suffix):
    log.info("populating Country with values %s:%s" % (name, suffix))
    sqlQuery = "INSERT INTO COUNTRY (NAME, SUFFIX) VALUES (%s, %s);"
    try:
        db.insertSingle(sqlQuery, [name, suffix])
    except:
        log.error("error inserting country")


def populateCompanies(file):
    log.info("populating COMPANY table, getting data from %s" % file)
    with open(file, "r") as f:
        reader = csv.reader(f)
        companies = [ x for x in reader ]
        for company in companies:
            companyName = company[0]
            companyCode = company[1]
            # get code for query
            industry = company[2]
            industryAsList = [industry]
            sqlQuery = "SELECT ID FROM INDUSTRY WHERE NAME = %s;"
            industryID = db.selectQuery(sqlQuery, industryAsList)
            industryID = industryID[0]['id']

            insertSQL = "INSERT INTO COMPANY (CODE, NAME, INDUSTRY_ID) VALUES (%s, %s, %s);"
            try:
                log.debug("trying to populate company with value %s" % companyName)
                db.insertSingle(insertSQL, [companyCode, companyName, industryID])
            except:
                log.error("unable to insert %s into company" % companyName)

def populateHistoric():
    companiesSQLQuery = """SELECT c.code || co.suffix as ycode
from company c
join country co on c.country_id = co.id;
"""

    companies = db.selectQuery(companiesSQLQuery, [])
    #print companies
    companyList = []
    for company in companies:
        companyList.append(company[0])

    for ycode in companyList:
        historicData.getHistoricInfo(ycode)
        
def main():
    try:
        file = sys.argv[1]
    except:
        print "Usage: python init-populateDB.py file.csv"
        log.error("init-populateDB.py called with no csv file")
        sys.exit(1)
    
    populateIndustry(file)
    populateCountry("Australia", ".ax")
    populateCompanies(file)
    populateHistoric()


if __name__ == "__main__":
    main()

