__author__ = 'mactep'

import os
from extra.share.igblastp_tools import runIgBlastp, parseIgBlastpOut


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