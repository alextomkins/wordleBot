# wordleBot
Python bot that utilises Selenium to guess the daily Wordle puzzle.

</img>
<img src = "wordle.gif", alt = "wordle", height = "720">

This program accesses the Wordle website and enters guesses until the answer is found, or it fails.

The logic behind the bot is based on the idea of eliminating words from a list until only the correct answer remains. This is designed to roughly mimic how a human would play the game on 'Hard Mode'. The first guess 'salet' was chosen based on the findings of 3Blue1Brown in their Wordle project (https://github.com/3b1b/videos/tree/master/_2022/wordle). The words.txt list of possible guesses was also lifted from this project.

After each round of guessing, words from the list are removed if they do not meet the necessary criteria. This involves ensuring that the remaining words in the list contain letters that returned 'Correct' or 'Present' clues and that these letters are in appropriate positions. Words that contain letters that return 'Absent' are also removed from the list. The special rules for cases where multiple of the same letter are guessed were also considered. 
