from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re

def main():
	setup()
	
	#Solve next 5 guesses
	for i in range(5):
		returnClues()
		removeAbsent()
		removeNear()
		removeMatches()
		method()
	
def setup():
        global driver
        global elem
        global wordList

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(options=options)
        url = 'https://www.powerlanguage.co.uk/wordle/'
        driver.get(url)
        
        time.sleep(1)

        elem = driver.find_element_by_tag_name('html')

        elem.click()

        time.sleep(1)


        with open('words.txt', 'r') as f:
                wordList = f.read().split()

        wordGuess('SALET')

def wordGuess(wordToGuess):
	elem.send_keys(wordToGuess)
	elem.send_keys(Keys.ENTER)

def returnClues():
        global matches
        global nearmatches
        global absent
        
        host = driver.find_element_by_tag_name("game-app")
        game = driver.execute_script("return arguments[0].shadowRoot.getElementById('game')", host)
        keyboard = game.find_element_by_tag_name("game-keyboard")
        keys = driver.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)
        time.sleep(2)
        keydata = driver.execute_script("return arguments[0].innerHTML;",keys)

        correctRegex = re.compile('...............correct', re.VERBOSE)

        matches = ['/', '/', '/', '/', '/']
        n = 0
        for groups in correctRegex.findall(keydata):
                matches[n] = (groups[0])
                n = n + 1



        presentRegex = re.compile('...............present', re.VERBOSE)

        nearmatches = ['/', '/', '/', '/', '/']
        n = 0
        for groups in presentRegex.findall(keydata):
                nearmatches[n] = (groups[0])
                n = n + 1


        absentRegex = re.compile('...............absent', re.VERBOSE)

        absent = ['/', '/', '/', '/', '/','/', '/', '/', '/', '/','/', '/', '/', '/', '/','/', '/', '/', '/', '/','/', '/', '/', '/', '/','/', '/', '/', '/', '/']

        n = 0
        for groups in absentRegex.findall(keydata):
                absent[n] = (groups[0])
                n = n + 1

def removeAbsent():
    for index in range(len(wordList)):
        if absent[0] in wordList[index] or absent[1] in wordList[index] or absent[2] in wordList[index] or absent[3] in wordList[index] or absent[4] in wordList[index] or absent[5] in wordList[index] or absent[6] in wordList[index] or absent[7] in wordList[index] or absent[8] in wordList[index] or absent[9] in wordList[index] or absent[10] in wordList[index] or absent[11] in wordList[index] or absent[12] in wordList[index] or absent[13] in wordList[index] or absent[14] in wordList[index] or absent[15] in wordList[index] or absent[16] in wordList[index] or absent[17] in wordList[index] or absent[18] in wordList[index] or absent[19] in wordList[index] or absent[20] in wordList[index] or absent[21] in wordList[index] or absent[22] in wordList[index] or absent[23] in wordList[index] or absent[24] in wordList[index] or absent[25] in wordList[index] or absent[26] in wordList[index] or absent[27] in wordList[index] or absent[28] in wordList[index] or absent[29] in wordList[index]:
            wordList[index] = ''

def removeNear():
    numNear = 5

    if nearmatches[4] == '/':
        numNear = 4

    if nearmatches[3] == '/':
        numNear = 3

    if nearmatches[2] == '/':
        numNear = 2

    if nearmatches[1] == '/':
        numNear = 1

    if nearmatches[0] == '/':
        numNear = 0

    for index in range(len(wordList)):
        if numNear == 5:
            if nearmatches[0] not in wordList[index] or nearmatches[1] not in wordList[index] or nearmatches[2] not in wordList[index] or nearmatches[3] not in wordList[index] or nearmatches[4] not in wordList[index]:
                wordList[index] = ''

        if numNear == 4:
            if nearmatches[0] not in wordList[index] or nearmatches[1] not in wordList[index] or nearmatches[2] not in wordList[index] or nearmatches[3] not in wordList[index]:
                wordList[index] = ''

        if numNear == 3:
            if nearmatches[0] not in wordList[index] or nearmatches[1] not in wordList[index] or nearmatches[2] not in wordList[index]:
                wordList[index] = ''

        if numNear == 2:
            if nearmatches[0] not in wordList[index] or nearmatches[1] not in wordList[index]:
                wordList[index] = ''

        if numNear == 1:
            if nearmatches[0] not in wordList[index]:
                wordList[index] = ''

def removeMatches():
    global numMatch
    numMatch = 5

    if matches[4] == '/':
        numMatch = 4

    if matches[3] == '/':
        numMatch = 3

    if matches[2] == '/':
        numMatch = 2

    if matches[1] == '/':
        numMatch = 1

    if matches[0] == '/':
        numMatch = 0

    for index in range(len(wordList)):

        if numMatch == 4:
            if matches[0] not in wordList[index] or matches[1] not in wordList[index] or matches[2] not in wordList[index] or matches[3] not in wordList[index]:
                wordList[index] = ''

        if numMatch == 3:
            if matches[0] not in wordList[index] or matches[1] not in wordList[index] or matches[2] not in wordList[index]:
                wordList[index] = ''

        if numMatch == 2:
            if matches[0] not in wordList[index] or matches[1] not in wordList[index]:
                wordList[index] = ''

        if numMatch == 1:
            if matches[0] not in wordList[index]:
                wordList[index] = ''

def method():
    global wordList
    global numMatch
    
    wordList = list(filter(None,wordList))

    nextGuess = False
    doubleLetter = False

    nextGuess2 = '/'

    for i in wordList:
        doubleLetter = False
        for letters in range(5):
            if i.count(i[letters]) > 1:
                doubleLetter = True
            if letters == 4 and doubleLetter == False and nextGuess == False:
                nextGuess2 = i
                nextGuess = True

    if nextGuess2 == '/' and numMatch != 5:
        nextGuess2 = wordList[0]

    wordGuess(nextGuess2)

    if numMatch != 5:
            wordList.remove(nextGuess2)

if __name__ == "__main__":
    main()
