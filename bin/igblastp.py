__author__ = 'mactep'

import os
import argparse

from extra.share import igblastp_tools

def main():
    parser = argparse.ArgumentParser(description="Fast IgBlastp Run Tool")
    parser.add_argument('source', action="store", help="source FASTA file")
    parser.add_argument('-d', action="store_const", metavar="domain", dest="domain", const=igblastp_tools.DOMAIN_KABAT,
                        default=igblastp_tools.DOMAIN_IMGT, help="use KABAT domain system (default: IMGT)")
    parser.add_argument('specie', action="store", help="specie that is used to align")
    parser.add_argument('-db', action="store", metavar="database", dest="db", default=None, help="additional database name")
    parser.add_argument('-t', action="store", metavar="threads", dest="threads", default=2, type=int,
                        help="number of threads (default: 2)")
    parser.add_argument('-n', action="store", metavar="alignments", dest="alignments", default=0, type=int,
                        help="number of alignments (default: BLAST+ default)")
    parser.add_argument('-f', action="store", metavar="outfmt", dest="outfmt", default=3, type=int,
                        help="output format (default: 3)")
    parser.add_argument('-o', metavar="out", action="store", dest="out", default=None, help="output file (default: stdout)")

    args = parser.parse_args()

    if( args.out != None ):
        args.out = os.path.join(os.path.abspath(os.path.curdir), args.out)

    print igblastp_tools.runIgBlastp(args.source, args.specie, args.domain, args.db,
                                    args.threads, args.alignments, args.outfmt, args.out )

if __name__ == "__main__":
    main()