import argparse
from datetime import datetime, timedelta
import enchant
import enum
from random_word import RandomWords
import re
import sys

guessMap = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth", 6: "Sixth"}
alphabet = "abcdefghijklmnopqrstuvwxyz"

class GuessState(enum.Enum):
    green = 1
    yellow = 2
    gray = 3

class printColors:
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    endc = '\033[0m'

def generateWord(n):
    r = RandomWords()
    word = r.get_random_word(hasDictionaryDef=True, minLength=n, maxLength=n)
    return word

def validateWord(s, n): #TODO
    if len(s) != n:
        return False
    d = enchant.Dict("en_US")
    return d.check(s)

def getValidWord(n):
    timeout = datetime.now() + timedelta(seconds=30)
    while datetime.now() < timeout:
        s = generateWord(n)
        print(s)
        if validateWord(s, n):
            return s

def compareLetters(word, guess):
    letters = word
    r = [None]*len(word)
    for i in range(len(word)):
        if word[i] == guess[i]:
            r[i] = GuessState.green
            letters = letters.replace(word[i], "", 1)
    for i, val in enumerate(r):
        if val == None:
            if guess[i] in letters:
                r[i] = GuessState.yellow
                letters = letters.replace(guess[i], "", 1)
            else:
                r[i] = GuessState.gray
    return r

def outputResult(res, guess):
    outputString = ""
    for i in range(len(guess)):
        if res[i] == GuessState.green:
            outputString += printColors.green
        elif res[i] == GuessState.yellow:
            outputString += printColors.yellow
        else:
            outputString += printColors.red
        outputString += guess[i] + printColors.endc
    return outputString

if __name__ == "__main__":
    #TODO: add hardmode
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=5, help="number of letters in wordle", required=False)
    parser.add_argument("--maxGuesses", type=int, default=6, help="maximum number of guesses", required=False)
    args = parser.parse_args()

    word = getValidWord(args.length)
    if word == "":
        sys.exit("error generating valid word")
    # print(word)
    guessNum = 0
    sharableResults = []
    while guessNum < args.maxGuesses:
        guessNum += 1
        guess = input(guessMap[guessNum] + " guess: ")
        if not validateWord(guess, args.length):
            print(guess + " is not a valid guess, try again")
            guessNum -= 1
            continue
        res = compareLetters(word, guess)
        sharableResults.append(res)
        print(outputResult(res, guess))
        # TODO: print color coded alphabet
        if guess == word:
            print("Congratulations! You got the wordle in", guessNum, "guesses!")
            share = input("Would you like to share your result (y/n)?")
            if share.lower() == "y":
                print(sharableResults) #TODO: output emojis?
            sys.exit()

    print("The wordle was " + word + ". Better luck next time!")
