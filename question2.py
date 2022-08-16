# Author: Jan van Rooyen
# Student Number: 57676615
# Module: COS486-1

# Class imports
from collections import Counter
from nltk.corpus import brown
import nltk


# To enable debug logging, change to True
# 0 - INFO
# 1 - DEBUG
# 2 - FINE
LOG_LEVEL = 1
UNIQUE_WORD_LIST = set()

# Since this is a much larger corpus than Unisa's one, we limit the words to process.
# Set to -1 to process all words.
WORD_LIMIT=50


# Function used to find the list of unique words given a corpus
def get_distinct_words(corpus):
    if LOG_LEVEL > 1:
        print('Starting get_distinct_words')

    word_list = set()
    # The sentences provided are already split up into a list in lists.
    for sentence in corpus:
        for tag in sentence:
            word_list.add(tag[0])

    if LOG_LEVEL > 1:
        print('Completed get_distinct_words')
    return word_list
# end def get_distinct_words(corpus)


# Function used to determine the most likely POS tag used for a unique word
def arg_max_for_word(corpus, word):
    if LOG_LEVEL > 1:
        print('Starting word_processor')

    # Create an array of all the tags in the corpus that the given word was tagged with
    tag_counts = []
    for corpus_sentence in corpus:
        for corpus_word in corpus_sentence:
            if word == corpus_word[0]:
                tag_counts.append(corpus_word[1])

    # Use a Counter to count the number of tags and summarize the result
    word_statistics = Counter(tag_counts)

    # Find the pos tag that had the highest count and return as the most likely tag to be used
    # for a given word.
    arg_max_pos_tag = ''
    highest_count = 0
    for pos in word_statistics:
        if word_statistics[pos] > highest_count:
            highest_count = word_statistics[pos]
            arg_max_pos_tag = pos

    if LOG_LEVEL > 2:
        print(word, end=' --> ')
        print(word_statistics, end=' --> ')
        print(arg_max_pos_tag)
    if LOG_LEVEL > 1:
        print('Ending word_processor')
    return arg_max_pos_tag
# end def word_processor(corpus, word)


# Function used to compute the argmax function for each word
def argmax():
    if LOG_LEVEL > 1:
        print('Starting argmax')
    # Grab the POS tagged sentences with from the 'news' category.
    brown_sentences = brown.tagged_sents(categories="news")

    # Get a list of unique words.
    distinct_word_list = get_distinct_words(brown_sentences)
    arg_max_for_word(brown_sentences, distinct_word_list)

    # The sentences provided are already split up into a 2-d arrays.
    counter = 0
    for word in distinct_word_list:
        arg_max_pos_tag = arg_max_for_word(brown_sentences, word)
        if LOG_LEVEL > 0:
            print(counter,'/', len(distinct_word_list), '-', word, 'is most likely going to be tagged as:', arg_max_pos_tag)

        if WORD_LIMIT > 0:
            if counter > WORD_LIMIT:
                break
        counter = counter + 1

    if LOG_LEVEL > 1:
        print('Ending argmax')

# end def argmax ()


# Function used to download the latest copy of the full Brown corpus
def download_corpus():
    if LOG_LEVEL > 1:
        print('Staring download_corpus')

    nltk.download('brown')

    if LOG_LEVEL > 1:
        print('Ending download_corpus')
# end def download_corpus()


# Functions used as the main entry into the application
def main():
    if LOG_LEVEL > 1:
        print('Staring main')

    # No file available via the MyUnisa portal, downloading the standard Brown Corpus
    download_corpus()
    argmax()

    if LOG_LEVEL > 1:
        print('Ending main')
# end def main()


if __name__ == '__main__':
    main()
