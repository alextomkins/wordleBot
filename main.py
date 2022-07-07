from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class WordList:
    def __init__(self):
        with open('words.txt', 'r') as f:
            self.words = f.read().split()
        
        self.guessNumber = 1
        self.wordToGuess = 'salet'

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        url = 'https://www.nytimes.com/games/wordle/index.html'
        self.driver.get(url)

        time.sleep(1)

        self.elem = self.driver.find_element(By.TAG_NAME, 'html')

        self.elem.click()

        self.wordGuess()

    ###########################

    def correctNumberOfMultiple(self, index, letterList, multiAttributes, i):
        if self.words[index].count(letterList[i]) != (multiAttributes.count('correct') + multiAttributes.count('present')):
            return True
        
        return False

    def absentOrPresentMultiple(self, index, letterList, attributeList, i):
        if (attributeList[i] == 'absent' or attributeList[i] == 'present') and letterList[i].lower() == self.words[index][i]:
            return True

        return False

    def isCorrect(self, index, letterList, attributeList, i):
        if attributeList[i] == 'correct' and letterList[i].lower() != self.words[index][i]:
            return True
        
        return False

    #######################

    def returnClues(self):
        time.sleep(2)

        letterList = []
        attributeList = []

        for i in range(5):
            letter = self.driver.find_element(By.XPATH, f'/html/body/div/div[1]/div/div[{self.guessNumber}]/div[{i+1}]/div') 
            attribute = self.driver.find_element(By.XPATH, f'/html/body/div/div[1]/div/div[{self.guessNumber}]/div[{i+1}]/div').get_attribute("data-state")

            letterList.append(letter.text)
            attributeList.append(attribute)

        self.guessNumber += 1

        if attributeList.count('correct') == 5:
            pass
        else:
            self.reduceWordList(letterList, attributeList)
    
    def wordGuess(self):
        self.elem.send_keys(self.wordToGuess)
        self.elem.send_keys(Keys.ENTER)
        self.returnClues()

    def reduceWordList(self, letterList, attributeList):
        indicies = []

        for i in range(len(letterList)):

            indicies.append([j for j, x in enumerate(letterList) if x == letterList[i]])

            multiAttributes = []

            if len(indicies[i]) > 1:
                for k in range(len(indicies[i])):
                    multiAttributes.append(attributeList[indicies[i][k]])

                if multiAttributes.count('absent') == len(multiAttributes):
                    index = 0
                    while(True):
                        if self.letterList[i].lower() in self.words[index]:
                            del self.words[index]
                            index -= 1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if multiAttributes.count('present') == len(multiAttributes):
                    index = 0
                    while(True):
                        if letterList[i].lower() == self.words[index][i] or letterList[i].lower() not in self.words[index]:
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if multiAttributes.count('correct') == len(multiAttributes):
                    index = 0
                    while(True):
                        if letterList[i].lower() != self.words[index][i]:
                            del self.words[index]
                            index -=1
                        
                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'absent' in multiAttributes and 'present' in multiAttributes and 'correct' in multiAttributes:
                    index = 0
                    while(True):
                        if self.correctNumberOfMultiple(index, letterList, multiAttributes, i) and self.absentOrPresentMultiple(index, letterList, attributeList, i) and self.isCorrect(index, letterList, attributeList, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'absent' in multiAttributes and 'present' in multiAttributes and 'correct' not in multiAttributes:
                    index = 0
                    while(True):
                        if self.correctNumberOfMultiple(index, letterList, multiAttributes, i) and self.absentOrPresentMultiple(index, letterList, attributeList, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'absent' in multiAttributes and 'correct' in multiAttributes and 'present' not in multiAttributes:
                    index = 0
                    while(True):
                        if self.correctNumberOfMultiple(index, letterList, multiAttributes, i) and self.absentOrPresentMultiple(index, letterList, attributeList, i) and self.isCorrect(index, letterList, attributeList, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'present' in multiAttributes and 'correct' in multiAttributes and 'absent' not in multiAttributes:
                    index = 0
                    while(True):
                        if self.words[index].count(self.letterList[i]) < (multiAttributes.count('correct') + multiAttributes.count('present')) and self.absentOrPresentMultiple(index, self.letterList, self.attributeList, i) and self.isCorrect(index, self.letterList, self.attributeList, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

            else:
                if attributeList[i] == 'absent':
                    index = 0
                    while(True):
                        if letterList[i].lower() in self.words[index]:
                            del self.words[index]
                            index -= 1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if attributeList[i] == 'present':
                    index = 0
                    while(True):
                        if letterList[i].lower() == self.words[index][i] or letterList[i].lower() not in self.words[index]:
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if attributeList[i] == 'correct':
                    index = 0
                    while(True):
                        if letterList[i].lower() != self.words[index][i]:
                            del self.words[index]
                            index -=1
                        
                        if index >= len(self.words) - 1:
                            break

                        index += 1
        
        self.wordToGuess = self.words[0]
        self.wordGuess()
        
w1 = WordList()
