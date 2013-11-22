# Kavin Autar
# 2013/11/17
# Last modified 2013/11/17
# Version 1.3
# Checks stocks

# Imports
import logger as log
import sys
import db
import pyql
import datetime

def numericInputFixup(input):
    if "K" in str(input):
        output = int(float(input.strip("K")) * 1000)
#        output = "%0.2f" % output
        log.debug("trying to fixup numeric data %s into %s" % (input, output))
        return output
    elif "M" in str(input):
        output = int(float(input.strip("M")) * 1000000)
 #       output = "%0.2f" % output
        log.debug("trying to fixup numeric data %s into %s" % (input, output))
        return output
    elif "B" in str(input):
        output =  int(float(input.strip("B")) * 1000000000)
  #      output = "%0.2f" % output
        log.debug("trying to fixup numeric data %s into %s" % (input, output))
        return output
    else:
        log.debug("%s does not require numeric fixup" % input)
        return input

def validate(input):
    #print input
    if input is None:
        return input

    if input == "N/A":
        return None

    if "%" in input:    # remove % symbols
        input = input.strip("%")

    return numericInputFixup(input)


def getIndustryIDs():
    sqlQuery = "SELECT ID FROM INDUSTRY;"
    ids = db.selectQueryNoWhere(sqlQuery)
    return ids


def getCompanyCodes():

    industryIDs = getIndustryIDs()

    companiesSQLQuery = """SELECT c.code || co.suffix as ycode
from company c
join country co on c.country_id = co.id
where c.industry_id = %s;
"""

    # list of lists, each interior list comtains company codes for that id
    companyByID = []
        
    for row in industryIDs:
        industryID = row['id']
        idList = [industryID]
        companies = db.selectQuery(companiesSQLQuery, idList)
        companyList = []
        for company in companies:
            companyList.append(company['ycode'])
        companyByID.append(companyList)

        log.info("industry %s has %s companies" % (industryID, len(companyList)))

    return companyByID


def insertData(data):
    ycode = data['Symbol']
    code = ycode.split(".")[0]
    today = str(datetime.date.today())

    keys = ["AverageDailyVolume",
            "BookValue",
            "Change",
            "ChangeFromFiftydayMovingAverage",
            "ChangeFromTwoHundreddayMovingAverage",
            "ChangeFromYearHigh",
            "ChangeFromYearLow",
            "DaysHigh",
            "DaysLow",
            "DividendShare",
            "DividendYield",
            "EarningsShare",
            "EBITDA",
            "EPSEstimateCurrentYear",
            "EPSEstimateCurrentYear",
            "EPSEstimateNextQuarter",
            "FiftydayMovingAverage",
            "LastTradePriceOnly",
            "MarketCapitalization",
            "Open",
            "PERatio",
            "PercebtChangeFromYearHigh",
            "PercentChange",
            "PercentChangeFromFiftydayMovingAverage",
            "PercentChangeFromTwoHundreddayMovingAverage",
            "PercentChangeFromYearLow",
            "PreviousClose",
            "PriceBook",
            "PriceEPSEstimateCurrentYear",
            "PriceEPSEstimateCurrentYear",
            "PriceEPSEstimateNextYear",
            "PriceEPSEstimateNextYear",
            "PriceSales",
            "TwoHundreddayMovingAverage",
            "Volume",
            "YearHigh",
            "YearLow"]

    # validate data, 0 all null values
    for key in keys:
        data[key] = validate(data[key])

    averagesQuery = """INSERT INTO AVERAGES 
(DATE, 
CODE, 
AVERAGEDAILYVOLUME, 
TWOHUNDREDDAYMOVINGAVERAGE, 
FIFTYDAYMOVINGAVERAGE) 
VALUES (%s, %s, %s, %s, %s);"""

    changeQuery = """INSERT INTO CHANGE
(DATE,
CODE,
change,
changefromfiftydaymovingaverage,
changefromtwohundreddaymovingaverage,
changefromyearhigh,
changefromyearlow,
percentchangefromyearhigh,
percentchange,
percentchangefromfiftydaymovingaverage,
percentchangefromtwohundreddaymovingaverage,
percentchangefromyearlow)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    dailyQuery = """INSERT INTO DAILY
(DATE,
CODE,
volume,
dayshigh,
dayslow,
bookvalue,
open,
previousclose,
pricebook,
dividendshare,
dividendyield,
earningsshare,
marketcapitalization,
yearhigh,
yearlow,
peratio,
pricesales,
ebitda)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    epsQuery = """INSERT INTO EPS
(DATE,
CODE,
EPSESTIMATECURRENTYEAR,
EPSESTIMATENEXTQUARTER,
PRICEEPSESTIMATECURRENTYEAR,
PRICEEPSESTIMATENEXTYEAR)
VALUES (%s, %s, %s, %s, %s, %s);"""

    historicQuery = """INSERT INTO HISTORICDATA
(DATE,
CODE,
HIGH,
LOW,
OPEN,
CLOSE,
VOLUME)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

    avgValues = [today, 
                code, 
                data['AverageDailyVolume'], 
                data['TwoHundreddayMovingAverage'], 
                data['FiftydayMovingAverage']]

    changeValues = [today,
                    code,
                    data['Change'],
                    data['ChangeFromFiftydayMovingAverage'],
                    data['ChangeFromTwoHundreddayMovingAverage'],
                    data['ChangeFromYearHigh'],
                    data['ChangeFromYearLow'],
                    data['PercebtChangeFromYearHigh'],
                    data['PercentChange'],
                    data['PercentChangeFromFiftydayMovingAverage'],
                    data['PercentChangeFromTwoHundreddayMovingAverage'],
                    data['PercentChangeFromYearLow']]

    dailyValues = [today,
                    code,
                    data['Volume'],
                    data['DaysHigh'],
                    data['DaysLow'],
                    data['BookValue'],
                    data['Open'],
                    data['PreviousClose'],
                    data['PriceBook'],
                    data['DividendShare'],
                    data['DividendYield'],
                    data['EarningsShare'],
                    data['MarketCapitalization'],
                    data['YearHigh'],
                    data['YearLow'],
                    data['PERatio'],
                    data['PriceSales'],
                    data['EBITDA']]

    epsValues = [today,
                code,
                data['EPSEstimateCurrentYear'],
                data['EPSEstimateNextQuarter'],
                data['PriceEPSEstimateCurrentYear'],
                data['PriceEPSEstimateNextYear']]

    historicValues = [today,
                    code,
                    data['DaysHigh'],
                    data['DaysLow'],
                    data['Open'],
                    data['PreviousClose'],
                    data['Volume']]

    db.insertSingle(averagesQuery, avgValues)
    db.insertSingle(changeQuery, changeValues)
    db.insertSingle(dailyQuery, dailyValues)
    db.insertSingle(epsQuery, epsValues)
    db.insertSingle(historicQuery, historicValues)

def getDailyData():
    # list of lists each list contains codes
    companyCodesPerIndustry = getCompanyCodes()

    for companies in companyCodesPerIndustry:
        companyDataList = pyql.lookup(companies)

        for companyData in companyDataList:
            insertData(companyData)


        sys.exit()

def main():
    getDailyData()

if __name__ == "__main__":
    main()
