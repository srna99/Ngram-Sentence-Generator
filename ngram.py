"""
Serena Cheng
CMSC 416 - PA 2: Ngrams
2/13/2020
~~~~~
Problem:
This assignment is about generating sentences based on different texts. The program constructs some
number of sentences using n-grams and relative frequency.
Usage:
The user should include additional arguments when executing program as follows:
    (number for n-gram model) (number of desired generated sentences) (one or more text files)
Ex. python3 ngram.py 3 3 pride_and_prejudice.txt huckleberry_finn.txt
    > Gardiner looking at her doubtingly.
    > And mighty glad to see harvey and oh my lordy lordy.
    > Hold on a sunday school book out with all the time.
Algorithm:
In this program, text files are parsed and modified (in a copy) with certain punctuation excluded
(i.e. "?", "'", ",", etc.). Start and end tags are then placed in the appropriate places (beginning and
end of sentence). The text is then tokenized and organized into a dictionary of occurrences according to
previous history. Another dictionary stores the overall occurrences of the said history. Words are then
selected based on relative frequency and previous history. The words are finally pieced together and
cleaned up to form sentences.
"""

import random
import re
import sys

ngram_dict = {}  # for occurrences of words based on previous history
history_freq_dict = {}  # for total occurrences of the (n-1)-grams
tokens = []  # stores tokens
ngram = []  # holds tokens when in transition
sentences = []  # for selected words

num_for_gram = 0  # number to implement for n-gram model
num_of_sentences = 0  # number of sentences to generate
text_files = []

print("Serena Cheng | Assignment 2: Ngrams")

# stores user arguments
for i in range(1, len(sys.argv)):
    if i == 1:
        num_for_gram = int(sys.argv[i])
    elif i == 2:
        num_of_sentences = int(sys.argv[i])
    else:
        text_files.append(sys.argv[i])

# parsing a modifying copy of text files
for txt_file in text_files:
    with open(txt_file, "r", encoding="utf-8-sig") as file:
        content = file.read().lower()

    # compile start tags equal to n-1
    start_tags = ""
    for _ in range(1, num_for_gram):
        start_tags += "<s> "

    # remove unnecessary punctuation
    content = re.sub(r'[,*\-_;:()\"]', ' ', content)
    content = re.sub(r'\'', '', content)

    # add start and end tags where needed
    content = start_tags + content
    content = re.sub(r'[.!?]', ' .', content)
    edit = content.split(".")
    end_start_tags = "<e> " + start_tags
    content = end_start_tags.join(map(str, edit))

    content = re.sub(r'\s+', ' ', content)

    # create tokens
    tokens.extend(content.split())

index = 0
# transition from tokens to ngram dictionary
while index < len(tokens):
    ngram.append(tokens[index])

    # when number of tokens is equal to n
    if len(ngram) == num_for_gram:
        word = ngram.pop()  # word
        key = " ".join(map(str, ngram))  # history

        # insert number of occurrences of word based on history in dictionary
        if key in ngram_dict.keys():
            if word in ngram_dict[key]:
                ngram_dict[key][word] += 1
            else:
                ngram_dict[key][word] = 1
        else:
            ngram_dict[key] = {word: 1}

        # set index back so overlapping n-grams can be collected
        index -= (num_for_gram - 2)
        ngram.clear()
    else:
        index += 1

# create dictionary to store total occurrences of history
for history, word_dict in ngram_dict.items():
    history_freq_dict[history] = sum(word_dict.values())

ngram.clear()
sentence_count = 0
index = 0
# piece selected words together based on history
while sentence_count != num_of_sentences:
    # begin sentence with start tag
    if len(sentences) == 0:
        begin_tag = ""
        for _ in range(1, num_for_gram):
            begin_tag += "<s> "

        sentences.extend(begin_tag.split())
        ngram.extend(sentences)

        index += (len(sentences) - 1)

    history = " ".join(map(str, ngram))

    possible_words = []  # for words to be chosen from
    probabilities = []  # for relative frequencies

    # calculate relative frequencies of each possible word
    for k, v in ngram_dict[history].items():
        possible_words.append(k)

        probability = round(v / history_freq_dict[history], 10)
        probabilities.append(probability)

    selected_word = ""
    # select word from possible words based on calculated weights
    while True:
        selected_word = random.choices(possible_words, probabilities)
        selected_word = re.sub(r'[\[\]\'\"]', '', str(selected_word))

        # too many ellipses-influenced tokens keep showing so guarded against that
        if selected_word == "<e>" and sentences[index] == "<s>":
            continue
        break

    # keep track of end of sentences
    if selected_word == "<e>":
        sentence_count += 1

    sentences.append(selected_word)
    ngram.append(selected_word)
    ngram.pop(0)

    index += 1

# fix up and join words
generated_sentences = " ".join(map(str, sentences))
generated_sentences = re.sub(r'<s> ', '', generated_sentences)

sentences = generated_sentences.split("<e>")
sentences.pop()

for sentence in sentences:
    print(sentence.strip().capitalize() + ".")
