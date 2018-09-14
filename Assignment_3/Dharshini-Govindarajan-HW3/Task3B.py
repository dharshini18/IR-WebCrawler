import os
import collections

# Generate a document frequency table comprising of three columns: term, docIDs, and df
Inverted_Index_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Inverted_Index/"
Document_Frequency_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Tables/Document_Frequency"


# Formatting the unigram Inverted Index
def unigram_formatting(file_lines):
    document_frequency_map = {}
    for line in file_lines:
        documentId = []
        tokens = line.split(" ", 1)
        key = tokens.pop(0)
        tokens = tokens[0].split(" ")
        for token in tokens:
            if "[" in token:
                value = token.lstrip("[")
                value = value.rstrip(",")
                value = value.rstrip("'")
                value = value.lstrip("'")
                documentId.append(value)
            document_frequency_map[key] = documentId
    return document_frequency_map


# Formatting the bigram Inverted Index
def bigram_formatting(file_lines):
    document_frequency_map = {}
    for line in file_lines:
        documentId = []
        tokens = line.split(" ", 2)
        key1 = tokens.pop(0)
        key2 = tokens.pop(0)
        key = key1 + " " + key2
        tokens = tokens[0].split(" ")
        for token in tokens:
            if "[" in token:
                value = token.lstrip("[")
                value = value.rstrip(",")
                value = value.rstrip("'")
                value = value.lstrip("'")
                documentId.append(value)
            document_frequency_map[key] = documentId
    return document_frequency_map


# Formatting the trigram Inverted Index
def trigram_formatting(file_lines):
    document_frequency_map = {}
    for line in file_lines:
        documentId = []
        tokens = line.split(" ", 3)
        key1 = tokens.pop(0)
        key2 = tokens.pop(0)
        key3 = tokens.pop(0)
        key = key1 + " " + key2 + " " + key3
        tokens = tokens[0].split(" ")
        for token in tokens:
            if "[" in token:
                value = token.lstrip("[")
                value = value.rstrip(",")
                value = value.rstrip("'")
                value = value.lstrip("'")
                documentId.append(value)
            document_frequency_map[key] = documentId
    return document_frequency_map


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


# To sort the terms - by lexicographical order
def sort_document_frequency_values(document_frequency_map):
    sorted_keys = sorted(document_frequency_map.keys())
    return sorted_keys


# To generate an ordered dictionary (Term, DocumentID's, documentFrequency)
def generate_ordered_dictionary(sorted_keys, document_frequency_map):
    ordered_dictionary = collections.OrderedDict()
    for key in sorted_keys:
        values = document_frequency_map[key]
        count = len(values)
        ordered_dictionary[key] = {"Documents": values, "Frequency": count}
    return ordered_dictionary


# Write the document frequency table to a file
def write_document_frequency_table(filename, ordered_document_frequency):
    filename = "document_frequency_" + filename
    folder = os.path.join(Document_Frequency_Location, filename)
    file_new = open(folder, "a+")
    file_new.write("File - Format (term document_ID's document_frequency)")
    file_new.write("\n")
    file_new.write("------------------------------------------------------")
    file_new.write("\n")
    for key, values in ordered_document_frequency.iteritems():
        file_new.write(key.encode(encoding='utf_8', errors='ignore'))
        file_new.write(" ")
        documents = values["Documents"]
        frequency = values["Frequency"]
        for doc in documents:
            file_new.write(doc.encode(encoding='utf_8', errors='ignore'))
            file_new.write(" ")
        frequency = str(frequency)
        file_new.write(frequency.encode(encoding='utf_8', errors='ignore'))
        file_new.write("\n")
    file_new.close()


# Read the contents of the Inverted Index to generate a document frequency table
def read_index_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        file_lines = [line.rstrip('\n') for line in file_f]
        file_lines = [line.rstrip(' ') for line in file_lines]
        document_frequency_map = format_file_lines(file_lines, filename)
        sorted_keys = sort_document_frequency_values(document_frequency_map)
        ordered_document_frequency = generate_ordered_dictionary(sorted_keys, document_frequency_map)
        write_document_frequency_table(filename, ordered_document_frequency)


# Main Function
def main():
    read_index_contents(Inverted_Index_Location)


if __name__ == "__main__":
    main()
