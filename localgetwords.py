import random

f = open("dict.txt", "r")
wordDictionary = f.read()
f.close()

wordDictionary = wordDictionary.split("\n")
syll = ""
unusedLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
def LetterManager(bestWord):
    bestWordLettersList = list(bestWord)
    global unusedLetters
    unusedLetters = (list(set(unusedLetters) - set(bestWordLettersList)))
    if unusedLetters == []:
        unusedLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']

def SelectSolvingMethod():
    diceRoll = random.randint(1, 4)
    diceRoll = 4
    if diceRoll == 1:
        print('Best Solution')
        return BestSolution()
    if diceRoll == 2:
        print('Shortest Solution')
        return ShortestSolution()
    if diceRoll == 3:
        print('Dashed Solution Attempted')
        x = DashedSolution()
        if (x == ""):
            print('Failed')
            return BestSolution()
        else:
            return x
    if diceRoll == 4:
        print('Longest Solution')
        return LongestSolution()

def Solve(syllablePassed):
    global syll
    syll = syllablePassed
    solutionGiven = SelectSolvingMethod()
    wordDictionary.remove(solutionGiven)
    LetterManager(solutionGiven)
    print(solutionGiven)
    print(alphabet)
    print(unusedLetters)
    return solutionGiven

#Solving Methods

def BestSolution():
    answers = []
    for word in wordDictionary:
        if syll in word:
            answers.append(word)
    previousBestWordscore = 0
    temporaryBestSolution = ""
    for word in answers: #for each word
        letters = list(set(list(word)))
        letters 
        wordscore = 0
        for letter in letters:  #for each letter
            if letter in unusedLetters:
                wordscore += 1
                if letter == "Q" or "Z" or "J":
                    wordscore += 1
        if wordscore >= previousBestWordscore:
            temporaryBestSolution = word
            previousBestWordscore = wordscore
    return temporaryBestSolution

def ShortestSolution():
    if syll in wordDictionary:
        return syll
    else:
        answers = []
        for word in wordDictionary:
            if syll in word:
                answers.append(word)
        for word in answers:
            previousShortest = 10
            wordLength = len(word)
            if wordLength <= previousShortest:
                temporaryBestSolution = word
        return temporaryBestSolution

def DashedSolution():
    answers = []
    for word in wordDictionary:
        if syll in word:
            answers.append(word)
    print(answers)
    temporaryBestSolution = ""
    for word in answers:
        if ('-' in word) and (len(word) >= len(temporaryBestSolution)):
            temporaryBestSolution = word
    return temporaryBestSolution

def LongestSolution():
    longest = ''
    answers = []
    for word in wordDictionary:
        if syll in word:
            answers.append(word)
            
    for x in answers:
        if len(x) >= len(longest):
            longest = x 
    return longest

print(Solve("NE"))