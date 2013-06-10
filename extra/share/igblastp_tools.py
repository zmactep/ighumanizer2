__doc__ = "Tools for working with IgBLASTP"

import os

import iterpipes

##########################

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

IGBLAST_DIR  = "ncbi-igblast"
IGBLAST_PATH = os.path.join(ROOT_PATH, IGBLAST_DIR)

IGBLAST_BIN = "bin"
IGBLAST_GERMLINE = "database"

BLASTDB_DIR  = "database"
BLASTDB_PATH = os.path.join(ROOT_PATH, BLASTDB_DIR)

##########################

GERMLINE_HUMAN = "human"
GERMLINE_MOUSE = "mouse"

DOMAIN_KABAT = "kabat"
DOMAIN_IMGT  = "imgt"

##########################

PARSELINE_QUERY    = "Query="
PARSELINE_DOMAIN   = "Domain classification requested"
PARSELINE_FWR3     = "FWR3"
PARSELINE_CDR3     = "CDR3 (V region only)"
PARSELINE_TOTAL    = "Total"
PARSELINE_ALIGN    = "Alignment"
PARSELINE_LAMBDA   = "Lambda"

##########################

DBTYPE_LOCAL = "lcl"

##########################

from . import fasta_tools
from . import ig_tools

#fasta_tools = loader.loadModule(loader.SHARE_PATH, 'fasta_tools.py')
#ig_tools    = loader.loadModule(loader.SHARE_PATH, 'ig_tools.py')

##########################


class BlastOutDomain(object):
    def __init__(self, domain):
        self.domain = domain

        self.domainModel = None
        self.germlineDomDict = {}
        self.homologDomDict  = {}
        self.humanizeDomDict = {}

    def getDomain(self):
        return self.domain


class BlastOutIg(object):
    def __init__(self, name):
        self.name = name
        self.vl   = None
        self.vh   = None

    def setVL(self, vl):
        self.vl = vl

    def getVL(self):
        return self.vl

    def setVH(self, vh):
        self.vh = vh

    def getVH(self):
        return self.vh

    def set(self, domainName, domain):
        if domainName == "VL":
            self.setVL(domain)
        elif domainName == "VH":
            self.setVH(domain)

    def get(self, domainName):
        if domainName == "VL":
            return self.getVL()
        elif domainName == "VH":
            return self.getVH()
        return None

##########################



##########################

def runIgBlastp( query, germlineSpecie = GERMLINE_HUMAN, domainSystem = DOMAIN_IMGT,
                 additionalDB = None, numThreads = 4, numAlignments = 10, outfmt = 3, out = None ):
    igblastp = os.path.join(os.path.join('.', IGBLAST_BIN), "igblastp")
    params = []

    if query == "" or germlineSpecie == "" or domainSystem not in [DOMAIN_IMGT, DOMAIN_KABAT]:
        return None

    # Query
    query = os.path.abspath(query)
    igblastp += " -query {}"
    params.append(query)

    # Germline
    germlineSpecie = "{0}/{1}_gl_V".format(IGBLAST_GERMLINE, germlineSpecie)
    igblastp += " -germline_db_V {}"
    params.append(germlineSpecie)

    # Domain
    igblastp += " -domain_system {}"
    params.append(domainSystem)

    # Database
    if additionalDB != None:
        additionalDB = os.path.join(BLASTDB_PATH, additionalDB)
        igblastp += " -db {}"
        params.append(additionalDB)

    # Threads
    igblastp += " -num_threads {}"
    params.append(str(numThreads))

    # Alignments
    igblastp += " -num_alignments {}"
    params.append(str(numAlignments))

    # Output format
    igblastp += " -outfmt {}"
    params.append(str(outfmt))

    # Output file
    if out != None:
        igblastp += " -out {}"
        params.append(out)

    # RUN IGBLASTP
    cur = os.path.curdir
    os.chdir(IGBLAST_PATH)
    runLine = iterpipes.linecmd(igblastp, *params)
    result = iterpipes.run(runLine)
    os.chdir(cur)

    returnResult = ""
    for line in result:
        returnResult += line

    return returnResult

##########################

def parseHomologList( lines, blastOutDomain ):
    for homLine in lines:
        hom = homLine.split()
        
        name,score = hom[0],hom[-2]
        dbName = name.split("|")[0]

        shortName = name[name.find('|')+1:]
        vPos = shortName.find('|')
        if vPos != -1:
            if vPos == 0:
                shortName = shortName[1:]
            else:
                shortName = shortName.replace('|','_')
        vPos = shortName.find('.')
        if vPos != -1:
            shortName = shortName[:vPos]


        domain = ig_tools.Domain((name, ""))
        domain.setScore(score)

        if dbName == DBTYPE_LOCAL:
            blastOutDomain.germlineDomDict[shortName] = domain
        else:
            blastOutDomain.homologDomDict[shortName] = domain

def parseAlignmentRegions( regionLine, regions, rEndReached ):
    regionsTmp = [len(x)+1 for x in regionLine.split('>')]
    if not regionLine.endswith('>'):
        regionsTmp[-1] -= 1
    if regionsTmp[-1] == 1:
        regionsTmp = regionsTmp[:-1]

    if rEndReached:
        regions.append(regionsTmp[0])
    else:
        regions[-1] += regionsTmp[0]

    regionsTmp = regionsTmp[1:]
    for region in regionsTmp:
        regions.append(region)

    if regionLine.endswith('>'):
        return True

    return False

def fixHomologBySeq( homSeq, seq ):
    if len(homSeq) != len(seq):
        return homSeq

    homNSeq = list(homSeq)
    for i in xrange(len(homNSeq)):
        if homNSeq[i] == '.':
            homNSeq[i] = seq[i]

    return "".join(homNSeq)

def createRegions( domain, regions, seq ):
    seqTmp = seq
    for i in xrange(len(regions)):
        domain.setByN(i, seqTmp[:regions[i]])
        seqTmp = seqTmp[regions[i]:]
    domain.setTail(seqTmp)


def parseAlignmentList( lines, blastOutDomain, cdr3Len ):
    # Count block numbers
    blockRanges = []
    bc = 0
    for line in lines:
        if PARSELINE_QUERY[:-1] in line:
            blockRanges.append(bc-1)
        bc += 1

    # Make blocks
    blocks = []
    for i in xrange(len(blockRanges)-1):
        blocks.append(lines[blockRanges[i]:blockRanges[i+1]])

    # Parse regions and query aligned seq
    regions = []
    rEndReached = True
    queryLine = ""
    for block in blocks:
        # Parse regions
        rEndReached = parseAlignmentRegions(block[0].strip(), regions, rEndReached)

        # Parse query seq
        queryLine += block[1].strip().split()[-2]

        # Parse homologs
        homs = block[2:]
        for hom in homs:
            homList = hom.strip().split()
            seq = homList[-2]
            sN = 2
            nN = 3
            if homList[0] != "V":
                sN -= 1
                nN -= 1
            same = [int(x) for x in homList[sN][1:-1].split('/')]
            name = homList[nN]

            if name in blastOutDomain.germlineDomDict:
                blastOutDomain.germlineDomDict[name].same =  (same[0], same[1])
                blastOutDomain.germlineDomDict[name].seq  += seq
            elif name in blastOutDomain.homologDomDict:
                blastOutDomain.homologDomDict[name].same =  (same[0], same[1])
                blastOutDomain.homologDomDict[name].seq  += seq
    if len(regions) < 6:
        regions.append(cdr3Len)

    # Fill regions in domain
    createRegions(blastOutDomain.getDomain(), regions, queryLine)

    # Fill homologs and fix sequences
    for i in xrange(len(regions)):
        for germName in blastOutDomain.germlineDomDict:
            germ = blastOutDomain.germlineDomDict[germName]
            germ.seq = fixHomologBySeq(germ.seq, queryLine)
            createRegions(germ, regions, germ.seq)
        for homName in blastOutDomain.homologDomDict:
            hom = blastOutDomain.homologDomDict[homName]
            hom.seq = fixHomologBySeq(hom.seq, queryLine)
            createRegions(hom, regions, hom.seq)


def parseIgBlastpDomain( domain, lines ):
    blastOutDomain = BlastOutDomain(domain)

    # Optimize
    lines = filter( lambda x : x != u'' and x != u'\r', lines )
    lines = lines[3:]

    # Find homolog lines
    lineCounter = 0
    while not lines[lineCounter].startswith(PARSELINE_DOMAIN):
        lineCounter += 1

    # Parse homolog list
    parseHomologList(lines[:lineCounter], blastOutDomain)

    # Parse domain system
    blastOutDomain.domainModel = lines[lineCounter].split()[-1]

    # Search for CDR3 length
    lineCounter = 0
    while lineCounter < len(lines) and not lines[lineCounter].startswith(PARSELINE_CDR3):
        lineCounter += 1
    if lineCounter < len(lines):
        cdr3Len = int(lines[lineCounter].split()[-5])
        lines = lines[lineCounter:]
    else:
        cdr3Len = 0
        lineCounter = 0
        while not lines[lineCounter].startswith(PARSELINE_TOTAL):
            lineCounter += 1
        lines = lines[lineCounter:]

    # Optimize
    lineCounter = 0
    while not lines[lineCounter].startswith(PARSELINE_ALIGN):
        lineCounter += 1
    lines = lines[lineCounter+1:]
    lineCounter = 0
    while not lines[lineCounter].startswith(PARSELINE_LAMBDA):
        lineCounter += 1
    lines = lines[:lineCounter]

    # Parse homolog alignments
    parseAlignmentList(lines, blastOutDomain, cdr3Len)

    # Filter homologs
    newHomDict = {}
    for hom in blastOutDomain.homologDomDict:
        if blastOutDomain.homologDomDict[hom].fr[0] != "":
            newHomDict[hom] = blastOutDomain.homologDomDict[hom]
    blastOutDomain.homologDomDict = newHomDict

    return blastOutDomain

def parseIgBlastpOut( igblastOut, query ):
    if igblastOut == None:
        return None

    fastaDict = fasta_tools.readFASTA(query)
    igDict,domainDict = fasta_tools.parseFASTA2IG(fastaDict)
    del fastaDict

    blastOutDomainDict = {}
    blastOutIgDict     = {}

    igblastResults = igblastOut.split(PARSELINE_QUERY)[1:]

    for igblastResult in igblastResults:
        lines = igblastResult.split("\n")
        fastaName,chainType = fasta_tools.getName(lines[0].strip())
        lines = lines[1:]

        if chainType == fasta_tools.CHAIN_NONE:
            # domainDict usage
            if fastaName not in domainDict:
                continue

            domain = ig_tools.domain2domainClass((fastaName, domainDict[fastaName]))
            blastOutDomainDict[fastaName] = parseIgBlastpDomain(domain, lines)
        else:
            # igDict usage
            if fastaName not in igDict:
                continue

            if fastaName not in blastOutIgDict:
                blastOutIgDict[fastaName] = BlastOutIg(fastaName)

            domain = ig_tools.domain2domainClass((chainType, igDict[fastaName][chainType]))
            blastOutIgDict[fastaName].set(chainType, parseIgBlastpDomain(domain, lines))

    return blastOutIgDict, blastOutDomainDict
