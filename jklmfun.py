from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import random
from selenium import webdriver

roomCode = "SDUX"

#Begin bot - create username on JKLM


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

driver = webdriver.Chrome()
driver.get("https://jklm.fun/" + str(roomCode))
driver.find_element_by_css_selector('button.styled').send_keys(Keys.ENTER)
WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
driver.find_element_by_css_selector('body').send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)

def AnswerLikeAHuman():
    try:
        ans = Solve(driver.find_element_by_class_name('syllable').text)
        ans = list(ans)
        time.sleep(random.uniform(0.2, 1.5))
        ArtificialTypos(ans)
        driver.find_element_by_css_selector('input.styled').send_keys(Keys.ENTER)
    except:
        print('wtf')

def RollForFuckup():
    num = random.randint(1, 100)
    if num > 90:
        return True
    else:
        return False

def FailBlock(block,letterWait):
    if random.randint(1, 2) == 1:
        driver.find_element_by_css_selector('input.styled').send_keys(block[0])
    else:
        driver.find_element_by_css_selector('input.styled').send_keys(block[1])
    for letter in block:
        driver.find_element_by_css_selector('input.styled').send_keys(letter)
        time.sleep(letterWait) 
    for unused in range(0,len(block)+1):
        driver.find_element_by_css_selector('input.styled').send_keys(Keys.BACK_SPACE)
        time.sleep(0.15) 


def ArtificialTypos(ans):
    ansList = []
    cnt = 0
    while len(ans) > cnt:
        chunkSize = random.randint(3, 6)
        ansList.append(ans[cnt:cnt+chunkSize])
        cnt += chunkSize
    for block in ansList:
        letterWait = random.uniform(0.02, 0.06)
        if RollForFuckup():
                FailBlock(block, letterWait)
                for letter in block:
                    driver.find_element_by_css_selector('input.styled').send_keys(letter)
                    time.sleep(letterWait) 
        else:
            for letter in block:
                driver.find_element_by_css_selector('input.styled').send_keys(letter)
                time.sleep(letterWait) 
        time.sleep(random.uniform(0.05, 0.2)) 

def AnswerLikeABot():
    x = Solve(driver.find_element_by_class_name('syllable').text)
    driver.find_element_by_css_selector('input.styled').send_keys(x, Keys.ENTER)

def ans():
    while not(driver.find_element_by_css_selector('input.styled').is_displayed()):
        True
    AnswerLikeAHuman()
    syllChange(driver.find_element_by_class_name('syllable').text)
    
def syllChange(x):
    while x == driver.find_element_by_css_selector('input.styled').is_displayed():
        True
    print("SYLLCHANGE SENT TO ANS:", driver.find_element_by_class_name('syllable').text)
    ans()

x = driver.find_element_by_class_name('syllable').text
print("X TO BEGIN WITH:", x)
syllChange(driver.find_element_by_css_selector('input.styled').is_displayed())

