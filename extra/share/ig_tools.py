__doc__ = "IG domain classes and tools for reading and writing"

class Domain(object):
    def __init__(self, domain):
        self.name = domain[0]
        self.seq  = domain[1]
        self.score = 0
        self.same = (0,0)

        self.cdr = ["", "", ""]
        self.fr  = ["", "", ""]
        self.tail = ""

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def setCDR(self, number, val):
        number -= 1
        if number < 0 or number > 2:
            return
        self.cdr[number] = val

    def setFR(self, number, val):
        number -= 1
        if number < 0 or number > 2:
            return
        self.fr[number] = val

    def setTail(self, tail):
        self.tail = tail

    def getCDR(self, number):
        number -= 1
        if number < 0 or number > 2:
            return None
        return self.cdr[number]

    def getFR(self, number):
        number -= 1
        if number < 0 or number > 2:
            return None
        return self.fr[number]

    def getTail(self):
        return self.tail

    def set(self, region, val):
        number = int(region[-1])
        if region.upper().startswith("CDR"):
            self.setCDR(number, val)
        elif region.upper().startswith("FR"):
            self.setFR(number, val)

    def setByN(self, n, val):
        if n % 2 == 0:
            self.setFR(n/2 + 1, val)
        elif n < 6:
            self.setCDR(n/2 + 1, val)
        else:
            self.setTail(val)

    def getByN(self, n):
        if n % 2 == 0:
            self.getFR(n/2 + 1)
        elif n < 6:
            self.getCDR(n/2 + 1)
        else:
            self.getTail()

    def get(self, region):
        number = int(region[-1])
        if region.upper().startswith("CDR"):
            return self.getCDR(number)
        elif region.upper().startswith("FR"):
            return self.getFR(number)
        return None

    def getRegionByPos(self, pos):
        npos = pos
        for reg in ["FR1", "CDR1", "FR2", "CDR2", "FR3", "CDR3"]:
            region = self.get(reg)
            if npos < len(region):
                return reg, region[npos]
            npos -= len(region)
        return None

    def generatedSeq(self):
        return self.fr[0] + self.cdr[0] + self.fr[1] + self.cdr[1] + self.fr[2] + self.cdr[2] + self.tail

# class Ig(object):
# 	def __init__(self, name):
# 		self.name = name
# 		self.vl   = None
# 		self.vh   = None

# 	def setVL(self, vl):
# 		self.vl = vl

# 	def setVH(self, vh):
# 		self.vh = vh

# 	def getVL(self):
# 		return self.vl

# 	def getVH(self):
# 		return self.vh

# 	def set(self, domainName, domain):
# 		if domainName == "VL":
# 			self.setVL(domain)
# 		elif domainName == "VH":
# 			self.setVH(domain)

# 	def get(self, domainName):
# 		if domainName == "VL":
# 			return self.getVL()
# 		elif domainName == "VH":
# 			return self.getVH()
# 		return None		

##########################

def domain2domainClass( domain ):
    return Domain((domain[0], domain[1]))

# def ig2igClass( ig ):
# 	igClass = Ig(ig[0])
# 	for domain in ig[1]:
# 		ifClass.set(domain, ig[1][domain])

# 	return igClass

def domainDict2domainClassList( domainDict ):
    domainList = []
    for domain in domainDict:
        domainList.append(domain2domainClass((domain, domainDict[domain])))
    return domainList

# def igDict2igClassList( igDict ):
# 	igList = []
# 	for ig in igDict:
# 		igList.append(ig2igClass((ig, igDict[ig])))

# 	return igList

##########################

def domainClass2domain( domainClass ):
    return (domainClass.name, domainClass.seq)

# def igClass2ig( igClass ):
# 	ig = (igClass.name, {})
# 	for domainName in ["VL", "VH"]:
# 		domain = igClass.get(domainName)
# 		if domain != None:
# 			ig[1][domain.name] = domain.seq

# 	return ig

def domainClassList2domainDict( domainList ):
    domainDict = {}
    for domain in domainList:
        domainDict[domain.name] = domain.seq
    return domainDict

# def igClassList2igDict( igList ):
# 	igDict = {}
# 	for igClass in igList:
# 		ig = igClass2ig(igClass)
# 		igDict[ig[0]] = ig[1]

# 	return igDict

##########################