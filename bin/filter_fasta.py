__author__ = 'mactep'

import sys
import argparse

from extra.share import fasta_tools, igblastp_tools

def filterAndConvDom( dom, k ):
    max_k = 0
    if dom == None:
        return False

    for g in dom.germlineDomDict:
        hom = dom.germlineDomDict[g]
        kk = float(hom.same[0])/hom.same[1]
        if kk > max_k:
            max_k = kk

    for g in dom.homologDomDict:
        hom = dom.homologDomDict[g]
        kk = float(hom.same[0])/hom.same[1]
        if kk > max_k:
            max_k = kk

    if max_k >= k:
        return dom.getDomain().name,dom.getDomain().seq

    return False

def filterAndConvIg( ig, k ):
    igconv = {}

    for dom in [ig.getVL(), ig.getVH()]:
        res = filterAndConvDom(dom, k)
        if res != False:
            igconv[res[0]] = res[1]
        else:
            return False

    return ig.name,igconv

def processSource( source, args ):
    k = args.k / 100.0
    res = igblastp_tools.runIgBlastp(source, args.specie, args.domain, args.db, args.threads, args.alignments)
    igDict,domDict = igblastp_tools.parseIgBlastpOut(res, source)

    igCFDict = {}
    domCFDict = {}

    for ig in igDict:
        igCF = filterAndConvIg(igDict[ig], k)
        if igCF != False:
            igCFDict[igCF[0]] = igCF[1]

    for dom in domDict:
        domCF = filterAndConvDom(domDict[dom], k)
        if domCF != False:
            domCFDict[domCF[0]] = domCF[1]
    return igCFDict,domCFDict

def main():
    parser = argparse.ArgumentParser(description="FASTA Filter Tool")
    parser.add_argument('source', action="store", nargs="+", help="source FASTA files")
    parser.add_argument('-d', action="store_const", metavar="domain", dest="domain", const=igblastp_tools.DOMAIN_KABAT,
                        default=igblastp_tools.DOMAIN_IMGT, help="use KABAT domain system (default: IMGT)")
    parser.add_argument('-s', metavar="specie", dest="specie", default=igblastp_tools.GERMLINE_HUMAN,
                        action="store", help="specie that is used to align (default: human)")
    parser.add_argument('-db', action="store", metavar="database", dest="db", default=None, help="additional database name")
    parser.add_argument('-t', action="store", metavar="threads", dest="threads", default=2, type=int,
                        help="number of threads (default: 2)")
    parser.add_argument('-n', action="store", metavar="alignments", dest="alignments", default=0, type=int,
                        help="number of alignments (default: BLAST+ default)")
    parser.add_argument('-l', action="store", metavar="count", dest="split", default=None, type=int,
                        help="split each input file to parts (default: False)")
    parser.add_argument('-k', action="store", metavar="threshold", dest="k", default=50, type=float,
                        help="threshold to filter domains (default: 50)")
    parser.add_argument('-o', metavar="out", action="store", dest="out", default=None, help="output file (default: stdout)")

    args = parser.parse_args()

    igCFDict = {}
    domCFDict = {}
    for source in args.source:
        if args.split:
            source_list = fasta_tools.splitFASTA(source, splitCount=args.split)
            for s in source_list:
                tmp_igD,tmp_domD = processSource(s, args)
                igCFDict.update(tmp_igD)
                domCFDict.update(tmp_domD)
        else:
            tmp_igD,tmp_domD = processSource(source, args)
            igCFDict.update(tmp_igD)
            domCFDict.update(tmp_domD)

    fout = sys.stdout
    if args.out != None:
        fout = open(args.out,"w")

    fastaDict = fasta_tools.parseIG2FASTA(igCFDict, domCFDict)
    fasta_tools.writeFASTA(fastaDict, fout)

    if args.out != None:
        fout.close()

if __name__ == "__main__":
    main()