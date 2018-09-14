# IR-Web-crawler (Spring - 2018)

## Files/Softwares to download
* Python - https://www.python.org/download/releases/2.7/
* NLTK Data - http://www.nltk.org/data.html
* NLTK - To use NLTK, "import nltk" and follow http://www.nltk.org/index.html thereafter
* BeautifulSoup - To download and import follow https://www.crummy.com/software/BeautifulSoup/
* Requests - http://docs.python-requests.org/en/master/user/install/#install
* PyCharm (Optional) - https://www.jetbrains.com/pycharm/

## Task1: Crawling the document and building the graph:

#### To Execute BFS, 
1) Navigate to the folder, containing the file (Task1.py)
   Eg -> C:\Documents\IR_WebCrawler\crawler\HW2
2) Type - python Task1.py seed_url "bfs" (In pythonScript/pycharm terminal/cmd)
   seed is the start URL without quotations - https://en.wikipedia.org/wiki/Solar_eclipse
3) The graph is written to a file named G1.txt in the same folder as the project

#### To Execute DFS, 
1) Navigate to the folder, containing the file (Task1.py)
   Eg -> C:\Documents\IR_WebCrawler\crawler\HW2
2) Type - python Task1.py seed_url "dfs" (In pythonScript/pycharm terminal/cmd)
   seed is the start URL without quotations - https://en.wikipedia.org/wiki/Solar_eclipse
3) The graph is written to a file named G2.txt in the same folder as the project

## Task2: Page Rank Algorithm:

To Execute, 
1) Navigate to the folder, containing the file (Task2.py)
   Eg -> C:\Documents\IR_WebCrawler\crawler\HW2
2) Type - python Task2.py file_name damping_factor
   file_name without any quotations - sample.txt


Files - Genrated
1) G1.txt - BFS graph
2) G2.txt - DFS graph
3) PageRankG1_D1.txt - BFS graph with damping factor d = 0.85
4) PageRankG1_D2.txt - BFS graph with damping factor d = 0.55
5) PageRankG2_D1.txt - DFS graph with damping factor d = 0.85
6) PageRankG2_D1.txt - DFS graph with damping factor d = 0.55
7) PageRankPerplexity_G1.txt - BFS graph Perplexity with d = 0.85
8) PageRankPerplexity_G2.txt - DFS graph Perplexity with d = 0.85
9) InLinksSortG1.txt - BFS graph sorted by the in-links count
10) InLinksSortG2.txt - DFS graph sorted by the in-links count
11) PageRank2B_G1.txt - BFS graph for four iterations
12) PageRank2B_G2.txt - BFS graph for four iterations


## References:
* https://docs.python.org/2/library/string.html
* http://www.nltk.org/data.html#
* https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
* http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
* http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
* https://codereview.stackexchange.com/questions/156863/bfs-dfs-web-crawler
* https://github.com/gkatsev/pagerank
* https://github.com/permag/py-crawler/tree/master/pycrawler
* https://en.wikipedia.org/wiki/PageRank
* https://www.geeksforgeeks.org/page-rank-algorithm-implementation/









