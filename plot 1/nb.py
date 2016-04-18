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

for word in dictCon:
    if word in vocabulary:
        p1 = (dictCon[word] + 1) * 1.0 / (len(TEXTcon) + len(vocabulary))
        Pconword[word] = p1

for word1 in dictLib:
    if word1 in vocabulary:
        p2 = (dictLib[word1] + 1) * 1.0 / (len(TEXTlib) + len(vocabulary))
        Plibword[word1] = p2


#test NB model
testInput = open(sys.argv[2],'r')
TestText = testInput.read().strip()
testList = []

for line2 in TestText.splitlines():
    testList.append(line2)

Accuracy = 0

for testFile in testList:
    targetFile2 = open(testFile, 'r').read().strip().lower()
    targetText2 = targetFile2.splitlines()
    Vcon = 0
    Vlib = 0
    for testWord in targetText2:
        if (testWord in Pconword) and (testWord in vocabulary):
            Vcon += math.log(Pconword[testWord])
        elif testWord in vocabulary and testWord not in Pconword:
            Vcon += math.log(1.0 / (len(TEXTcon) + len(vocabulary)))
    Vcon += math.log(Pcon)

    for testWord2 in targetText2:
        if (testWord2 in Plibword) and (testWord2 in vocabulary):
            Vlib += math.log(Plibword[testWord2])
        elif testWord2 in vocabulary and testWord2 not in Plibword:
            Vlib += math.log(1.0 / (len(TEXTlib) + len(vocabulary)))
    Vlib += math.log(Plib)

    if Vcon > Vlib:
        sys.stdout.write('C' + "\n")
        if 'con' in testFile:
            Accuracy += 1
    elif Vcon <= Vlib:
        sys.stdout.write('L' + "\n")
        if 'lib' in testFile:
            Accuracy += 1



sys.stdout.write('Accuracy: %.04f' % (Accuracy * 1.0 / len(testList)) + "\n")




        


