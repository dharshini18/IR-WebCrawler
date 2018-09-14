import os
import operator

# Generate a term frequency table comprising of two columns: term and tf
Inverted_Index_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Inverted_Index/"
Term_Frequency_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Tables/Term_Frequency"


# Formatting the unigram Inverted Index
def unigram_formatting(file_lines):
    term_frequency_map = {}
    for line in file_lines:
        term_frequency = 0
        tokens = line.split(" ", 1)
        key = tokens.pop(0)
        tokens = tokens[0].split(" ")
        for token in tokens:
            if "]" in token:
                value = token.rstrip("]")
                value = value.rstrip("'")
                value = value.lstrip("'")
                term_frequency = term_frequency + int(value)
        term_frequency_map[key] = term_frequency
    return term_frequency_map


# Formatting the bigram Inverted Index
def bigram_formatting(file_lines):
    term_frequency_map = {}
    for line in file_lines:
        term_frequency = 0
        tokens = line.split(" ", 2)
        key1 = tokens.pop(0)
        key2 = tokens.pop(0)
        key = key1 + " " + key2
        tokens = tokens[0].split(" ")
        for token in tokens:
            if "]" in token:
                value = token.rstrip("]")
                value = value.rstrip("'")
                value = value.lstrip("'")
                term_frequency = term_frequency + int(value)
        term_frequency_map[key] = term_frequency
    return term_frequency_map


# Formatting the trigram Inverted Index
def trigram_formatting(file_lines):
    term_frequency_map = {}
    for line in file_lines:
        term_frequency = 0
        tokens = line.split(" ", 3)
        key1 = tokens.pop(0)
        key2 = tokens.pop(0)
        key3 = tokens.pop(0)
        key = key1 + " " + key2 + " " + key3
        tokens = tokens[0].split(" ")
        for token in tokens:
            if "]" in token:
                value = token.rstrip("]")
                value = value.rstrip("'")
                value = value.lstrip("'")
                term_frequency = term_frequency + int(value)
        term_frequency_map[key] = term_frequency
    return term_frequency_map


#  To apply different formatting while reading the Inverted Indexes
def format_file_lines(file_lines, filename):
    if filename == "Unigram.txt":
        unigram_map = unigram_formatting(file_lines)
        return unigram_map
    elif filename == "Bigram.txt":
        bigram_map = bigram_formatting(file_lines)
        return bigram_map
    elif filename == "Trigram.txt":
        trigram_map = trigram_formatting(file_lines)
        return trigram_map
    else:
        raise Exception(
            "The filename provided is not valid. Kindly rename file to Unigram/Bigram/Trigram depending on the type")


# Write the term frequency table to a file
def write_term_frequency_table(filename, sorted_items):
    filename = "term_frequency_" + filename
    folder = os.path.join(Term_Frequency_Location, filename)
    file_new = open(folder, "a+")
    file_new.write("File - Format (term term_frequency)")
    file_new.write("\n")
    file_new.write("-------------------------------------")
    file_new.write("\n")
    for value in sorted_items:
        value0 = str(value[0])
        file_new.write(value0.encode(encoding='utf_8', errors='ignore'))
        file_new.write(" ")
        value1 = str(value[1])
        file_new.write(value1.encode(encoding='utf_8', errors='ignore'))
        file_new.write("\n")
    file_new.close()


# To sort the terms - descending order of their term frequency (most to least)
def sort_term_frequency_values(term_frequency_map):
    sorted_items = sorted(term_frequency_map.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_items


# Read the contents of the Inverted Index to generate a term frequency table
def read_index_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        file_lines = [line.rstrip('\n') for line in file_f]
        file_lines = [line.rstrip(' ') for line in file_lines]
        term_frequency_map = format_file_lines(file_lines, filename)
        sorted_items = sort_term_frequency_values(term_frequency_map)
        write_term_frequency_table(filename, sorted_items)


# Main Function
def main():
    read_index_contents(Inverted_Index_Location)


if __name__ == "__main__":
    main()
