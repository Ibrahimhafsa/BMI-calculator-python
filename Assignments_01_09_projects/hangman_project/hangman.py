import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words) #randomly chooses something from the list 
    while '_' in word or ' ' in word:
        word = random.choice(words)


    return word


def hangman():
    word = get_valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()


user_input = input("Type something: ")
print(user_input)    