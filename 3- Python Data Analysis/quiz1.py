#!/usr/bin/env python3
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#



monty_quote = "listen strange women lying in ponds distributing swords is no basis for a system of government supreme executive power derives from a mandate from the masses not from some farcical aquatic ceremony"

monty_words = monty_quote.split(" ")

def count_letters(word_list):
    """ See question description """
    
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    letter_count = {}
    most_frequently_letter = ""
    most_frequently_value = 0
    
    for word in word_list:
        for letter in word:
            value = letter_count.get(letter, 0) + 1
            letter_count[letter] = value
            if most_frequently_value < value:
                most_frequently_value = value
                most_freqently_letter = letter
        
    return most_freqently_letter, most_frequently_value


print(count_letters(["hello","world"])) # ------->> 'l', 3
print(count_letters(monty_words))
