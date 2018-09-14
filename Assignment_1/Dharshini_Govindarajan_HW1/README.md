# IR-Web-crawler (Spring - 2018)

## Files/Softwares to download
* Python - https://www.python.org/download/releases/2.7/
* NLTK Data - http://www.nltk.org/data.html
* NLTK - To use NLTK, "import nltk" and follow http://www.nltk.org/index.html thereafter
* BeautifulSoup - To download and import follow https://www.crummy.com/software/BeautifulSoup/
* Requests - http://docs.python-requests.org/en/master/user/install/#install
* PyCharm (Optional) - https://www.jetbrains.com/pycharm/

## Task1: Crawling the documents:

#### To Execute BFS, 
1) Navigate to the folder, containing the file (Task1.py)
   Eg -> C:\Documents\IR_WebCrawler\crawler
2) Type - python Task1.py seed "bfs" (In pythonScript/pycharm terminal/cmd)
   seed is the start URL without quotations - https://en.wikipedia.org/wiki/Solar_eclipse
3) The links visited are written to a file named CrawledLinks_bfs.txt in the same folder as the project

#### To Execute DFS, 
1) Navigate to the folder, containing the file (Task1.py)
   Eg -> C:\Documents\IR_WebCrawler\crawler
2) Type - python Task1.py seed "dfs" (In pythonScript/pycharm terminal/cmd)
   seed is the start URL without quotations - https://en.wikipedia.org/wiki/Solar_eclipse
3) The links visited are written to a file named CrawledLinks_dfs.txt in the same folder as the project

## Task2: Focused Crawling:

To Execute, 
1) Navigate to the folder, containing the file (Task2.py)
   Eg -> C:\Documents\IR_WebCrawler\crawler
2) Type - python Task2.py
   seed is the start URL without quotations - https://en.wikipedia.org/wiki/Solar_eclipse
   keywords is the set of words without quotations and seperated with comma - lunar,moon
3) The links visited are written to a file named CrawledLinks_focusedCrawling.txt in the same folder as the project

## References:
* https://docs.python.org/2/library/string.html
* http://www.nltk.org/data.html#
* https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
* http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
* http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
* https://codereview.stackexchange.com/questions/156863/bfs-dfs-web-crawler
* https://github.com/permag/py-crawler/tree/master/pycrawler









