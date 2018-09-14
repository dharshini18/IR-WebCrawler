import os
import optparse
from string import punctuation
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner

# Generating the corpus
BFS_Files_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/BFS_Files/"
CORPUS_Location = "C:/Users/Dharshini/PycharmProjects/IR_WebCrawler/HW3/Corpus"


# To parse the input from the user
def parse_input():
    parser_for_input = optparse.OptionParser()
    args = parser_for_input.parse_args()
    return args


# Read the contents of the files from the folders
def read_file_from_folder(file_location, parser_options):
    for filename in os.listdir(file_location):
        filter_html_content(filename, file_location, parser_options)


# To write the visited links to a file
def write_to_file(filename, corpus):
    print filename
    folder = os.path.join(CORPUS_Location, filename)
    file_new = open(folder, "a+")
    file_new.write(corpus.encode(encoding='utf_8', errors='ignore'))
    file_new.close()


# To filter html content from the file
def filter_html_content(filename, file_location, parser_options):
    file_f = open(file_location + filename)
    soup = BeautifulSoup(file_f.read(), 'html.parser')
    file_f.close()
    corpus_contents = allowed_content(soup, parser_options)
    write_to_file(filename, corpus_contents)


# To generate a clean content for the corpus after applying Case folding and Removing punctuations
def format_soup_object(soup_object, parser_options):
    clean_content = BeautifulSoup(soup_object, 'lxml').get_text()
    clean_content = ' '.join(clean_content.split())
    clean_content = clean_content.replace('html ', '')
    clean_content = ''.join(content for content in clean_content if 0 < ord(content) < 127)
    if parser_options == "CF":
        clean_content = case_folding(clean_content)
    elif parser_options == "RP":
        clean_content = remove_punctuations(clean_content)
    else:
        clean_content = case_folding(clean_content)
        clean_content = remove_punctuations(clean_content)
    return clean_content


# To change the Upper case letters to lower case
def case_folding(clean_content):
    clean_content = clean_content.lower()
    return clean_content


# To remove punctuation characters from the content
def remove_punctuations(clean_content):
    clean_content = ''.join(characters for characters in clean_content if characters not in '}{][)(\><=')
    clean_content = ' '.join(token.strip(punctuation) for token in clean_content.split() if token.strip(punctuation))
    clean_content = ' '.join(token.replace("'", "") for token in clean_content.split() if token.replace("'", ""))
    clean_content = ' '.join(clean_content.split())
    return clean_content


# To generate cleaner object (Filter out unnecessary information to focus on the content)
def set_cleaner_parameters():
    reject_list = ['script', 'noscript', 'style', 'meta', 'semantics', 'img', 'label', 'table', 'li', 'ul',
                   'ol', 'nav', 'dl', 'dd', 'sub', 'sup', 'math']
    accept_list = ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'span', 'b', 'a', 'u', 'i', 'body']
    html_cleaner = Cleaner()
    html_cleaner.remove_unknown_tags = True
    html_cleaner.processing_instructions = True
    html_cleaner.style = True
    html_cleaner.comments = True
    html_cleaner.scripts = True
    html_cleaner.javascript = True
    html_cleaner.meta = True
    html_cleaner.links = True
    html_cleaner.embedded = True
    html_cleaner.annoying_tags = True
    html_cleaner.frames = True
    html_cleaner.forms = True
    html_cleaner.remove_tags = accept_list
    html_cleaner.kill_tags = reject_list
    return html_cleaner


# To eliminate the unwanted tags from the parsed html object
def extract_unwanted_tags(soup_object, parser_options):
    nav_content = soup_object.find('div', class_='mw-jump')
    footer = soup_object.find('div', class_='printfooter')
    siteSub = soup_object.find('div', id='siteSub')
    if nav_content:
        soup_object.find('div', class_='mw-jump').decompose()

    if footer:
        soup_object.find('div', class_='printfooter').decompose()

    if siteSub:
        soup_object.find('div', id='siteSub').decompose()
    html_cleaner = set_cleaner_parameters()
    title_html = soup_object.find('title')
    body_content = soup_object.find('div', {'id': 'bodyContent'})
    soup_object = html_cleaner.clean_html(str(title_html) + " " + str(body_content))
    clean_content = format_soup_object(soup_object, parser_options)
    return clean_content


def allowed_content(soup_object, parser_options):
    clean_content = extract_unwanted_tags(soup_object, parser_options)
    return clean_content


# Main Function
def main():
    args = parse_input()
    argument1 = args[1]
    read_file_from_folder(BFS_Files_Location, argument1)


if __name__ == "__main__":
    main()
