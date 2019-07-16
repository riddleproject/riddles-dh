"""
	* Jury is out on the best way to do this. Hard to asses whether extra steps for 
	poem similarity is necessary. Simplest thing to do is a windowed approach for 
	text similarity. Kulback Libler divergence. (KLB divergence). Measures how much 
	information is lost when you approximate one probability distribution by another.
	Divergence score. Probability distributions are observed word frequencies in a corpus. 
	Set A is all documents from a 10 year period, represented as a list of words & their 
	frequencies. Normalize by the length of the documents. Do that for the next 10 year window. 
	Two distributions that can be compared. From 1900 to 1905, how much information is lost 
	when I approximate that to 1905 to 1910. Slide forward taking 5 year windows, which can 
	show that things are the same or changing. Question of the significance of change is a new 
	problem. 1901 to 1906 compared to 1907 to 1911. Gives an estimate of when the period of change 
	occurred. Once you find that peak point of change, use the vocabulary test to find what 
	is distinctive of that set.

	* Simplest measure of complexity: Vocabulary richness. Word length. Sentence length. Use a 
	package in r called "koRpus:" suite of reading difficulty measures. Plenty of  formulas that 
	condition on word length, syllable length/count, sentence length. Flesh reading ease. Used to
	study the difficulty. Small data problem, should wash out. If you have more things, the 
	differences could be more or less. Language will pile in and get less disjointed. Differences 
	between any two texts is large, but between all texts is small.

"""

