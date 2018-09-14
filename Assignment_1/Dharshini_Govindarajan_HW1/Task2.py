from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import urlparse
import requests
import time
import re
import enchant

# Global Variables
max_depth = 6  # Maximum depth for crawling
url_limit = 1000  # Maximum number of links

# Delimiters
margin = ":"
samePage = "#"

# Page URLS
homePage = "https://www.wikipedia.org"
canonical_mainPage = "/wiki/Main_Page"

# File Prefix
FILE_NAME_PREFIX = "CrawledLinks_"

# Dictionary of English words to compare
word_list = enchant.Dict("en_US")


# Check if the word is present in the dictionary
def check_word_presence(array_new):
    boolean_value = False
    for word in array_new:
        if word != "" and len(word) != 0:
            if word_list.check(word):
                boolean_value = True
    return boolean_value


# Checks if the split (Word split into two, Eg - Green Power) is present in the dictionary
# i.e to check if they are valid english words
def check_split(new_string, lower_case):
    result = False
    start = new_string.find(lower_case)
    if lower_case == new_string:
        return True
    else:
        word_before = new_string[:start]
        word_after = new_string[start:]
        if word_before != "" and len(word_before) != 0:
            word_list.check(word_before)
            result = True
        if word_after != "" and len(word_after) != 0:
            word_list.check(word_after)
            result = True
    return result


# To check if the keyword is present in the link tokens
# Eg - "Power" is present in "GreenPower" (Ignore Case)
# Also to check if the tokens are present in the dictionary
def check_link_keys(lower_case, link_tokens):
    for token in link_tokens:
        token = token.encode('utf-8')
        if lower_case in token.lower():
            new_string = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", ' ', token.lower())
            new_string = new_string.replace("-", " ")
            new_string = new_string.replace("_", " ")
            array_new = new_string.split(" ")
            if word_list.check(new_string.lower()) or check_word_presence(array_new) or check_split(new_string,
                                                                                                    lower_case):
                return True
            else:
                return False
        else:
            return False


# To check if the keyword is present in the anchor tokens
# Eg - "Power" is present in "GreenPower" (Ignore Case)
# Also to check if the tokens are present in the dictionary
def check_anchor_keys(lower_case, anchor_tokens):
    for token in anchor_tokens:
        token = token.encode('utf-8')
        if lower_case in token.lower():
            new_string = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", ' ', token.lower())
            new_string = new_string.replace("-", " ")
            array_new = new_string.split(" ")
            if word_list.check(token.lower()) or check_word_presence(array_new):
                return True
            else:
                return False
        else:
            return False


# To check the relevance of the URL to the keyword or the set of keywords
def check_relevance_to_keyword(url, url_text, keywords):
    # Default Value
    relevance = None
    anchor_text = url_text  # Anchor text
    link_text = url  # URL
    start = int(link_text.find("/wiki/") + len("/wiki/") - 1)
    start = start + 1
    temp = link_text.encode('utf-8')
    link_text = temp[start:]

    # Tokenize the words in the anchor and URL
    anchor_tokens = word_tokenize(anchor_text)
    link_tokens = word_tokenize(link_text)
    for keyword in keywords:
        lower_case_keyword = keyword.lower()
        # Check if the anchor or URL contains the keyword
        anchor_boolean = check_anchor_keys(lower_case_keyword, anchor_tokens)
        link_boolean = check_link_keys(lower_case_keyword, link_tokens)
        relevance = anchor_boolean or link_boolean
    return relevance


# To fetch all the valid links at each depth
# Valid links include:
# Links that have the homepage as prefix
# Links that do not lead to the Main Page
# Links that do not contain the delimiters
# Links not in the marginal/References/Notes/See Also
# Links that are relevant to the keyword/set of keywords
def fetch_valid_links_at_depth(current_link, keywords, visited_set):
    # Time between requests
    time.sleep(1)
    valid_links = []
    # Fetch the response for the URL
    response = requests.get(current_link)
    # Parse the content to HTML format
    soup = BeautifulSoup(response.text, 'html.parser')
    # Fetch the content (Body) of the HTML
    body_content = soup.find('div', {'id': 'bodyContent'})
    # Ignore the References section of the HTML
    if len(soup.find('ol', class_='references') or ()) > 1:
        soup.find('ol', class_='references').decompose()
    # Fetch al the links that obey the pattern "/wiki/"
    links_in_content = body_content.find_all('a', {'href': re.compile("^/wiki/")})

    # Filter the links based on the conditions
    for link in links_in_content:
        if canonical_mainPage not in link.get('href'):
            if margin not in link.get('href'):
                url = urlparse.urljoin(homePage, link.get('href'))
                # Check the relevance of the URL
                # (If the anchor text or the url consists of the keyword or its variation)
                relevance = check_relevance_to_keyword(url, link.text, keywords)
                if relevance:
                    if samePage in link.get('href'):
                        # Fetch the links before the '#' tag
                        url = url[: url.index('#')]
                    if url not in valid_links and url not in visited_set:
                        valid_links.append(url)
    return valid_links


# To crawl the URLS in the order determined by Breadth First Search
# Links at the same level are crawled first, before visiting the next depth
def breadth_first_search(seed, keywords):
    data_structure = [seed]
    visited_links = []
    visited_set = set()
    links_at_next_depth = []
    depth_count = 1
    while data_structure:

        # Restrict the depth level
        if depth_count > max_depth:
            break

        # Restrict the total number of links visited
        if len(visited_links) >= url_limit:
            break

        # Current state is the front of the queue
        current_url = data_structure.pop(0)
        if current_url not in visited_links and current_url not in visited_set:
            # Explore the child nodes of every node
            next_links_to_visit = fetch_valid_links_at_depth(current_url, keywords, visited_set)
            if next_links_to_visit is not None:
                for url in next_links_to_visit:
                    # To fetch unique links (Avoid already visited/existing links)
                    if url not in links_at_next_depth and url not in visited_set:
                        links_at_next_depth.append(url)
                visited_links.append(current_url)
                visited_set.add(current_url)
        if not data_structure:
            # Update the next set of urls to be explored
            data_structure = links_at_next_depth
            links_at_next_depth = []
            # Increment the depth
            depth_count += 1

    return visited_links


# To write the visited links to a file
def write_to_file(links, file_f):
    for link in links:
        file_f.write(link)
        file_f.write("\n")


# Main Function
def main():
    seed = raw_input("Enter the seed URL (without quotations):")
    keywords = raw_input("Enter the keyword or keywords (without quotation and separated by a comma):").split(",")

    filename = FILE_NAME_PREFIX + "focusedCrawling.txt"
    file_bfs = open(filename, "w+")
    links_bfs = breadth_first_search(seed, keywords)
    write_to_file(links_bfs, file_bfs)
    file_bfs.close()


if __name__ == "__main__":
    main()
