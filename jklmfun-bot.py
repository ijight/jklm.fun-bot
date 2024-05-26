from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchFrameException, ElementNotInteractableException
import time
import re
import random

#############################
########## GLOBALS ##########
#############################

ROOMCODE = "MHEN"
MODE = "player"
LOG_ANSWERS_FOR_OTHERS = True
ANSWER_LIKE_A_BOT = False

#############################
###### INITIALIZATION #######
#############################

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(f"https://jklm.fun/{ROOMCODE}")
driver.find_element(By.CSS_SELECTOR, 'button.styled').send_keys(Keys.ENTER)

time.sleep(2) # this is 1000% necessary, the game is slow to load the iframe

# WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))) this is broken
frameNotLoaded = True
while frameNotLoaded:
    try:
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        frameNotLoaded = False
    except NoSuchFrameException:
        frameNotLoaded = True

#############################

def FailBlock(block, letterWait):
    if random.randint(1, 2) == 1:
        driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(block[0])
    else:
        driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(block[1])
    for letter in block:
        driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(letter)
        time.sleep(letterWait)
    for _ in range(len(block) + 1):
        driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(Keys.BACK_SPACE)
        time.sleep(0.15)

def ArtificialTypos(ans):
    ansList = []
    cnt = 0
    while len(ans) > cnt:
        chunkSize = random.randint(3, 6)
        ansList.append(ans[cnt:cnt + chunkSize])
        cnt += chunkSize
    for block in ansList:
        letterWait = random.uniform(0.02, 0.06)
        if random.randint(1, 100) > 97:
            FailBlock(block, letterWait)
            for letter in block:
                driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(letter)
                time.sleep(letterWait)
        else:
            for letter in block:
                driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(letter)
                time.sleep(letterWait)
        time.sleep(random.uniform(0.05, 0.2))

def SelectSolvingMethod(dictionary, unusedLetters, syllablePassed):
    diceRoll = random.randint(1, 4)
    diceRoll = 1
    if diceRoll == 1:
        print('Best Solution')
        return BestSolution(dictionary, unusedLetters, syllablePassed)
    if diceRoll == 2:
        print('Shortest Solution')
        return ShortestSolution(dictionary, unusedLetters, syllablePassed)
    if diceRoll == 3:
        print('Dashed Solution Attempted')
        x = DashedSolution(dictionary, unusedLetters, syllablePassed)
        if not x:
            print('Failed')
            return BestSolution(dictionary, unusedLetters, syllablePassed)
        else:
            return x
    if diceRoll == 4:
        print('Longest Solution')
        return LongestSolution(dictionary, unusedLetters, syllablePassed)

def CheatSolve(dictionary, unusedLetters, syllablePassed):
    print(BestSolution(dictionary, unusedLetters, syllablePassed, type="list")[:30])

def BestSolution(dictionary, unusedLetters, syll, type="string"):
    answers = [word for word in dictionary if syll in word]
    if type == "list": # Return a list of all possible answers
        return answers
    
    previousBestWordscore = 0
    temporaryBestSolution = ""
    for word in answers:
        letters = list(set(word))
        wordscore = sum(1 for letter in letters if letter in unusedLetters)
        wordscore += sum(1 for letter in letters if letter in ['Q', 'J'])
        if wordscore >= previousBestWordscore:
            temporaryBestSolution = word
            previousBestWordscore = wordscore

    return temporaryBestSolution 

def ShortestSolution(dictionary, syll):
    answers = [word for word in dictionary if syll in word]
    return min(answers, key=len, default=syll)

def DashedSolution(dictionary, syll):
    answers = [word for word in dictionary if syll in word]
    return max((word for word in answers if '-' in word), key=len, default="")

def LongestSolution(dictionary, syll):
    answers = [word for word in dictionary if syll in word]
    return max(answers, key=len, default="")

class GameStateManager:
    def __init__(self):
        self.unusedLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']

        # Load the word dictionary
        with open("jklm.fun-bot/dict.txt", "r") as f:
            wordDictionary = f.read().split("\n")
        self.dictionary = wordDictionary

    def removeLetters(self, bestWord):
        for letter in bestWord:
            if letter in self.unusedLetters:
                self.unusedLetters.remove(letter)

    def addLetters(self, word):
        for letter in word:
            if letter not in self.alphabet:
                self.alphabet.append(letter)
            if letter not in self.unusedLetters:
                self.unusedLetters.append(letter)

    def removeWord(self, word):
        if word in self.dictionary:
            self.dictionary.remove(word)

    def addWord(self, word):
        if word not in self.dictionary:
            self.dictionary.append(word)

    def reset(self):
        self.unusedLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
        with open("jklm.fun-bot/dict.txt", "r") as f:
            wordDictionary = f.read().split("\n")
        self.dictionary = wordDictionary

def findAnswerAndSubmit(gameState, bot_mode=False):
    syllable = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'syllable'))).text
    solve = SelectSolvingMethod(gameState.dictionary, gameState.unusedLetters, syllable)
    gameState.removeWord(solve)
    gameState.removeLetters(solve)

    if bot_mode:
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(solve)
    else:
        time.sleep(random.uniform(0.2, 0.6))
        ArtificialTypos(list(solve))
    
    driver.find_element(By.CSS_SELECTOR, 'input.styled').send_keys(Keys.ENTER)
    
    if not driver.find_element(By.CSS_SELECTOR, 'input.styled').is_displayed():
        gameState.addWord(solve)
        gameState.addLetters(solve)

class Logger:
    def __init__(self, silent = []):
        self.silent = silent
    
    def log(self, source, message):
        if source == None:
            print(message)

        if source not in self.silent:
            print(message)
            self.silent.append(source)

    def unsilence(self, source):
        if source in self.silent:
            self.silent.remove(source)

log = Logger()
gameState = GameStateManager()

if MODE == "player":
    while True:
        join_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'joinRound')))
        print("Joining game")
        join_button.click()

        game_ongoing = True

        while game_ongoing:
            log.log("game_loop", "Game loop started")
            agent_is_current_player = driver.find_element(By.CSS_SELECTOR, 'input.styled').is_displayed()
            current_syllable = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'syllable'))).text
        
            while not agent_is_current_player and game_ongoing:
                log.log("current_player_loop", "Agent is not the current player")
                past_syllable = current_syllable
                current_syllable = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'syllable'))).text

                if LOG_ANSWERS_FOR_OTHERS and past_syllable != current_syllable:
                    CheatSolve(gameState.dictionary, gameState.unusedLetters, WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'syllable'))).text)
                    time.sleep(1.0)

                agent_is_current_player = driver.find_element(By.CSS_SELECTOR, 'input.styled').is_displayed()
                time.sleep(0.5)
                game_ongoing =  not(join_button.is_displayed())

            log.unsilence("current_player_loop")
            log.log(None, "Agent is the current player")

            log.log(None, "Attempted to answer")
            try:
                findAnswerAndSubmit(gameState, bot_mode = ANSWER_LIKE_A_BOT) # This is the main function that finds the answer and submits it
            except ElementNotInteractableException:
                log.log(None, "Failed to answer, probably because the game ended")

            time.sleep(0.2)
            agent_is_current_player = driver.find_element(By.CSS_SELECTOR, 'input.styled').is_displayed()
            
            game_ongoing = not(join_button.is_displayed())

        log.log("game_loop", "Game has ended")
        gameState.reset()
        time.sleep(2)

if MODE == "monitor":
    while True:
        game_start = True
