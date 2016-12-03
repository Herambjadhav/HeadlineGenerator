# HeadlineGenerator/POSTagger

taggerHG.py
Takes the input summarized text file and uses nltk package to identify Parts of speech. Uses Dependency graph extract main POS and root verb. Generates headlines along those words where the words are keywords in the text.

keywords.py
Takes an article and return the top n keywords based on frequency and excludes stopwords.

Run example:
python taggerHG.py summarize.txt 

where summarize.txt is the input summarized file.
generates a file called headline.txt

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

	<li>Main NP ambiguity
	<a href="http://stackoverflow.com/questions/5544475/does-an-algorithm-exist-to-help-detect-the-primary-topic-of-an-english-sentence">http://stackoverflow.com/questions/5544475/does-an-algorithm-exist-to-help-detect-the-primary-topic-of-an-english-sentence</a>
	</li>
	<li>Various grammar regex parsers
	<a href ="http://blog.quibb.org/2010/01/nltk-regular-expression-parser-regexpparser/">	http://blog.quibb.org/2010/01/nltk-regular-expression-parser-regexpparser/</a>



	
</ul>
