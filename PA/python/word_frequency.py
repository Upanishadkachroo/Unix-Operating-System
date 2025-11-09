# word_frequency.py

from collections import Counter

filename = input("Enter file name: ")

with open(filename, 'r') as file:
    words = file.read().lower().split()

freq = Counter(words)

for word, count in freq.items():
    print(f"{word}: {count}")
