from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def main():
    setup()

    print(wordList)

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

    wordGuess('salet')

    returnClues(guessNumber)



def wordGuess(wordToGuess):
    elem.send_keys(wordToGuess)
    elem.send_keys(Keys.ENTER)

def returnClues(guessNumber):
    time.sleep(2)

    letterList = []
    attributeList = []

    for i in range(5):
        letter = driver.find_element_by_xpath(f'/html/body/div/div[1]/div/div[{guessNumber}]/div[{i+1}]/div') 
        attribute = driver.find_element_by_xpath(f'/html/body/div/div[1]/div/div[1]/div[{i+1}]/div').get_attribute("data-state");

        letterList.append(letter.text)
        attributeList.append(attribute)

    print(letterList)
    print(attributeList)

    guessNumber += 1

    reduceWordList(letterList, attributeList)


def reduceWordList(letterList, attributeList):
    for i in range(len(letterList)):
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

if __name__ == "__main__":
    main()
