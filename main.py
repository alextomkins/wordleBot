#-----Description----------------------------------------------------#
#
#  WORDLE BOT, Version 2 (12.07.2022)
#
#  This program provides an automated solution to solving the daily 
#  wordle puzzle. The Google Chrome WebDriver is utilized to access
#  the official Wordle game on the New York Times website where the
#  script enters guesses until the answer is found, or it fails.
#  The answer is found through eliminating words from a list by
#  using the clues returned from the website. When the script 
#  finishes, the reduced word list is printed to the console. 
#
#  Author: Alexander Tomkins 
#  github.com/alextomkins
#
#--------------------------------------------------------------------#

# Import necessary selenium functions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Import time functions
import time

# Define a class to allow driver, elem, word_guess, and words to always be accessible
class WordList:
    # Initialise words list and navigate the website to allow for guessing
    def __init__(self):
        with open('words.txt', 'r') as f:
            self.words = f.read().split()
        
        self.guess_number = 1
        self.word_to_guess = 'salet'

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        url = 'https://www.nytimes.com/games/wordle/index.html'
        self.driver.get(url)

        time.sleep(2)

        self.elem = self.driver.find_element(By.TAG_NAME, 'html')

        self.close = self.driver.find_element(By.XPATH, f'/html/body/div/div/dialog/div/button')
        
        self.close.click()

        time.sleep(1)

        self.word_guess()

    #-----Conditional Statements------------------------------------------#

    def correct_number_multiple(self, index, letter_list, multi_attributes, i):
        if self.words[index].count(letter_list[i].lower()) != (multi_attributes.count('correct') + multi_attributes.count('present')):
            return True
        
        return False

    def less_than_number_multiple(self, index, letter_list, multi_attributes, i):
        if (self.words[index].count(letter_list[i].lower()) < (multi_attributes.count('correct') + multi_attributes.count('present'))):
            return True
        
        return False

    def absent_present_multiple(self, index, letter_list, attribute_list, i):
        if (attribute_list[i] == 'absent' or attribute_list[i] == 'present') and letter_list[i].lower() == self.words[index][i]:
            return True

        return False

    def is_correct(self, index, letter_list, attribute_list, i):
        if attribute_list[i] == 'correct' and letter_list[i].lower() != self.words[index][i]:
            return True
        
        return False

    def game_finished(self, attribute_list):
        if attribute_list.count('correct') == 5:
            return True
        
        return False

    def all_absent(self, multi_attributes):
        if multi_attributes.count('absent') == len(multi_attributes):
            return True
        
        return False

    def all_present(self, multi_attributes):
        if multi_attributes.count('present') == len(multi_attributes):
            return True
        
        return False

    def all_correct(self, multi_attributes):
        if multi_attributes.count('correct') == len(multi_attributes):
            return True
        
        return False

    #--------------------------------------------------------------------#

    # Return absent, present or correct for letters in the most recent guess
    def return_clues(self):
        time.sleep(2)

        letter_list = []
        attribute_list = []

        for i in range(5):
            #/html/body/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div
            #/html/body/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div
            #/html/body/div/div/div[2]/div/div[1]/div/div[2]/div[4]/div
            letter = self.driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[1]/div/div[{self.guess_number}]/div[{i+1}]/div') 
            attribute = self.driver.find_element(By.XPATH, f'/html/body/div/div/div[2]/div/div[1]/div/div[{self.guess_number}]/div[{i+1}]/div').get_attribute("data-state")

            letter_list.append(letter.text)
            attribute_list.append(attribute)

        self.guess_number += 1

        if self.game_finished(attribute_list):
            pass
        else:
            self.reduce_word_list(letter_list, attribute_list)
    
    # Send word guess to the website
    def word_guess(self):
        self.elem.send_keys(self.word_to_guess)
        self.elem.send_keys(Keys.ENTER)
        self.return_clues()

    # Reduce word list to ensure remaining words follow clues read from return_clues()
    def reduce_word_list(self, letter_list, attribute_list):
        indicies = []

        for i in range(len(letter_list)):

            indicies.append([j for j, x in enumerate(letter_list) if x == letter_list[i]])

            multi_attributes = []

            if len(indicies[i]) > 1:
                for k in range(len(indicies[i])):
                    multi_attributes.append(attribute_list[indicies[i][k]])

                if self.all_absent(multi_attributes):
                    index = 0
                    while(True):
                        if letter_list[i].lower() in self.words[index]:
                            del self.words[index]
                            index -= 1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if self.all_present(multi_attributes):
                    index = 0
                    while(True):
                        if letter_list[i].lower() == self.words[index][i] or letter_list[i].lower() not in self.words[index]:
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if self.all_correct(multi_attributes):
                    index = 0
                    while(True):
                        if letter_list[i].lower() != self.words[index][i]:
                            del self.words[index]
                            index -=1
                        
                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'absent' in multi_attributes and 'present' in multi_attributes and 'correct' in multi_attributes:
                    index = 0
                    while(True):
                        if self.correct_number_multiple(index, letter_list, multi_attributes, i) or self.absent_present_multiple(index, letter_list, attribute_list, i) or self.is_correct(index, letter_list, attribute_list, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'absent' in multi_attributes and 'present' in multi_attributes and 'correct' not in multi_attributes:
                    index = 0
                    while(True):
                        if self.correct_number_multiple(index, letter_list, multi_attributes, i) or self.absent_present_multiple(index, letter_list, attribute_list, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'absent' in multi_attributes and 'correct' in multi_attributes and 'present' not in multi_attributes:
                    index = 0
                    while(True):
                        if self.correct_number_multiple(index, letter_list, multi_attributes, i) or self.absent_present_multiple(index, letter_list, attribute_list, i) or self.is_correct(index, letter_list, attribute_list, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if 'present' in multi_attributes and 'correct' in multi_attributes and 'absent' not in multi_attributes:
                    index = 0
                    while(True):
                        if self.less_than_number_multiple(index, letter_list, multi_attributes, i) or self.absent_present_multiple(index, letter_list, attribute_list, i) or self.is_correct(index, letter_list, attribute_list, i):
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

            else:
                if attribute_list[i] == 'absent':
                    index = 0
                    while(True):
                        if letter_list[i].lower() in self.words[index]:
                            del self.words[index]
                            index -= 1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if attribute_list[i] == 'present':
                    index = 0
                    while(True):
                        if letter_list[i].lower() == self.words[index][i] or letter_list[i].lower() not in self.words[index]:
                            del self.words[index]
                            index -=1

                        if index >= len(self.words) - 1:
                            break

                        index += 1

                if attribute_list[i] == 'correct':
                    index = 0
                    while(True):
                        if letter_list[i].lower() != self.words[index][i]:
                            del self.words[index]
                            index -=1
                        
                        if index >= len(self.words) - 1:
                            break

                        index += 1
        
        self.word_to_guess = self.words[0]
        self.word_guess()

# Start the script by initialising a wordList object        
w1 = WordList()

# Print reduced word list, first item will be correct guess or next guess if the bot failed
print(w1.words)
