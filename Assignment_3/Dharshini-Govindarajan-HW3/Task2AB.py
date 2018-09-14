import os
import nltk
from nltk.util import ngrams

# Store the number of terms in each document in a separate data structure

CORPUS_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Corpus/"
Unigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Unigram"
Bigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Bigram"
Trigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Trigram"


# Write the contents of the Unigram to files
def write_uni_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    for key, value in corpus_map.iteritems():
        temp_string = key[0] + " " + filename + " " + str(value)
        file_new.write(temp_string.encode(encoding='utf_8', errors='ignore'))
        file_new.write("\n")
    file_new.close()


# Write the contents of the Bigram to files
def write_bi_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    for key, value in corpus_map.iteritems():
        key_combined = ' '.join(str(k) for k in key)
        temp_string = "(" + key_combined + ")" + " " + filename + " " + str(value)
        file_new.write(temp_string.encode(encoding='utf_8', errors='ignore'))
        file_new.write("\n")
    file_new.close()


# Write the contents of the Trigram to files
def write_tri_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    for key, value in corpus_map.iteritems():
        key_combined = ' '.join(str(k) for k in key)
        temp_string = "(" + key_combined + ")" + " " + filename + " " + str(value)
        file_new.write(temp_string.encode(encoding='utf_8', errors='ignore'))
        file_new.write("\n")
    file_new.close()


# To generate unigrams from the corpus
def generate_uni_grams(tokens, filename):
    unigrams = ngrams(tokens, 1)
    corpus_map = nltk.FreqDist(unigrams)
    write_uni_gram_contents(corpus_map, Unigram_Location, filename)


# To generate bigrams from the corpus
def generate_bi_grams(tokens, filename):
    bigrams = ngrams(tokens, 2)
    corpus_map = nltk.FreqDist(bigrams)
    write_bi_gram_contents(corpus_map, Bigram_Location, filename)


# To generate trigrams from the corpus
def generate_tri_grams(tokens, filename):
    bigrams = ngrams(tokens, 3)
    corpus_map = nltk.FreqDist(bigrams)
    write_tri_gram_contents(corpus_map, Trigram_Location, filename)


# To generate n-grams (where n = 1, 2, 3) from the corpus
def generate_n_grams(tokens, filename):
    generate_uni_grams(tokens, filename)
    generate_bi_grams(tokens, filename)
    generate_tri_grams(tokens, filename)


# Convert the contents of the file to tokens
def load_file_as_tokens(file_f):
    content = file_f.read()
    tokens = content.split(" ")
    return tokens


# Read the contents of the corpus
def read_corpus_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        tokens = load_file_as_tokens(file_f)
        file_f.close()
        generate_n_grams(tokens, filename)


# Main Function
def main():
    read_corpus_contents(CORPUS_Location)


if __name__ == "__main__":
    main()
