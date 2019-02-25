package index;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.search.BooleanClause.Occur;
import org.apache.lucene.search.BooleanQuery;

public class exact4 {
	public static void doSearch() throws Exception{
		Directory directory = FSDirectory.open(new File("/home/weixin/Downloads/TAGME-Reproducibility-master/20180320-link-index"));
		IndexReader indexReader = DirectoryReader.open(directory);
		IndexSearcher indexSearcher = new IndexSearcher(indexReader);  
		
		String pathname = "./Query.txt"; 
		File filename = new File(pathname); 
		InputStreamReader reader = new InputStreamReader(new FileInputStream(filename)); 
		BufferedReader br = new BufferedReader(reader);
		
		String filePath = "./Query_doc.txt";
		FileWriter fw = new FileWriter(filePath, false);  
		BufferedWriter bw = new BufferedWriter(fw);
		String line = "";  
		line = br.readLine(); 
		
		int count = 0;
		while (line != null) {
			String[] strs = line.split(" ");
			BooleanQuery query = new BooleanQuery();
			for (int j = 0; j < strs.length; j++) {
				if (strs[j].length() >0) {
					Query query1 = new TermQuery(new Term("contents",strs[j]));
					query.add(query1, Occur.SHOULD);
				}
			}
			Query query2 = new TermQuery(new Term("contents","refer"));
			query.add(query2, Occur.MUST_NOT);
			TopDocs topDocs = indexSearcher.search(query, 20);        		
			if (topDocs.totalHits >0) {
				count += 1;
	        	System.out.println(count);
	        	bw.write(line + '\t');
		        int doccounter = 0;
				for (ScoreDoc scoreDoc : topDocs.scoreDocs) {
			        Document document = indexSearcher.doc(scoreDoc.doc);
			        String s = document.get("contents");
		            if(s.length() < 100) {
		            	continue;
		            }
		            doccounter += 1;
		            s = s.replace('\n', ' ');
		            s = s.replace('\t', ' ');
		            bw.write(s.toLowerCase() + '\t');
		            if(doccounter == 10) break;                 
			    }   		
				bw.write('\n');
			}
			line = br.readLine(); 
		}
		indexReader.close();
		bw.close();  
		fw.close(); 
		}
	
	public static void main(String[] args) throws Exception {
		doSearch();
    }
}

