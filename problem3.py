### Ryan Anderson
### TCSS 456 - Assignment 1
### 2/1/19

###Step 2-4) Smoothing
from random import shuffle
import random

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
    
#This is like the unigram model but we will instead store the word count and
#the previous word counts.  We do this by using a list in a dictionary for
#list[0] being count of word. List[1] is another dictionary to store 
#i-1 word counts.
wordDict = {}
for i in range(len(tempList)):
    if tempList[i] in wordDict:
        wordDict[tempList[i]][0] += 1
        if tempList[i-1] in wordDict[tempList[i]][1]:
            wordDict[tempList[i]][1][tempList[i-1]] += 1
        else:
            wordDict[tempList[i]][1][tempList[i-1]] = 1

    else:
        wordDict[tempList[i]] = [1, {}]
        wordDict[tempList[i]][1][tempList[i-1]] = 1
    
#Make a list of keys and shuffle them.  Write to file 100 random probabilities.
#Also pick a random number for prev word with random integer method.
fOut = open("smooth_probs.txt","w")   
keys = list(wordDict)
shuffle(keys)

for i in range(100):

    #word i
    word = keys[i]
    
    #previous words list
    prevKeys = list(wordDict[word][1])
    
    #pick a random previous word
    lenPrevWordList = len(wordDict[word][1])
    randomPrevWordIndex = random.randint(0,lenPrevWordList - 1)
    prevWord = prevKeys[randomPrevWordIndex]
    
    #previous word count
    w0 = wordDict[prevWord][0]
    
    #previousWord and current word count
    w1  = wordDict[word][1][prevWord]
    
    #smoothing element
    smoothing = .1
    
    #v * smoothing
    vSmoothed = lenPrevWordList * smoothing
    
    #Smoothing: Prob(wordi|wordi-1): 
    #Count(wordi-1 wordi) + alpha / Count(wordi-1) + v(alpha)
    probability = (w1 + smoothing) / (w0 + vSmoothed)
    

    fOut.writelines("P({0}|{1}) = {2:.5}".format(word, prevWord, probability))
    fOut.write("\n")

testFile = "doyle-case-27.txt"
r = open(testFile, 'r')
fOut2 = open("smoothed_eval.txt", "w")

count = 0

sentList = []
for line in r:
    line = line.strip()
    sentList.append(line)
    
for i in range(100):
    s = []
    for word in sentList[i].split(" "):
        s.append(word)
    sentProb = 1.0
    
    for g in range(len(s)):
        if s[g] in wordDict:
            
            #smoothing element
            smoothing = .1
                
            #v * smoothing
            vSmoothed = len(wordDict[s[g]][1]) * smoothing
            
            #First word of sentence then use previous word which is last word
            #of last sentence.
            if g == 0:
                
                #Start of corpus
                if i == 0:
                    sentProb *= 0
                    continue
                
                #Get previous sentence
                prevSentList = []
                for word in sentList[i-1].split(" "):
                    prevSentList.append(word)
                
                #word in wordDict
                if prevSentList[-1] in wordDict[s[g]][1]:
                    
                    #previous word count
                    w0 = wordDict[prevSentList[-1]][0]
                    
                    #previousWord and current word count
                    w1  = wordDict[s[g]][1][prevSentList[-1]]
                    
                    #Prob(wordi|wordi-1)=  Count(wordi-1 wordi)/ Count(wordi-1)
                    probability = (w1 + smoothing) / (w0 + vSmoothed)
                
                    sentProb *= probability
                    
                #word not in wordDict but can still smooth
                else:
                    sentProb *= (smoothing / vSmoothed)
                
            #word in wordDict
            elif s[g-1] in wordDict[s[g]][1]:
                
                #prev word count
                w0 = wordDict[s[g-1]][0]
                
                #previousWord and current word count
                w1  = wordDict[s[g]][1][s[g-1]]
                
                #Prob(wordi|wordi-1)=  Count(wordi-1 wordi)/ Count(wordi-1)
                probability = (w1 + smoothing) / (w0 + vSmoothed)
                
                sentProb *= probability
                
            #word not in worddict
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


    