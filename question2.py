# Author: Jan van Rooyen
# Student Number: 57676615
# Module: COS486-1

# Class imports
from sortedcontainers import SortedSet
from collections import Counter
from nltk.corpus import brown
import nltk

# File to tag
FILE_TO_TAG='question_2_resources/pos_test.txt'

# To enable debug logging, change to True
# 0 - INFO
# 1 - DEBUG
# 2 - FINE
LOG_LEVEL = 2
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
    if LOG_LEVEL > 2:
        print('Starting arg_max_for_word')

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
    if LOG_LEVEL > 2:
        print('Ending arg_max_for_word')
    return arg_max_pos_tag
# end def arg_max_for_word(corpus, word)


# Function used to compute the argmax function for each word
def argmax():
    if LOG_LEVEL > 1:
        print('Starting argmax')
    # Grab the POS tagged sentences with from the 'news' category.
    brown_sentences = brown.tagged_sents(categories="news")

    # Get a list of unique words.
    distinct_word_list = get_distinct_words(brown_sentences)
    # arg_max_for_word(brown_sentences, distinct_word_list)

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


# Function used to go through all the words in a given file and tag them as per the
# MLE of the POS tag given the brown corpus
def tag_file(file):
    if LOG_LEVEL > 1:
        print('Staring tag_file')
    input_file = open(file, "r")
    output_file = open(file + '_out', "w")

    # Grab the POS tagged sentences with from the 'news' category.
    brown_sentences = brown.tagged_sents(categories="news")

    for line in input_file:
        tagged_line = ''
        for word in line.split():
            pos_tag = arg_max_for_word(brown_sentences, word)

            # If we do not find any words that match, that means the given word is not in the corpus.
            # Use the tag 'NN' instead.
            if not pos_tag:
                pos_tag = 'NN'
            tagged_line = tagged_line + word+ '/' +pos_tag + ' '
        tagged_line = tagged_line + '\n'
        output_file.write(tagged_line)
        if LOG_LEVEL > 1:
            print(tagged_line)

    output_file.close()
    input_file.close()
    if LOG_LEVEL > 1:
        print('Ending tag_file')
# end def tag_file(FILE_TO_TAG)


def confusion_matrix():
    if LOG_LEVEL > 1:
        print('Staring confusion_matrix')

    # Input file
    input_file = 'question_2_resources/pos_test.txt_out'
    pos_test = open(input_file, "r")

    # Golden file
    golden_file = 'question_2_resources/pos_golden_standard.txt'
    pos_golden_standard = open(golden_file, "r")

    # We look at each word and see what it was supposed to be ... and what it was tagged as.
    tag_list = SortedSet()
    incorrect_tags = []
    total_miss_tags = 0
    test_line = 'not empty'
    while test_line:
        test_line = pos_test.readline()
        test_words = test_line.split()

        golden_line = pos_golden_standard.readline()
        golden_words = golden_line.split()

        i = 0
        while i < len (golden_words):
            test_word = test_words[i].split('/')[0]
            test_tag = test_words[i].split('/')[1]
            golden_word = golden_words[i].split('/')[0]
            golden_tag = golden_words[i].split('/')[1]

            tag_list.add(golden_tag)
            tag_list.add(test_tag)

            if test_tag != golden_tag:
                if LOG_LEVEL > 2:
                    print(test_word + '/' + test_tag + ' --> ' + golden_word + '/' + golden_tag)
                incorrect_tags.append(golden_tag + '/' + test_tag)
                total_miss_tags = total_miss_tags + 1

            i = i + 1

    tagging_statistics = Counter(incorrect_tags)

    if LOG_LEVEL > 1:
        print(tagging_statistics)

    print(tag_list)
    print()
    # Print column names
    print(''.ljust(10, ' '), end='')
    for col_tag in tag_list:
        print(col_tag.ljust(5, ' '), end='')

    print()
    for row_tag in tag_list:
        print(row_tag.ljust(10, ' '), end='')
        for col_tag in tag_list:
            tag = row_tag + '/' + col_tag

            if tag in tagging_statistics.keys():
                tag_count = tagging_statistics[tag]
                perc = (tag_count / total_miss_tags) * 100
                perc_str = '{:.1f}'.format(perc)
                print(perc_str.ljust(5, ' '), end='')
            else:
                print('-'.ljust(5, ' '), end='')

        print()

    print("\n\n")

    pos_test.close()
    pos_golden_standard.close()
    if LOG_LEVEL > 1:
        print('Ending confusion_matrix')
# end def confusion_matrix


# Functions used as the main entry into the application
def main():
    if LOG_LEVEL > 1:
        print('Staring main')

    # No file available via the MyUnisa portal, downloading the standard Brown Corpus
    download_corpus()

    # Part a
    # argmax()

    # Part b
    # tag_file(FILE_TO_TAG)

    # Part c
    confusion_matrix()
    if LOG_LEVEL > 1:
        print('Ending main')
# end def main()


if __name__ == '__main__':
    main()
