# Kavin Autar
# 2013/11/17
# Version 1.0
# Checks stocks


import pyql
import logger as log


def multiStockAll(codes):
    """
    function takes a list of codes and provides information via pyql
    """

    log.info("mining list [ %s ] for all information via pyql" % " : ".join(codes))

    return pyql.lookup(codes)


def main():
    import sys
    code = sys.argv[1]
    #multiStockAll(code)
    stockAll(code)
    #historicPricesAsCSV("CBA.AX")

if __name__ == "__main__":
    main()
