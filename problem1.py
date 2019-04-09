### Ryan Anderson
### TCSS 456 - Assignment 1
### 2/1/19

###Step 1-1) Create the Word Dictionary
###Step 1-2) Building	an	MLE	unigram	model

#Open and read training file.  Use "The Adventures of Sherlock Holmes".
trainingFile = "doyle-27.txt"

f = open(trainingFile, 'r')
tempList = []

#Strip new line chars, split words by space, and make words lower 
#case before appending to list. 
for line in f:
    line = line.strip()
    for word in line.split(" "):
        tempList.append(word.lower())


#Now we can make our dictionary and add words from list to 
#dictionary.  We will search through dictionary for the word
#before adding, if we find the word we will increment the count and continue
#, if we dont find the word, we will add the word and set the count to 1.
wordDict = {}
for i in tempList:
    if i in wordDict:
        wordDict[i] += 1
    else:
        wordDict[i] = 1

#write probabilites to file.  Prob(word) = count(word) / count(all words)
fOut = open("unigram_probs.txt", "w")
totalCount = len(tempList)
for i in wordDict:
    prob = wordDict[i] / totalCount
    fOut.writelines("Prob: {0:<20} = {1:>15.3}".format(i, prob))
    fOut.write("\n")

testFile = "doyle-case-27.txt"
r = open(testFile, 'r')
fOut2 = open("unigram_eval.txt", "w")

count = 0

for line in r:
    #Only first 100 lines
    if count == 100:
        break
    line = line.strip()
    #add words to list to iterate
    s = []
    for word in line.split(" "):
        s.append(word.lower())
    sentProb = 1
    #calculate joint prob
    for word in s:
        if word in wordDict:
            prob = (wordDict[word.lower()] / totalCount)
            sentProb *= prob
        else:
            sentProb *= 0
    
    #sent length
    sentLength = len(s)
    
    #calc perplexity: perplexity = 1/(pow(sentprob, 1.0/sent_len))
    if sentProb == 0:
        perplex = 0
    else:       
        perplex = 1 / (pow(sentProb, 1/sentLength))
    
    #write joints and perplexes of each sentence
    fOut2.write("Sentence {0}: JointProb = {1:.4}, Perplexity = {2}".format(count, sentProb, perplex))
    fOut2.write("\n")
    count += 1
        
    
    
f.close()
r.close()

fOut.close()
fOut2.close()
    