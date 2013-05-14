__doc__ = "FASTA file format tools for reading and writing"

import os
import sys

##########################

lightChainWords = ["VL", "Light"]
heavyChainWords = ["VH", "Heavy"]

CHAIN_VL = "VL"
CHAIN_VH = "VH"
CHAIN_NONE = ""
CHAIN_TYPE = {-1:CHAIN_VL, 1:CHAIN_VH, 0:CHAIN_NONE}

##########################

replaceList = [" ", "\r", "\n"]
stripList = [" ", "-", "_", "[", "<", "("]

##########################

def nucleo2acid( fd, orfShift = False ):
    from Bio.Seq import Seq

    fa = {}
    for f in fd:
        shifts = [0] if not orfShift else [0,1,2]
        for sh in shifts:
           name = f if not orfShift else "orf{0}|".format(sh) + f
           fa[name] = str(Seq(fd[f][sh:]).translate())
    return fa

##########################

def readFASTA( fileName, nucleo = False, orfShift = False ):
    fastaDict = {}

    fd = open(fileName, "r")

    fasta_name = ""
    fasta_seq = ""
    for line in fd:
        if line.startswith(">"):
            if fasta_name != "":
                for rep in replaceList:
                    fasta_seq = fasta_seq.replace(rep, "")
                fastaDict[fasta_name] = fasta_seq

            fasta_name = line[1:].strip()
            fasta_seq = ""
        else:
            fasta_seq += line.strip()

    if fasta_name != "":
        for rep in replaceList:
            fasta_seq = fasta_seq.replace(rep, "")
        fastaDict[fasta_name] = fasta_seq

    fd.close()

    if nucleo:
        return nucleo2acid(fastaDict, orfShift)

    return fastaDict


def writeFASTA( fastaDict, fd = sys.stdout, writeLen = 20 ):
    for fasta in fastaDict:
        fd.write("> " + fasta + "\n")
        fasta_seq = fastaDict[fasta]
        i = 0
        while i < len(fasta_seq):
            fd.write(fasta_seq[i:i+writeLen] + "\n")
            i += writeLen
        fd.write("\n")

##########################

def splitFASTA( fileName, outdir = None, writeLen = 20, splitCount = 100 ):
    fd = readFASTA(fileName)
    if not outdir:
        outdir = os.path.dirname(fileName)

    split_to = []
    prefix = os.path.basename(fileName)
    prefix = prefix[:prefix.rfind('.') + 1]
    prefix = os.path.join(outdir, prefix)
    fout = None

    counter = 0
    fd_tmp = {}
    for fasta in fd:
        if counter % splitCount == 0:
            if fout:
                writeFASTA(fd_tmp, fout, writeLen)
                fout.close()
            split_to.append(prefix + str(counter / splitCount) + ".fa")
            fout = open(split_to[-1], "w")
            fd_tmp = {}
        fd_tmp[fasta] = fd[fasta]
        counter += 1

    if fd_tmp:
        writeFASTA(fd_tmp, fout, writeLen)
        fout.close()

    return split_to

##########################

def getChain( fastaName ):
    chain =  0
    pos   = -1

    for word in lightChainWords:
        pos = fastaName.find(word)
        if pos != -1:
            chain += -1

    for word in heavyChainWords:
        pos = fastaName.find(word)
        if pos != -1:
            chain += 1

    return chain,pos

def getName( fastaName ):
    chain,pos = getChain(fastaName)
    if CHAIN_TYPE[chain] == CHAIN_NONE:
        return fastaName,CHAIN_TYPE[chain]

    newName = fastaName[:pos-1]
    for strp in stripList:
        newName = newName.strip(strp)

    return newName,CHAIN_TYPE[chain]

def parseFASTA2IG( fastaDict ):
    igDict     = {}
    domainDict = {}

    for fasta in fastaDict:
        chain,pos = getChain(fasta)

        if CHAIN_TYPE[chain] == CHAIN_NONE:
            domainDict[fasta] = fastaDict[fasta]
        else:
            igName,chainType = getName(fasta)
            if igName not in igDict:
                igDict[igName] = {}
            igDict[igName][CHAIN_TYPE[chain]] = fastaDict[fasta]

    return igDict,domainDict

def parseIG2FASTA( igDict, domainDict = None ):
    fastaDict = {}

    for ig in igDict:
        for domain in igDict[ig]:
            fastaName = ig + "-" + domain
            fastaDict[fastaName] = igDict[ig][domain]

    if domainDict != None:
        for domain in domainDict:
            fastaDict[domain] = domainDict[domain]

    return fastaDict
