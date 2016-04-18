import sys 
import math



trainInput = open(sys.argv[1],'r')
TrainText = trainInput.read().strip()
trainList = []

for line in TrainText.splitlines():
    trainList.append(line)


#Create Vocabulary
vocabulary = set()

for f in trainList:
    targetFile = open(f, 'r').read().strip().lower()
    targetText = targetFile.splitlines()
    for fileWord in targetText:
        vocabulary.add(fileWord)


#Calculate P(vj)
conCount = 0
libCount = 0
examples = len(trainList) 

for party in trainList:
    if "con" in party:
        conCount += 1
    elif "lib" in party:
        libCount += 1
Pcon = conCount * 1.0 / examples
Plib = libCount * 1.0 / examples

#Calculate P(wk|vj)

TEXTcon = []
TEXTlib = []



for f2 in trainList:
    if 'con' in f2:
        conFile = open(f2, 'r').read().strip().lower()
        conText = conFile.splitlines()
        for conWord in conText:
            TEXTcon.append(conWord)
    elif 'lib' in f2:
        libFile = open(f2, 'r').read().strip().lower()
        libText = libFile.splitlines()
        for libWord in libText:
            TEXTlib.append(libWord)

dictCon = dict()
dictLib = dict()
for c in TEXTcon:
    if c in dictCon:
        dictCon[c] += 1
    elif c not in dictCon:
        dictCon[c] = 1

for l in TEXTlib:
    if l in dictLib:
        dictLib[l] += 1
    elif l not in dictLib:
        dictLib[l] = 1

Pconword = dict()
Plibword = dict()
conWordList = list()
libWordList = list()

for word in dictCon:
    if word in vocabulary:
        p1 = (dictCon[word] + 1) * 1.0 / (len(TEXTcon) + len(vocabulary))
        Pconword[word] = p1
        conWordList.append(p1)

for word1 in dictLib:
    if word1 in vocabulary:
        p2 = (dictLib[word1] + 1) * 1.0 / (len(TEXTlib) + len(vocabulary))
        Plibword[word1] = p2
        libWordList.append(p2)

oddslib = dict()
oddsCon = dict()
oddslibList = []
oddsconList = []

for oddsWord in Plibword:
    if oddsWord in Pconword:
        oddslib[oddsWord] = math.log(Plibword[oddsWord] * 1.0 / Pconword[oddsWord])
    elif oddsWord not in Pconword:
        oddsPcon = (1.0 / (len(TEXTcon) + len(vocabulary)))
        oddslib[oddsWord] = math.log(Plibword[oddsWord] * 1.0 / oddsPcon)
    oddslibList.append(oddslib[oddsWord])

for oddsWord2 in Pconword:
    if oddsWord2 in Plibword:
        oddsCon[oddsWord2] = math.log(Pconword[oddsWord2] * 1.0 / Plibword[oddsWord2])
    elif oddsWord2 not in Plibword:
        oddsPlib = (1.0 / (len(TEXTlib) + len(vocabulary)))
        oddsCon[oddsWord2] = math.log(Pconword[oddsWord2] * 1.0 / oddsPlib)
    oddsconList.append(oddsCon[oddsWord2])




printListConNum = []
printListConVal = []
printListLibNum = []
printListLibVal = []
i = -1 

b = sorted(oddslibList)

while(i >= -20):
    value = b[i]
    for key in oddslib:
        if oddslib[key] == value:
            printListLibNum.append(value)
            printListLibVal.append(key)
            i -= 1



j = -1 

a = sorted(oddsconList)

while(j >= -20):
    value2 = a[j]
    for key2 in oddsCon:
        if oddsCon[key2] == value2:
            printListConNum.append(value2)
            printListConVal.append(key2)
            j -= 1



for time in range(0, 20):
    sys.stdout.write('%s' % printListLibVal[time] + ' ' + '%.04f' % printListLibNum[time] + '\n')


sys.stdout.write('\n')

for time2 in range(0, 20):
    sys.stdout.write('%s' % printListConVal[time2] + ' ' + '%.04f' % printListConNum[time2] + '\n')


