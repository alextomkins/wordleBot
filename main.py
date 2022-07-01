from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def setup():
    global driver
    global elem
    global wordList
    global guessNumber

    guessNumber = 1

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    url = 'https://www.nytimes.com/games/wordle/index.html'
    driver.get(url)

    time.sleep(1)

    elem = driver.find_element_by_tag_name('html')

    elem.click()

    time.sleep(1)


    with open('words.txt', 'r') as f:
        wordList = f.read().split()

    wordGuess('moons', guessNumber)


def wordGuess(wordToGuess, guessNumber):
    elem.send_keys(wordToGuess)
    elem.send_keys(Keys.ENTER)
    returnClues(guessNumber)

def returnClues(guessNumber):
    time.sleep(2)

    letterList = []
    attributeList = []

    for i in range(5):
        letter = driver.find_element_by_xpath(f'/html/body/div/div[1]/div/div[{guessNumber}]/div[{i+1}]/div') 
        attribute = driver.find_element_by_xpath(f'/html/body/div/div[1]/div/div[{guessNumber}]/div[{i+1}]/div').get_attribute("data-state");

        letterList.append(letter.text)
        attributeList.append(attribute)

    print(letterList)
    print(attributeList)

    guessNumber += 1

    if attributeList.count('correct') == 5:
        pass
    else:
        reduceWordList(letterList, attributeList, guessNumber)


def reduceWordList(letterList, attributeList, guessNumber):
    indicies = []

    for i in range(len(letterList)):

        indicies.append([j for j, x in enumerate(letterList) if x == letterList[i]])

        multiAttributes = []

        if len(indicies[i]) > 1:
            for k in range(len(indicies[i])):
                multiAttributes.append(attributeList[indicies[i][k]])
                print(multiAttributes)

            if multiAttributes.count('absent') == len(multiAttributes):
                index = 0
                while(True):
                    if letterList[i].lower() in wordList[index]:
                        del wordList[index]
                        index -= 1

                    if index >= len(wordList) - 1:
                        break

                    index += 1

            if multiAttributes.count('present') == len(multiAttributes):
                index = 0
                while(True):
                    if letterList[i].lower() == wordList[index][i] or letterList[i].lower() not in wordList[index]:
                        del wordList[index]
                        index -=1

                    if index >= len(wordList) - 1:
                        break

                    index += 1

            if multiAttributes.count('correct') == len(multiAttributes):
                index = 0
                while(True):
                    if letterList[i].lower() != wordList[index][i]:
                        del wordList[index]
                        index -=1
                    
                    if index >= len(wordList) - 1:
                        break

                    index += 1

            if 'absent' in multiAttributes and 'present' in multiAttributes and 'correct' in multiAttributes:
                pass

            if 'absent' in multiAttributes and 'present' in multiAttributes:
                pass

            if 'absent' in multiAttributes and 'correct' in multiAttributes:
                pass

            if 'present' in multiAttributes and 'correct' in multiAttributes:
                pass

        else:
            if attributeList[i] == 'absent':
                index = 0
                while(True):
                    if letterList[i].lower() in wordList[index]:
                        del wordList[index]
                        index -= 1

                    if index >= len(wordList) - 1:
                        break

                    index += 1

            if attributeList[i] == 'present':
                index = 0
                while(True):
                    if letterList[i].lower() == wordList[index][i] or letterList[i].lower() not in wordList[index]:
                        del wordList[index]
                        index -=1

                    if index >= len(wordList) - 1:
                        break

                    index += 1

            if attributeList[i] == 'correct':
                index = 0
                while(True):
                    if letterList[i].lower() != wordList[index][i]:
                        del wordList[index]
                        index -=1
                    
                    if index >= len(wordList) - 1:
                        break

                    index += 1

    wordGuess(wordList[0], guessNumber)

if __name__ == "__main__":
    setup()

    print(wordList)
