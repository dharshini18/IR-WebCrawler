import math
import operator
import optparse

# PageRank damping/teleportation factor
in_links = set()
in_links_for_count = []

FILE_NAME_PREFIX = "PageRank"


# Read contents from the file and add it to a dictionary
def read_contents_from_the_file(filename):
    M = {}
    P = set()
    file_f = open(filename, "r")
    content = file_f.readlines()

    for line in content:
        array_characters = line.split(" ")
        for char in array_characters:
            if char == array_characters[0]:
                P.add(char.rstrip('\n'))
        M[array_characters[0]] = []
        first_element = array_characters[0]
        array_characters.remove(array_characters[0])
        temp_array = []
        for character in array_characters:
            in_links_for_count.append(character.rstrip('\n'))
            temp_array.append(character.rstrip('\n'))
            for value in temp_array:
                in_links.add(value.rstrip('\n'))
            M[first_element] = temp_array
    file_f.close()
    return M, P


# Find links without out-links
def fetch_pages_without_out_links(P):
    page_with_no_out_links = set()
    for page in P:
        if page not in in_links:
            page_with_no_out_links.add(page)  # Set of links without out-links
    return page_with_no_out_links


# Find the number of out-links for each page
def fetch_count_of_out_links(P):
    out_links_count = {}
    for page in P:
        count = in_links_for_count.count(page)
        if count != 0:
            out_links_count[page] = count
    return out_links_count


# To check if the perplexity converges
def iteration_check(iteration_count):
    list_iterations = []
    for value in iteration_count:
        list_iterations.append(math.floor(value))
    temp_value = list_iterations[0]
    for index, value in enumerate(list_iterations):
        if value == temp_value:
            list_iterations[index] = True
        else:
            list_iterations[index] = False
    if len(list_iterations) >= 4 and all(list_iterations):
        return True
    else:
        return False


# Page Rank Algorithm
def calculate_page_rank(P, S, M, out_links_count, damping_factor):
    page_rank_values = {}
    count = []
    N = len(P)
    for page in P:
        page_rank_values[page] = 1.0 / N

    perplexity = calculate_perplexity(page_rank_values, P)
    count = count + [perplexity]
    # round = 1
    # filename = FILE_NAME_PREFIX + "Perplexity_G2.txt"
    # file_f = open(filename, "a+")

    while not iteration_check(count[-4:]):
        # file_f.write("Round" + str(round) + ":")
        # file_f.write("\t")
        # file_f.write(str(perplexity))
        # file_f.write("\n")
        newPR = {}
        sinkPR = 0
        for sink in S:
            sinkPR += page_rank_values[sink]
        for page in P:
            newPR[page] = (1.0 - damping_factor) / N
            newPR[page] += damping_factor * sinkPR / N
            for page_in in M[page]:
                if page_in in out_links_count and page_in in page_rank_values:
                    newPR[page] += damping_factor * page_rank_values[page_in] / out_links_count[page_in]
        for page in P:
            page_rank_values[page] = newPR[page]
        perplexity = calculate_perplexity(page_rank_values, P)
        count = count + [perplexity]
        # round = round + 1
    # file_f.close()
    return page_rank_values


# To calculate the entropy
def calculate_entropy(page_rank_values, P):
    entropy = 0
    for page in P:
        page_rank = page_rank_values[page]
        if page_rank > 0:
            entropy += (-(page_rank * math.log(page_rank, 2)))
    return entropy


# To calculate the perplexity
def calculate_perplexity(page_rank_values, P):
    # Perplexity = 2 ^ H(PR)
    entropy = calculate_entropy(page_rank_values, P)
    perplexity = pow(2, entropy)
    return perplexity


# To parse the input from the user
def parse_input():
    parser_for_input = optparse.OptionParser()
    args = parser_for_input.parse_args()
    return args


# To write the list to file (List of Page Ranks)
def write_list_to_file(links_page_rank, file_f):
    for link in links_page_rank:
        file_f.write(str(link[0]))
        file_f.write(",")
        file_f.write(str(link[1]))
        file_f.write("\n")


def main():
    args = parse_input()
    argument1 = args[1]
    # The argument is the filename
    filename = argument1[0]
    damping_factor = float(argument1[1])

    # M is the in-links to each page
    # P is the set of all pages
    M, P = read_contents_from_the_file(filename)
    S = fetch_pages_without_out_links(P)
    out_links_count = fetch_count_of_out_links(P)
    result_page_rank = calculate_page_rank(P, S, M, out_links_count, damping_factor)
    sorted_x = sorted(result_page_rank.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    filename = FILE_NAME_PREFIX + filename
    file_f = open(filename, "a+")
    write_list_to_file(sorted_x, file_f)

    # # Sort based on in_links
    # in_links_map = {}
    # for key in M.keys():
    #     value = M[key]
    #     in_links_map[key] = len(value)
    # sorted_y = sorted(in_links_map.items(), key=operator.itemgetter(1))
    # sorted_y.reverse()
    # filename = "InLinksSort" + filename
    # file_f = open(filename, "a+")
    # write_list_to_file(sorted_y, file_f)
    # file_f.close()


if __name__ == '__main__':
    main()
