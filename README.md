Same problem: 

Your task is to quickly find the number of pairs of sentences that are at the word-
level edit distance at most 1. Two sentences S1 and S2 they are at edit distance 1 if S1 can be transformed to S2 by: adding, removing or substituting a single word.

For example, consider the following sentences where each letter represents a word: • S1: A B C D • S2: A B X D • S3: A B C • S4: A B X C Then pairs the following pairs of sentences are at word edit distance 1 or less: (S1, S2), (S1, S3), (S2, S4), (S3, S4).

The input data has 9,397,023 sentences, each one divided by a new line and with the sentence id at the beginning of the line. The zip compressed file size is around 500MB and it's located here. All sentences in the input data are at least 10 words long. A straightforward LSH approach like the one taught in class for jaccard similarity can be used to solve this problem, however it may not necessarily be the faster approach.

Solution:..
    Tried to use Java but to no avail since using HashMap<String,Integer> is too big and cannot store whole dataset (kept running into garbage collector overhead).  So had to cheat and fuck with sentences.txt (originally huge ass motherfucking file):..
	```
	    cut -d' ' -f2- sentences.txt | sort | uniq -c > post
	```..
    But this postprocessed file STILL wouldn't fit into Java (roughly 50% of it was finished before it farted). Using Python instead, this was easily done. So I just made keys in the following form: