package HW4;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.stream.Stream;

public class Task2 {

	static String INDEXER_LOCATION = "C:\\Users\\Dharshini\\Desktop\\Semester4\\IR_HW4\\IR_HW4\\Indexer\\Unigram.txt";
	static String TABLES_LOCATIon = "C:\\Users\\Dharshini\\Desktop\\Semester4\\IR_HW4\\IR_HW4\\Tables_Task2\\";

	static double K1 = 1.2;
	static double K2 = (double) 100;
	static double b = 0.75;
	static double R = (double) 0; // Relevance is zero
	static double r = (double) 0;

	// Main Function
	public static void main(String args[]) throws IOException {
		List<String> file_lines = readFileContents(); // Read File contents
		// Format the file contents
		Map<String, Map<String, Integer>> frequency_map = split_file_contents(file_lines);
		int document_count = totalDocumentCount(frequency_map);
		Map<String, Integer> term_frequency = calculateTermFrequency(frequency_map);
		Map<Integer, String> query_words = populateQueryWords();
		Map<String, Integer> dl_values = findDlValues(frequency_map);
		double avdl = calculateAvdlValue(dl_values);

		/* Calculate the BM25 score for every query word */
		for (Integer key : query_words.keySet()) {
			Map<String, Integer> qf_values = findQueryWordsSplit(query_words.get(key));
			List<String> query_split_list = Arrays.asList(query_words.get(key).split(" "));
			Map<String, Double> document_score = calculateBM25_Score(qf_values, query_split_list, avdl, frequency_map,
					term_frequency, document_count, dl_values);
			Map<Integer, Map<String, Double>> BM25_values = new HashMap<Integer, Map<String, Double>>();
			BM25_values.put(key, document_score);
			for (Integer BM25_key : BM25_values.keySet()) {
				Map<String, Double> values = sortBM25DocumentsByScore(BM25_values, BM25_key);
				writeContentToFile(values, BM25_key);
			}
		}
	}

	/* To write the contents of the BM25 scores to appropriate files */
	private static void writeContentToFile(Map<String, Double> values, int BM25_key) throws IOException {
		String filePath = "C:\\Users\\Dharshini\\Desktop\\Semester4\\IR_HW4\\IR_HW4\\Task2_Files\\";
		String filename = filePath + "Task2Query_" + BM25_key + ".txt";
		File file = new File(filename);
		int count = 0;
		if (file.createNewFile()) {
			FileWriter writer = new FileWriter(file);
			writer.write("QueryID Q0 DocumentID Rank BM25Score SystemName");
			writer.write("\n");
			writer.write("---------------------------------------------------");
			writer.write("\n");
			for (String value : values.keySet()) {
				count = count + 1;
				String documentID = value;
				double score = values.get(value);
				String BM25_score = Double.toString(score);
				String rank = Integer.toString(count);
				String queryId = Integer.toString(BM25_key);
				writer.write(queryId + " " + "Q0" + " " + documentID + " " + rank + " " + BM25_score + " "
						+ "BM25RankingAlgorithm");
				writer.write("\n");
			}
			writer.close();
		}
	}

	/* To sort the documents in the decreasing order of their BM25 scores */
	private static <K, V extends Comparable<? super V>> Map<String, Double> sortBM25DocumentsByScore(
			Map<Integer, Map<String, Double>> bM25_values, Integer bM25_key) {
		Map<String, Double> documents = bM25_values.get(bM25_key);
		List<Entry<String, Double>> list = new ArrayList<>(documents.entrySet());
		list.sort(Entry.comparingByValue());
		Collections.reverse(list);

		Map<String, Double> result = new LinkedHashMap<>();
		for (Entry<String, Double> entry : list) {
			if (result.size() > 99) {
				break;
			} else {
				result.put(entry.getKey(), entry.getValue());
			}
		}
		return result;
	}

	/* To split the query words and find the qf value */
	private static Map<String, Integer> findQueryWordsSplit(String query) {
		List<String> query_split = Arrays.asList(query.split(" "));
		Map<String, Integer> count_query = new HashMap<String, Integer>();
		for (String querysplit : query_split) {
			if (count_query.containsKey(querysplit)) {
				int count = count_query.get(querysplit);
				count = count + 1;
				count_query.put(querysplit, count);
			} else {
				count_query.put(querysplit, 1);
			}
		}
		return count_query;
	}

	/* To calculate the dl and avdl value */
	private static double calculateAvdlValue(Map<String, Integer> dl_values) {
		double avdl = 0;
		for (Integer value : dl_values.values()) {
			avdl = avdl + value;
		}
		int length = dl_values.size();
		avdl = avdl / length;
		return avdl;
	}

	/* To calculate the document length for all the documents in the corpus */
	private static Map<String, Integer> findDlValues(Map<String, Map<String, Integer>> frequency_map) {
		Map<String, Integer> dl_values = new HashMap<String, Integer>();
		for (String key : frequency_map.keySet()) {
			Map<String, Integer> values = frequency_map.get(key);
			for (String doc_key : values.keySet()) {
				int frequency = values.get(doc_key);
				if (dl_values.containsKey(doc_key)) {
					int count = dl_values.get(doc_key);
					count = count + frequency;
					dl_values.put(doc_key, count);
				} else {
					dl_values.put(doc_key, frequency);
				}
			}
		}
		return dl_values;
	}

	/* To populate the query words to a map, to make processing easier */
	private static Map<Integer, String> populateQueryWords() {
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

	/* To calculate the total number of documents in the index */
	private static int totalDocumentCount(Map<String, Map<String, Integer>> frequency) {
		Set<String> documents_set = new HashSet<String>();
		for (String key : frequency.keySet()) {
			Map<String, Integer> documents = frequency.get(key);
			for (String document_name : documents.keySet()) {
				documents_set.add(document_name);
			}
		}
		return documents_set.size();
	}

	/*
	 * To split the contents of the Unigram Index and form an appropriate data
	 * structure
	 */
	private static Map<String, Map<String, Integer>> split_file_contents(List<String> file_lines) {
		Map<String, Map<String, Integer>> term_frequency = new HashMap<String, Map<String, Integer>>();

		for (String line : file_lines) {
			int count = -1;
			Map<String, Integer> document_frequency = new HashMap<String, Integer>();
			int index = line.indexOf(" ");
			String word = line.substring(0, index);
			String rest_of_line = line.substring(index + 1, line.length());
			List<String> documents = Arrays.asList(rest_of_line.split(" "));
			List<String> documents_temp = new ArrayList<String>();
			for (String document : documents) {
				document = document.replace("[", "").replace("]", "");
				documents_temp.add(document);
			}

			documents = new ArrayList<String>();
			for (String value : documents_temp) {
				value = value.replaceAll("'", "");
				if (value.contains(".txt")) {
					int index_txt = value.indexOf(".txt");
					String text = ".txt";
					value = value.substring(0, index_txt + text.length());
				}
				documents.add(value.trim());
			}

			for (int i = 0; i < documents.size(); i += 2) {
				if (count != documents.size()) {
					count = count + 2;
					String document_name = documents.get(i);
					String frequency = documents.get(count);
					int occurance = Integer.parseInt(frequency);
					document_frequency.put(document_name, occurance);
				}
			}
			term_frequency.put(word, document_frequency);
		}
		return term_frequency;
	}

	/* To read the contents of the Unigram Index */
	private static List<String> readFileContents() throws IOException {
		List<String> lines = new ArrayList<String>();
		try (BufferedReader r = Files.newBufferedReader(Paths.get(INDEXER_LOCATION), StandardCharsets.UTF_8)) {
			Stream<String> stream = r.lines();
			stream.forEach(line -> lines.add(line));
		}
		return lines;
	}

	/*
	 * To calculate the BM25 score for every document with respect to the query
	 */
	private static Map<String, Double> calculateBM25_Score(Map<String, Integer> qf_values,
			List<String> query_split_list, double avdl, Map<String, Map<String, Integer>> frequency_map,
			Map<String, Integer> term_frequency, int document_count, Map<String, Integer> dl_values) {
		Map<String, Double> BM25_values = new HashMap<String, Double>();
		for (String key_doc : dl_values.keySet()) {
			List<Double> total_values = new ArrayList<Double>();
			double N = dl_values.size();
			double dl = dl_values.get(key_doc);
			double K = calculateKValue(dl, avdl);
			double first_num = (r + 0.5) / (R - r + 0.5);
			double f = 0;
			double n = 0;
			for (String query : query_split_list) {
				if (frequency_map.containsKey(query)) {
					n = frequency_map.get(query).size();
					Map<String, Integer> value = frequency_map.get(query);
					if (value.containsKey(key_doc)) {
						f = value.get(key_doc);
					}
				}
				double qf = qf_values.get(query);
				double first_den = (n - r + 0.5) / (N - n - R + r + 0.5);
				double first = first_num / first_den;
				double second = ((K1 + 1) * f) / (K + f);
				double third = ((K2 + 1) * qf) / (K2 + qf);
				double log_value = Math.log(first);
				double total_value = log_value * second * third;
				total_values.add(total_value);
			}
			double BM25 = calculateTotalScore(total_values);
			BM25_values.put(key_doc, BM25);
		}
		return BM25_values;
	}

	/* To calculate the cumulative BM25 score */
	private static double calculateTotalScore(List<Double> total_values) {
		double temp = 0;
		for (Double value : total_values) {
			temp = temp + value;
		}
		return temp;
	}

	/* To calculate the 'K' value - empirical */
	private static double calculateKValue(double dl, double avdl) {
		return K1 * ((1 - b) + (b * (dl / avdl)));
	}

	/* To calculate the term frequency for every term in the Unigram Index */
	private static Map<String, Integer> calculateTermFrequency(Map<String, Map<String, Integer>> frequency_map) {
		Map<String, Integer> term_frequency = new HashMap<String, Integer>();
		for (String key : frequency_map.keySet()) {
			int count = 0;
			Map<String, Integer> documents = frequency_map.get(key);
			Collection<Integer> integer_values = documents.values();
			for (Integer value : integer_values) {
				count = count + value;
			}
			term_frequency.put(key, count);
		}
		return term_frequency;
	}
}
