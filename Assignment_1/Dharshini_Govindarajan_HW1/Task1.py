from bs4 import BeautifulSoup
import urlparse
import optparse
import requests
import time
import re
import sys
sys.setrecursionlimit(10 ** 6)

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

# Downloaded Documents
file_list = {}


# To parse the input from the user
def parse_input():
    parser_for_input = optparse.OptionParser()
    args = parser_for_input.parse_args()
    return args


# To fetch all the valid links at each depth
# Valid links include:
# Links that have the homepage as prefix
# Links that do not lead to the Main Page
# Links that do not contain the delimiters
# Links not in the marginal/References/Notes/See Also

def fetch_valid_links_at_depth(current_link):
    # Time between requests
    time.sleep(1)
    valid_links = []
    # Fetch the response for the URL
    response = requests.get(current_link)
    # download_raw_html(response, current_link)

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
                if samePage in link.get('href'):
                    # Fetch the links before the '#' tag
                    url = url[: url.index('#')]
                if url not in valid_links:
                    valid_links.append(url)
    return valid_links


# To crawl the URLS in the order determined by Breadth First Search
# Links at the same level are crawled first, before visiting the next depth
def breadth_first_search(seed):
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
            next_links_to_visit = fetch_valid_links_at_depth(current_url)
            if next_links_to_visit is not None:
                for url in next_links_to_visit:
                    # To fetch unique links (Avoid already visited/existing links)
                    if url not in links_at_next_depth:
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


# To crawl the URLS in the order determined by Depth First Search
# Links at the each level are crawled along a branch and back tracked once the max depth is reached
def depth_first_search(seed, depth, visited_links):
    depth_count = 1
    # Restrict the depth level and the total number of links visited
    if depth_count <= depth and len(visited_links) < url_limit:
        # Explore the child nodes of every node
        data_structure = fetch_valid_links_at_depth(seed)
        if seed not in visited_links:
            visited_links.append(seed)
        for link in data_structure:
            if len(visited_links) < url_limit and depth > depth_count:
                if link not in visited_links:
                    # To fetch unique links (Avoid already visited/existing links)
                    for url in depth_first_search(link, max_depth - 1, visited_links):
                        if url not in visited_links:
                            visited_links.append(url)
            else:
                break
    else:
        return []
    return visited_links


# To write the visited links to a file
def write_to_file(links, file_f):
    for link in links:
        file_f.write(link)
        file_f.write("\n")


# def download_raw_html(response, current_url):
#     file_name = current_url.encode("utf-8")
#     start = int(file_name.find("/wiki/") + len("/wiki/") - 1)
#     start = start + 1
#     temp = file_name.encode('utf-8')
#     link_text = temp[start:]
#     file_name = FILE_NAME_PREFIX + file_name
#     file_new = open(file_name, "w+")
#     file_new.write(response.read())
#     file_list.add(current_url, file_name)
#     file_new.close()


# Main Function
def main():
    args = parse_input()
    argument1 = args[1]
    # Seed - The start link
    # crawl - The crawl type
    seed, crawl = (argument1[0], argument1[1])

    # Crawl type - Depth First Search
    if crawl == "dfs":
        filename = FILE_NAME_PREFIX + "dfs.txt"
        file_dfs = open(filename, "a+")
        links_dfs = depth_first_search(seed, max_depth, [])
        write_to_file(links_dfs, file_dfs)
        file_dfs.close()

    # Crawl type - Breadth First Search
    if crawl == "bfs":
        filename = FILE_NAME_PREFIX + "bfs.txt"
        file_bfs = open(filename, "a+")
        links_bfs = breadth_first_search(seed)
        write_to_file(links_bfs, file_bfs)
        file_bfs.close()


if __name__ == "__main__":
    main()
