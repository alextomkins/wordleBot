from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
 

driver = webdriver.Chrome()

url = 'https://www.powerlanguage.co.uk/wordle/'
driver.get(url)

time.sleep(1)

elem = driver.find_element_by_tag_name('html')

elem.click()

time.sleep(1)


with open('words2.txt', 'r') as f:
    wordList = f.read().split()

elem.send_keys('CRANE')
elem.send_keys(Keys.ENTER)

host = driver.find_element_by_tag_name("game-app")
firstHost = driver.find_element_by_tag_name("game-app")
game = driver.execute_script("return arguments[0].shadowRoot.getElementById('game')", host)
    
    
keyboard = game.find_element_by_tag_name("game-keyboard")
    
keys = driver.execute_script("return arguments[0].shadowRoot.getElementById('keyboard')", keyboard)
    
time.sleep(2)
    #store data of all the letters (match, match in different location, no match)
keydata = driver.execute_script("return arguments[0].innerHTML;",keys)
    #get array of matches and matches in different locations using janky regex logic
correctRegex = re.compile('...............correct', re.VERBOSE)
    
matches = ['/', '/', '/', '/', '/']
n = 0
for groups in correctRegex.findall(keydata):
    matches[n] = (groups[0])
    n = n + 1

print(matches)

presentRegex = re.compile('...............present', re.VERBOSE)
    
nearmatches = ['/', '/', '/', '/', '/']
n = 0
for groups in presentRegex.findall(keydata):
    nearmatches[n] = (groups[0])
    n = n + 1

print(nearmatches)

absentRegex = re.compile('...............absent', re.VERBOSE)
    
absent = ['/', '/', '/', '/', '/']
n = 0
for groups in absentRegex.findall(keydata):
    absent[n] = (groups[0])
    n = n + 1

print(absent)

print(wordList)
print(matches)


for index in range(len(wordList)):
    if absent[0] in wordList[index] or absent[1] in wordList[index] or absent[2] in wordList[index] or absent[3] in wordList[index] or absent[4] in wordList[index]:
        wordList[index] = ''

if nearmatches[0] == '/':
    
    elif nearmatches[1] == '/':
            
        elif nearmatches[2] == '/':

            elif nearmatches[3] == '/':

                elif nearmatches[4] == '/':

for index in range(len(wordList)):
    

            
        



print(wordList)





