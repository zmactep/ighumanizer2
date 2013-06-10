__author__ = 'mactep'

import os
import tempfile
from extra.share.fasta_tools import writeFASTA
from extra.share.igblastp_tools import runIgBlastp, parseIgBlastpOut

temp_file_name = "ighumanizer2_131291.fa"

class FastaModel(object):
    def __init__(self, models):
        # structure: {model : { filename : { igs, domains } } }
        self.models = [model.lower() for model in models]
        self.data = {model: {} for model in self.models}

    def getData(self):
        return self.data

    def loadData(self, fileList):
        self.data = {model: {} for model in self.models}
        for model in self.models:
            for filename in fileList:
                basefilename = os.path.basename(str(filename))
                basefilename = basefilename[:basefilename.rfind('.')]
                res = runIgBlastp(query=str(filename), domainSystem=model)
                self.data[model][basefilename] = parseIgBlastpOut(res, str(filename))

    def rerunBLAST(self, domain, configuration):
        path = os.path.join(tempfile.gettempdir(), temp_file_name)
        fd = open(path, "wt")
        self.saveDomain(domain, fd)
        fd.close()
        if configuration.getDBPath():
            res = runIgBlastp(path, configuration.getSpecie(), domain.domainModel,
                              configuration.getDBPath(), configuration.getNumThreads(),
                              configuration.getNumAlignments())
            newdomain = parseIgBlastpOut(res, path)[1].values()[0]
            domain.germlineDomDict = newdomain.germlineDomDict
            domain.homologDomDict = newdomain.homologDomDict
        os.unlink(path)

    def rerunTotalBLAST_slow(self, configuration):
        for model in self.data:
            for baseName in self.data[model]:
                for igName in self.data[model][baseName][0]:
                    for dom in self.data[model][baseName][0][igName]:
                        self.rerunBLAST(self.data[model][baseName][0][igName][dom], configuration)
                for dom in self.data[model][baseName][1]:
                    self.rerunBLAST(self.data[model][baseName][1][dom], configuration)

    def saveDomain(self, domain, fd):
        if not domain:
            return
        fdict = {domain.getDomain().name: domain.getDomain().seq}
        writeFASTA(fdict, fd)

    def saveTotalDomains(self, fd):
        data = self.data[self.models[0]]
        for baseName in data:
            for igName in data[baseName][0]:
                for domName in data[baseName][0][igName]:
                    fdict = {baseName + "/$/" + igName + "/$/" + domName: data[baseName][0][igName][domName]}
                    writeFASTA(fdict, fd)
            for domName in data[baseName][1]:
                fdict = {baseName + "/$/" + domName: data[baseName][1][domName]}
                writeFASTA(fdict, fd)


    def cleanup(self):
        self.data = {model: {} for model in self.models}

    def getDomain(self, baseName, igName, domainName, domainModel):
        try:
            lookup = self.data[domainModel][baseName]
            if igName:
                return lookup[0][igName].get(domainName)
            else:
                return lookup[1][domainName]
        except (IndexError, TypeError):
            return None