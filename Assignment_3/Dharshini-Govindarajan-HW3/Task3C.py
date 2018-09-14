import os
import collections
from nltk.corpus import stopwords

# Generate three stop lists, one per index
Stop_Words_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Stopwords"
Term_Frequency = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Tables/Term_Frequency/"
stop_words = set(stopwords.words('english'))


# Formatting the unigram Inverted Index
def unigram_formatting(file_lines):
    term_frequency_map = collections.OrderedDict()
    unigrams = []
    for line in file_lines:
        tokens = line.split(" ")
        key = tokens.pop(0)
        unigrams.append(key)
        count = tokens.pop(0)
        term_frequency_map[key] = int(count)
    return unigrams, term_frequency_map


# Formatting the bigram Inverted Index
def bigram_formatting(file_lines):
    term_frequency_map = collections.OrderedDict()
    bigrams = []
    for line in file_lines:
        tokens = line.split(" ")
        key1 = tokens.pop(0)
        key2 = tokens.pop(0)
        key = key1 + " " + key2
        bigrams.append(key)
        count = tokens.pop(0)
        term_frequency_map[key] = int(count)
    return bigrams, term_frequency_map


# Formatting the trigram Inverted Index
def trigram_formatting(file_lines):
    term_frequency_map = collections.OrderedDict()
    trigrams = []
    for line in file_lines:
        tokens = line.split(" ")
        key1 = tokens.pop(0)
        key2 = tokens.pop(0)
        key3 = tokens.pop(0)
        key = key1 + " " + key2 + " " + key3
        trigrams.append(key)
        count = tokens.pop(0)
        term_frequency_map[key] = int(count)
    return trigrams, term_frequency_map


#  To apply different formatting while reading the Inverted Indexes
def format_file_lines(file_lines, filename):
    if filename == "term_frequency_Unigram.txt":
        unigrams, unigram_map = unigram_formatting(file_lines)
        return unigrams, unigram_map
    elif filename == "term_frequency_Bigram.txt":
        bigrams, bigram_map = bigram_formatting(file_lines)
        return bigrams, bigram_map
    elif filename == "term_frequency_Trigram.txt":
        trigrams, trigram_map = trigram_formatting(file_lines)
        return trigrams, trigram_map
    else:
        raise Exception(
            "The filename provided is not valid. Kindly rename file to Unigram/Bigram/Trigram depending on the type")


# To generate unigram Stopwords
def unigram_stop_words(words_map):
    count_iteration = 0
    stop_words_unigram = []
    for key, value in words_map.iteritems():
        if count_iteration > 131:
            break
        stop_words_unigram.append(key)
        count_iteration += 1
    return stop_words_unigram


# To generate bigram Stopwords
def bigram_stop_words(words_map):
    count_iteration = 0
    stop_words_bigram = []
    for key, value in words_map.iteritems():
        if count_iteration > 222:
            break
        stop_words_bigram.append(key)
        count_iteration += 1
    return stop_words_bigram


# To generate trigram Stopwords
def trigram_stop_words(words_map):
    count_iteration = 0
    stop_words_bigram = []
    for key, value in words_map.iteritems():
        if count_iteration > 100:
            break
        stop_words_bigram.append(key)
        count_iteration += 1
    return stop_words_bigram


# To generate n-gram Stopwords
def generate_stop_words(words_map, filename):
    filename = filename.replace("term_frequency_", "")
    if filename == "Unigram.txt":
        stop_words_gram = unigram_stop_words(words_map)
        return stop_words_gram
    elif filename == "Bigram.txt":
        stop_words_gram = bigram_stop_words(words_map)
        return stop_words_gram
    elif filename == "Trigram.txt":
        stop_words_gram = trigram_stop_words(words_map)
        return stop_words_gram
    else:
        raise Exception(
            "The filename provided is not valid. Kindly rename file to Unigram/Bigram/Trigram depending on the type")


# To write the stop words to a file
def write_stop_words_to_file(stop_words_grams, filename):
    filename = filename.replace("term_frequency_", "")
    filename = "stopwords_" + filename
    folder = os.path.join(Stop_Words_Location, filename)
    file_new = open(folder, "a+")
    for word in stop_words_grams:
        file_new.write(word.encode(encoding='utf_8', errors='ignore'))
        file_new.write("\n")
    file_new.close()


# Read the contents of the Inverted Index to generate stop words
def read_index_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        file_lines = [line.rstrip('\n') for line in file_f.readlines()[2:]]
        file_lines = [line.rstrip(' ') for line in file_lines]
        list_of_words, words_map = format_file_lines(file_lines, filename)
        stop_words_grams = generate_stop_words(words_map, filename)
        write_stop_words_to_file(stop_words_grams, filename)


# Main Function
def main():
    read_index_contents(Term_Frequency)


if __name__ == "__main__":
    main()
