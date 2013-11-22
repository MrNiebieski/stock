# Kavin Autar
# 2013/11/19
# Version 1.0
# Checks stocks



import ystockquote as stock
import datetime
import logger as log
import json
import db
#Global vars

def getHistoricInfo(ycode):
    code = ycode.split(".")[0]
    fromDay = "2000-01-01"
    #fromDay = "2013-11-19"
    toDay = datetime.datetime.now().strftime("%Y-%m-%d")
    log.info("getting historic [%s - %s] data for %s" % (fromDay, toDay, ycode))
    
    try:
        stockData = stock.get_historical_prices(ycode, fromDay, toDay)
    except:
        log.error("Unable to get historic data for %s" % ycode)
        return None

    historicDataQuery = """INSERT INTO HISTORIC_DATA
(DATE,
CODE,
HIGH,
LOW,
OPEN,
VOLUME)
VALUES (%s, %s, %s, %s, %s, %s);"""

    days = stockData.keys()

    for day in days:
        date = str(day)
        data = stockData[day]
#        print data, type(data)
        historicValues = [date,
                            code,
                            data['High'],
                            data['Low'],
                            data['Open'],
                            data['Volume']]

        db.insertSingle(historicDataQuery, historicValues)



def main():
    import sys
    code = sys.argv[1]
    getHistoricInfo(code)

if __name__ == "__main__":
    main()
