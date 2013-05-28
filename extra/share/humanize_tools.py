__author__ = 'mactep'

import sys
import extra.methods
from extra.methods import *


def getMethods():
    return {m[m.find('_')+1:]: sys.modules[m] for m in sys.modules if m.startswith(extra.methods.__name__ + ".method")}


def runMethod(domain, method):
    methods = getMethods()
    methods[method].humanization_algorithm(domain)


def makeFastaDict(domain):
    d = ["FR1", "CDR1", "FR2", "CDR2", "FR3", "CDR3"]
    tail = domain.getDomain().getTail()
    fd = {}
    dhdd = domain.humanizeDomDict
    for h in dhdd:
        hum = dhdd[h]
        n = h + " " + "-".join(str(len(hum.get(i))) for i in d)
        fd[n] = "".join(hum.get(i) for i in d) + tail
    return fd
