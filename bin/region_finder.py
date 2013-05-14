__author__ = 'mactep'

import argparse

from extra.share import igblastp_tools

def printRegionLabels( dom ):
    for i in [1,2,3]:
        FR_S = "FR"
        CDR_S = "CDR"

        if len(dom.getFR(i)) > 0:
            FR_S = FR_S[:(len(dom.getFR(i))-1)]
        if len(dom.getCDR(i)) > 0:
            CDR_S = CDR_S[:(len(dom.getCDR(i))-1)]

        space = len(dom.getFR(i)) - (len(FR_S) + 1)
        print "{0}{1}".format("{0}{1}".format(FR_S, i), " "*space),

        if len(dom.getCDR(i)) > 0:
            space = len(dom.getCDR(i)) - (len(CDR_S) + 1)
            print "{0}{1}".format("{0}{1}".format(CDR_S, i), " "*space),
        else:
            print "",

def printRegionSeqs( dom ):
    for i in [1,2,3]:
        print "{0} {1}".format(dom.getFR(i), dom.getCDR(i)),

def printDomainRegions( dom, useMargin = False ):
    margin = ""
    if useMargin:
        margin = " "*4

    print "{0}{1}:".format(margin, dom.name),
    print "{0}".format(dom.seq)


    print "{0}   ".format(margin),
    printRegionLabels(dom)
    print ""

    print "{0}   ".format(margin),
    printRegionSeqs(dom)
    print ""

    print "{0}   ".format(margin),
    printRegionLabels(dom)
    print ""

def printIgRegions( ig ):
    print "{0}:".format(ig.name)
    if ig.getVL() != None:
        printDomainRegions(ig.getVL().getDomain(), True)
    if ig.getVH() != None:
        printDomainRegions(ig.getVH().getDomain(), True)

def printDomainsRegions( domDict ):
    for dom in domDict:
        printDomainRegions(domDict[dom].getDomain())
        print ""

def printIgsRegions( igDict ):
    for ig in igDict:
        printIgRegions(igDict[ig])
        print ""


def main():
    parser = argparse.ArgumentParser(description="Region Finding Tool")
    parser.add_argument('source', action="store", help="source FASTA file")
    parser.add_argument('-d', action="store_const", metavar="domain", dest="domain", const=igblastp_tools.DOMAIN_KABAT,
                        default=igblastp_tools.DOMAIN_IMGT, help="use KABAT domain system (default: IMGT)")
    parser.add_argument('-s', metavar="specie", dest="specie", default=igblastp_tools.GERMLINE_HUMAN,
                        action="store", help="specie that is used to align (default: human)")

    args = parser.parse_args()

    res = igblastp_tools.runIgBlastp(args.source, args.specie, args.domain)
    igDict,domDict = igblastp_tools.parseIgBlastpOut(res, args.source)

    printIgsRegions(igDict)
    printDomainsRegions(domDict)

if __name__ == "__main__":
    main()