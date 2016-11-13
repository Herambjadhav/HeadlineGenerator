# HeadlineGenerator/POSTagger

taggerHG.py
Takes the input summarized text file and uses nltk package to identify Parts of speech.

keywords.py
Takes an article and return the top n keywords based on frequency and excludes stopwords.

Run:
python taggerHG.py sum_test1.txt 

where sum_tese1.txt is the input summarized file.


References:
<ul>

	
	<li>Summarization test tool
		<a href="http://autosummarizer.com/index.php">http://autosummarizer.com/index.php</a>
	</li>
	
	<li>Part of speech test tool
		<a href="http://parts-of-speech.info/">http://parts-of-speech.info/</a>
	</li>

	<li>Part of speech labels
		<a href="https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html">https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html</a>
	</li>

	<li>Chunking
		<a href="https://www.eecis.udel.edu/~trnka/CISC889-11S/lectures/dongqing-chunking.pdf">https://www.eecis.udel.edu/~trnka/CISC889-11S/lectures/dongqing-chunking.pdf</a>
	</li>

	<li>POS and Chunking using NLTK
		<a href="http://www.nltk.org/book/ch07.html">http://www.nltk.org/book/ch07.html</a>
	</li>

	NP main ambiguity
	http://stackoverflow.com/questions/5544475/does-an-algorithm-exist-to-help-detect-the-primary-topic-of-an-english-sentenc

	Various grammar regex parsers
	http://blog.quibb.org/2010/01/nltk-regular-expression-parser-regexpparser/
	
</ul>