# Kavin Autar
# 2013/11/11
# Version 1.2
# Checks stocks



import ystockquote as stock
import pyql
import datetime
import logger as log
import json



def stockAll(code):
    """
    function which gets all stock information provided by pyql  

    """

    log.info("mining %s for all data" % code)
    codeList = [code]
    pyqlReturn = pyql.lookup(codeList)
    codeReturn = pyqlReturn[0]
    keys = ["AverageDailyVolume", "BookValue", "Change", "ChangeFromFiftydayMovingAverage", "ChangeFromTwoHundreddayMovingAverage", "ChangeFromYearHigh", "ChangeFromYearLow", "DaysHigh", "DaysLow", "DividendShare", "DividendYield", "EarningsShare", "EBITDA", "EPSEstimateCurrentYear", "EPSEstimateNextQuarter", "FiftydayMovingAverage", "MarketCapitalization", "Open", "PERatio", "PercebtChangeFromYearHigh", "PercentChange", "PercentChangeFromFiftydayMovingAverage", "PercentChangeFromTwoHundreddayMovingAverage", "PercentChangeFromYearLow", "PreviousClose", "PriceBook", "PriceEPSEstimateCurrentYear", "PriceEPSEstimateNextYear", "PriceSales", "TwoHundreddayMovingAverage", "Volume", "YearHigh", "YearLow"]

    for key in keys:
        print "%s : %s" % (key, codeReturn[key])

def multiStockAll(codes):
    """
    function takes a list of codes and provides information via pyql
    """

    log.info("mining list [ %s ] for all information" % " : ".join(codes))
    pyqlReturn = pyql.lookup(codes)
    keys = ["AverageDailyVolume", "BookValue", "Change", "ChangeFromFiftydayMovingAverage", "ChangeFromTwoHundreddayMovingAverage", "ChangeFromYearHigh", "ChangeFromYearLow", "DaysHigh", "DaysLow", "DividendShare", "DividendYield", "EarningsShare", "EBITDA", "EPSEstimateCurrentYear", "EPSEstimateNextQuarter", "FiftydayMovingAverage", "MarketCapitalization", "Open", "PERatio", "PercebtChangeFromYearHigh", "PercentChange", "PercentChangeFromFiftydayMovingAverage", "PercentChangeFromTwoHundreddayMovingAverage", "PercentChangeFromYearLow", "PreviousClose", "PriceBook", "PriceEPSEstimateCurrentYear", "PriceEPSEstimateNextYear", "PriceSales", "TwoHundreddayMovingAverage", "Volume", "YearHigh", "YearLow"] 
    for stockInfo in pyqlReturn:
        for key in keys:
            print "%s : %s" % (key, stockInfo[key])
        
    



def historicPricesAsCSV(code):
    """
    function that gets historical stock prices for a provided code
    
    """

    fromDay = "2013-10-01"
    #fromDay = "2000-01-01"
    toDay = datetime.datetime.now().strftime("%Y-%m-%d")
    log.info("mining %s for historic prices [%s - %s]" % (code, fromDay, toDay))
    apiReturn = stock.get_historical_prices(code, fromDay, toDay)
    stockKeys = apiReturn.keys()
    stockKeys.sort()

    print "date,code,high,low,open,close,volume,adj_close"
    for key in stockKeys:
        log.debug("%s for %s has data %s" % (code, key, str(apiReturn[key])))
        dailyDict = json.loads(str(apiReturn[key]).replace("'", "\""))
        print "%s,%s,%s,%s,%s,%s,%s,%s" % (str(key), code, dailyDict["High"], dailyDict["Low"], dailyDict["Open"], dailyDict["Close"], dailyDict["Volume"], dailyDict["Adj Close"])



def main():
    import sys
    code = sys.argv[1]
    #multiStockAll(code)
    stockAll(code)
    #historicPricesAsCSV("CBA.AX")

if __name__ == "__main__":
    main()
