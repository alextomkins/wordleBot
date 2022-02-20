# wordle
Python bot that utilises Selenium to guess the daily Wordle puzzle.

</img>
<img src = "wordle.gif", alt = "wordle", height = "720">

This program accesses the Wordle website and enters guesses until the answer is found, or it fails.

The logic behind the bot is based around the idea of eliminating words from a list until only the correct answer remains. The first guess 'salet' was chosen based on the findings of 3Blue1Brown in their Wordle project (https://github.com/3b1b/videos/tree/master/_2022/wordle). The words.txt list of possible guesses was also lifted from this project.

After each round of guessing, words from the list are removed if they do not meet the necessary criteria. This involves removing all words that do not contain letters that appear as a 'Match' or 'Present'. All words that contain letters identified as 'Absent' are also disregarded. This algorithm also refrains from guessing words with multiple of the same letters until other options have been utilised. This is to remove as many possibilities as possible and produce a bot that successfully guesses the word with a high win percentage, and not necessarily with the least number of guesses used.
