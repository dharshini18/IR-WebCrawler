import os

# Implementing an inverted indexer and creating inverted indexes
Unigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Unigram/"
Bigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Bigram/"
Trigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Trigram/"
Inverted_Index_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Inverted_Index"

Unigram_map, Bigram_map, Trigram_map = [{}, {}, {}]


# Read the contents of the generated n-grams
def read_file_contents(file_f, type_gram):
    file_map = {}
    for line in file_f.readlines():
        if type_gram == "Unigram":
            term, documentId, term_freq = line.split(" ")
            term_freq = term_freq.replace("\n", "")
            file_map[term] = [documentId, term_freq]
        if type_gram == "Bigram":
            term, term1, documentId, term_freq = line.split(" ")
            term = term.replace("(", "")
            term1 = term1.replace(")", "")
            term_freq = term_freq.replace("\n", "")
            key = term + " " + term1
            file_map[key] = [documentId, term_freq]
        if type_gram == "Trigram":
            term, term1, term2, documentId, term_freq = line.split(" ")
            term = term.replace("(", "")
            term2 = term2.replace(")", "")
            key = term + " " + term1 + " " + term2
            term_freq = term_freq.replace("\n", "")
            file_map[key] = [documentId, term_freq]
    return file_map


# Generate an index for the Unigram with the term as the key and the the term frequency as the value
def populate_unigram_index(file_f):
    file_contents = read_file_contents(file_f, "Unigram")
    for key, value in file_contents.iteritems():
        if key in Unigram_map:
            values = Unigram_map[key]
            values.append(value)
            Unigram_map[key] = values
        else:
            Unigram_map[key] = [value]


# Generate an index for the Bigram with the term as the key and the the term frequency as the value
def populate_bigram_index(file_f):
    file_contents = read_file_contents(file_f, "Bigram")
    for key, value in file_contents.iteritems():
        if key in Bigram_map:
            values = Bigram_map[key]
            values.append(value)
            Bigram_map[key] = values
        else:
            Bigram_map[key] = [value]


# Generate an index for the Trigram with the term as the key and the the term frequency as the value
def populate_trigram_index(file_f):
    file_contents = read_file_contents(file_f, "Trigram")
    for key, value in file_contents.iteritems():
        if key in Trigram_map:
            values = Trigram_map[key]
            values.append(value)
            Trigram_map[key] = values
        else:
            Trigram_map[key] = [value]


# Write the inverted indexes to the file
def write_inverted_indexes(file_location, index_type):
    filename = index_type + ".txt"
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    if index_type == "Unigram":
        content_map = Unigram_map
    elif index_type == "Bigram":
        content_map = Bigram_map
    else:
        content_map = Trigram_map
    for key in content_map:
        values = content_map[key]
        key = str(key)
        file_new.write(key.encode(encoding='utf_8', errors='ignore'))
        file_new.write(" ")
        for value in values:
            value = str(value)
            file_new.write(value.encode(encoding='utf_8', errors='ignore'))
            file_new.write(" ")
        file_new.write("\n")
    file_new.close()


# Read the unigrams
def read_unigram_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        populate_unigram_index(file_f)
    write_inverted_indexes(Inverted_Index_Location, "Unigram")


# Read the bigrams
def read_bigram_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        populate_bigram_index(file_f)
    write_inverted_indexes(Inverted_Index_Location, "Bigram")


# Read the trigrams
def read_trigram_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        populate_trigram_index(file_f)
    write_inverted_indexes(Inverted_Index_Location, "Trigram")


# Main Function
def main():
    read_unigram_contents(Unigram_Location)
    read_bigram_contents(Bigram_Location)
    read_trigram_contents(Trigram_Location)


if __name__ == "__main__":
    main()
