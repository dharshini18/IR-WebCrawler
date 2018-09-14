package HW4;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */

// Index Position - C:\Users\Dharshini\Desktop\Semester4\IR_HW4\IR_HW4\Index\
// Corpus Location - C:\Users\Dharshini\Desktop\Semester4\IR_HW4\IR_HW4\Corpus\

public class Task1 {

	private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	public static void main(String[] args) throws IOException {

		System.out.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String s = br.readLine();

		Task1 indexer = null;
		try {
			indexLocation = s;
			indexer = new Task1(s);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		// ===================================================
		// read input from user until he enters q for quit
		// ===================================================
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out.println(
						"Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
				System.out.println("[Acceptable file types: .xml, .html, .html, .txt]");
				s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}

				// try to add file into the index
				indexer.indexFileOrDirectory(s);
			} catch (Exception e) {
				System.out.println("Error indexing " + s + " : " + e.getMessage());
			}
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);

		s = "";
		int count = 0;
		while (!s.equalsIgnoreCase("q")) {
			try {
				count = count + 1;
				Map<Integer, String> query_words = indexer.populateQueryWords();
				int length = query_words.size();
				if (count > length) {
					System.out.println("The indexes are generated successfully in the location:" + indexLocation);
					break;
				}
				s = query_words.get(count);

				TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
				Query q = new QueryParser(Version.LUCENE_47, "contents", sAnalyzer).parse(s);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. display results
				System.out.println("Found " + hits.length + " hits.");
				for (int i = 0; i < hits.length; ++i) {
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);
					System.out.println((i + 1) + ". " + d.get("path") + " score=" + hits[i].score);
				}
				// 5. term stats --> watch out for which "version" of the term
				// must be checked here instead!
				Term termInstance = new Term("contents", s);
				long termFreq = reader.totalTermFreq(termInstance);
				long docCount = reader.docFreq(termInstance);
				System.out.println(s + " Term Frequency " + termFreq + " - Document Frequency " + docCount);

				// 6. Write the contents of the top 100 hits to a file
				// Format of table,
				// query_id Q0 doc_id rank BM25_score system_name
				indexer.writeContentToFile(searcher, s, count, hits);

			} catch (Exception e) {
				System.out.println(e);
				System.out.println("Error searching " + s + " : " + e.getMessage());
				break;
			}

		}

	}

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	Task1(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/*
	 * To write the contents/Output of the Lucene System. The top 100 hits are
	 * written to the file in the order - QueryID Q0 DocumentID LuceneScore
	 * SystemName, space separated
	 */
	public void writeContentToFile(IndexSearcher searcher, String query_word, int count, ScoreDoc[] hits)
			throws IOException {
		String queryId = Integer.toString(count);
		String filePath = "C:\\Users\\Dharshini\\Desktop\\Semester4\\IR_HW4\\IR_HW4\\Task1_Files\\";
		String filename = filePath + "Task1Query_" + queryId + ".txt";
		File file = new File(filename);
		if (file.createNewFile()) {
			FileWriter writer = new FileWriter(file);
			writer.write("QueryID Q0 DocumentID LuceneScore SystemName");
			writer.write("\n");
			writer.write("---------------------------------------------------");
			writer.write("\n");
			for (int i = 0; i < hits.length; i++) {
				int docId = hits[i].doc;
				Document d = searcher.doc(docId);
				String p = d.get("path");
				Path p_temp = Paths.get(p);
				String documentID = p_temp.getFileName().toString();
				String score = Float.toString(hits[i].score);
				writer.write(queryId + " " + "Q0" + " " + documentID + " " + score + " " + "ApacheLucene");
				writer.write("\n");
			}
			writer.close();
		}
	}

	/*
	 * To populate the Query Words for the search Engine in a HashMap for quick
	 * processing. If new words are to be added, add a new entry to the HashMap
	 * with the query ID
	 */
	public Map<Integer, String> populateQueryWords() {
		Map<Integer, String> query_words = new HashMap<Integer, String>();
		query_words.put(1, "dark eclipse moon");
		query_words.put(2, "forecast models");
		query_words.put(3, "total eclipse solar");
		query_words.put(4, "japan continental airline");
		query_words.put(5, "japan continental airlines");
		query_words.put(6, "solar eclipse fiction");
		query_words.put(7, "2017 solar eclipse");
		query_words.put(8, "total eclipse lyrics");
		query_words.put(9, "nordic marine animals");
		query_words.put(10, "volcanic eruptions tornadoes eruption tornado");
		return query_words;
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(), Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html") || filename.endsWith(".xml")
					|| filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}