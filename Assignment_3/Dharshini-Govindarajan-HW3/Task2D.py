import os
import nltk

# Generate a unigram index storing the positions
CORPUS_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Corpus/"
Unigram_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/N-Grams/Unigram_Position"


# Convert the contents of the file to tokens
def load_file_as_tokens(file_f):
    content = file_f.read()
    tokens = content.split(" ")
    return tokens


# Generate n-grams with their positions in the document
def generate_n_grams(tokens, filename):
    corpus_map_with_positions = {}
    for index, token in enumerate(tokens):
        if token in corpus_map_with_positions:
            documentID, count, position = corpus_map_with_positions[token]
            count = count + 1
            position.append(index)
            corpus_map_with_positions[token] = [documentID, count, position]
        else:
            corpus_map_with_positions[token] = [filename, 1, [index]]
    return corpus_map_with_positions


# Write the Inverted Index with positions to file
def write_n_grams_with_positions(corpus_map_with_positions, filename):
    # Format written to the file(Term, documentID, term frequency, positions in the document)
    folder = os.path.join(Unigram_Location, filename)
    file_new = open(folder, "a+")
    for key in corpus_map_with_positions:
        documentId, count, positions = corpus_map_with_positions[key]
        key = str(key)
        file_new.write(key.encode(encoding='utf_8', errors='ignore'))
        file_new.write(" ")
        documentId = str(documentId)
        file_new.write(documentId.encode(encoding='utf_8', errors='ignore'))
        file_new.write(" ")
        count = str(count)
        file_new.write(count.encode(encoding='utf_8', errors='ignore'))
        file_new.write(" ")
        for position in positions:
            position = str(position)
            file_new.write(position.encode(encoding='utf_8', errors='ignore'))
            file_new.write(" ")
        file_new.write("\n")
    file_new.close()


# Read the contents of the corpus to create an index
def read_corpus_contents(file_location):
    for filename in os.listdir(file_location):
        file_f = open(file_location + filename)
        tokens = load_file_as_tokens(file_f)
        file_f.close()
        corpus_map_with_positions = generate_n_grams(tokens, filename)
        write_n_grams_with_positions(corpus_map_with_positions, filename)


# Main Function
def main():
    read_corpus_contents(CORPUS_Location)


if __name__ == "__main__":
    main()
