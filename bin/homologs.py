__author__ = 'mactep'

import region_finder
import argparse

from extra.share import igblastp_tools

def printDomainHomologs( dom, useMargin = False ):
    margin = ""
    if useMargin:
        margin = " "*4

    for germ in dom.germlineDomDict:
        hom = dom.germlineDomDict[germ]
        print "{0}   ".format(margin),
        region_finder.printRegionSeqs(hom)
        print "",germ

    for homn in dom.homologDomDict:
        hom = dom.homologDomDict[homn]
        print "{0}   ".format(margin),
        region_finder.printRegionSeqs(hom)
        print "",homn

def printDomainRAH( dom, useMargin = False ):
    margin = ""
    if useMargin:
        margin = " "*4

    region_finder.printDomainRegions(dom.getDomain(), useMargin)
    printDomainHomologs(dom, useMargin)
    print "{0}   ".format(margin),
    region_finder.printRegionLabels(dom.getDomain())
    print ""

def printIgRAH( ig ):
    print "{0}:".format(ig.name)
    if ig.getVL() != None:
        printDomainRAH(ig.getVL(), True)
    if ig.getVH() != None:
        printDomainRAH(ig.getVH(), True)

def printDomainsRAH( domDict ):
    for dom in domDict:
        printDomainRAH(domDict[dom])
        print ""

def printIgsRAH( igDict ):
    for ig in igDict:
        printIgRAH(igDict[ig])
        print ""

def main():
    parser = argparse.ArgumentParser(description="Homolog View Tool")
    parser.add_argument('source', action="store", help="source FASTA file")
    parser.add_argument('-d', action="store_const", metavar="domain", dest="domain", const=igblastp_tools.DOMAIN_KABAT,
                        default=igblastp_tools.DOMAIN_IMGT, help="use KABAT domain system (default: IMGT)")
    parser.add_argument('specie', action="store", help="specie that is used to align")
    parser.add_argument('-db', action="store", metavar="database", dest="db", default=None, help="additional database name")
    parser.add_argument('-t', action="store", metavar="threads", dest="threads", default=2, type=int,
                        help="number of threads (default: 2)")
    parser.add_argument('-n', action="store", metavar="alignments", dest="alignments", default=0, type=int,
                        help="number of alignments (default: BLAST+ default)")

    args = parser.parse_args()

    res = igblastp_tools.runIgBlastp(args.source, args.specie, args.domain, args.db,
                                     args.threads, args.alignments )
    igDict,domDict = igblastp_tools.parseIgBlastpOut(res, args.source)

    printIgsRAH(igDict)
    printDomainsRAH(domDict)

if __name__ == "__main__":
    main()