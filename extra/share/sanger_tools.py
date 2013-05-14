__author__ = 'mactep'

from Bio import SeqIO

def abi2fastq( in_fileName, out_fileName ):
    input_handle  = open(in_fileName, "rb")
    output_handle = open(out_fileName, "w")

    seqs = SeqIO.parse(input_handle, "abi")
    count = SeqIO.write(seqs, output_handle, "fastq")

    input_handle.close()
    output_handle.close()

    return count

def readQualityUniversal( fileName, fileType, fileMode = "r" ):
    qDict = {}
    fd = open(fileName, fileMode)
    seqs = SeqIO.parse(fd, fileType)
    for seq in seqs:
        qDict[seq.id] = (str(seq.seq), seq.letter_annotations["phred_quality"])
    return qDict

def readFastq( fileName ):
    return readQualityUniversal(fileName, "fastq")

def readAbi( fileName ):
    return readQualityUniversal(fileName, "abi", "rb")

def filterFqDict( fastqDict, qualSD = 0.25, threashold = 40, length = 700, asym = -70 ):
    ffastqDict = {}
    for fq in fastqDict:
        seq = fastqDict[fq][0]
        qual = fastqDict[fq][1]
        max_val = max(qual)
        if max_val < threashold:
            continue
        down_val = max_val * (1 - qualSD)
        l,r = 0,len(qual)-1
        # Get left
        while l < len(qual) and qual[l] < down_val:
            l += 1
        # Get right
        while r >= 0 and qual[r] < down_val:
            r -= 1
        m = (r + l) / 2 + asym
        r = m + length / 2
        l = m - length / 2
        ffastqDict[fq] = (seq[l:r],qual[l:r])
        print "LEFT: {0} / RIGHT: {1}".format(l, r)
    return ffastqDict

def fqDict2faDict( fastqDict ):
    fastaDict = {}
    for fq in fastqDict:
        fastaDict[fq] = fastqDict[fq][0]
    return fastaDict


#######################################################

def test():
    fq = readFastq("/home/mactep/Downloads/test.fastq")
    ffq = filterFqDict(fq)
    return ffq