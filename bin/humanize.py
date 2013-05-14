__author__ = 'mactep'

import sys
import os
import argparse

import region_finder

from extra.share import fasta_tools, ig_tools, igblastp_tools, humanize_tools

def printDomainHumanizations( dom, useMargin = False ):
    margin = ""
    if useMargin:
        margin = " "*4

    for humn in dom.humanizeDomDict:
        hum = dom.humanizeDomDict[humn]
        print "{0}   ".format(margin),
        region_finder.printRegionSeqs(hum)
        print "",humn

def printDomainRAH( dom, useMargin = False ):
    margin = ""
    if useMargin:
        margin = " "*4

    region_finder.printDomainRegions(dom.getDomain(), useMargin)
    printDomainHumanizations(dom, useMargin)
    print "{0}   ".format(margin),
    region_finder.printRegionLabels(dom.getDomain())
    print ""

def printIgRAH( ig ):
    print "{0}:".format(ig.name)
    if ig.getVL() != None:
        printDomainRAH(ig.getVL(), True)
    if ig.getVH() != None:
        printDomainRAH(ig.getVH(), True)

def main():
    parser = argparse.ArgumentParser(description="FASTA Filter Tool")
    parser.add_argument('source', action="store", help="source FASTA file")
    parser.add_argument('method', action="store", help="method to humanize")
    parser.add_argument('-s', metavar="specie", dest="specie", default=igblastp_tools.GERMLINE_HUMAN,
                        action="store", help="specie that is used to align (default: human)")
    parser.add_argument('-d', action="store_const", metavar="domain", dest="domain", const=igblastp_tools.DOMAIN_KABAT,
                        default=igblastp_tools.DOMAIN_IMGT, help="use KABAT domain system (default: IMGT)")
    parser.add_argument('-db', action="store", metavar="database", dest="db", default=None, help="additional database name")
    parser.add_argument('-t', action="store", metavar="threads", dest="threads", default=2, type=int,
                        help="number of threads (default: 2)")
    parser.add_argument('-n', action="store", metavar="alignments", dest="alignments", default=0, type=int,
                        help="number of alignments (default: BLAST+ default)")
    parser.add_argument('-k', action="store", metavar="threshold", dest="k", default=50, type=float,
                        help="threshold to filter domains (default: 50)")
    parser.add_argument('out', action="store", help="output directory")

    args = parser.parse_args()

    methods = humanize_tools.getMethods()
    if args.method not in methods:
        print "Available humanization methods:"
        for m in methods:
            print "     {0}: {1}".format(m, methods[m].__doc__)
        exit()

    res = igblastp_tools.runIgBlastp(args.source, args.specie, args.domain, args.db,
                                     args.threads, args.alignments )
    igDict,domDict = igblastp_tools.parseIgBlastpOut(res, args.source)

    for i in igDict:
        ig = igDict[i]
        p = os.path.join(args.out, ig.name)
        os.mkdir(p, 0775)
        for dom in [ig.getVL(), ig.getVH()]:
            humanize_tools.runMethod(dom, args.method)
            fd = open(os.path.join(p, dom.getDomain().name) + ".fa", "w")
            dic = humanize_tools.makeFastaDict(dom)
            fasta_tools.writeFASTA(dic, fd)
            fd.close()
        # Logging
        printIgRAH(ig)
        print ""
    for d in domDict:
        dom = domDict[d]
        humanize_tools.runMethod(dom, args.method)
        fd = open(os.path.join(args.out, dom.getDomain().name) + ".fa", "w")
        dic = humanize_tools.makeFastaDict(dom)
        fasta_tools.writeFASTA(dic, fd)
        fd.close()
        # Logging
        printDomainRAH(dom)
        print ""


if __name__ == "__main__":
    main()