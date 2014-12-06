Same problem: 

Your task is to quickly find the number of pairs of sentences that are at the word-
level edit distance at most 1. Two sentences S1 and S2 they are at edit distance 1 if S1 can be transformed to S2 by: adding, removing or substituting a single word.

For example, consider the following sentences where each letter represents a word: • S1: A B C D • S2: A B X D • S3: A B C • S4: A B X C Then pairs the following pairs of sentences are at word edit distance 1 or less: (S1, S2), (S1, S3), (S2, S4), (S3, S4).

The input data has 9,397,023 sentences, each one divided by a new line and with the sentence id at the beginning of the line. The zip compressed file size is around 500MB and it's located here. All sentences in the input data are at least 10 words long. A straightforward LSH approach like the one taught in class for jaccard similarity can be used to solve this problem, however it may not necessarily be the faster approach.

Solution:  
  Tried to use Java but to no avail since using HashMap\<String,ArrayList\<Integer\>\> is too big and cannot store whole dataset (kept running into garbage collector overhead).  So had to cheat and fuck with sentences.txt (originally huge ass motherfucking file):  

  ```
  cut -d' ' -f2- sentences.txt | sort | uniq -c > post
  ```  

  But this postprocessed file STILL wouldn't fit into Java (roughly 50% of it was finished before it farted). So I used Python instead.  This is nice because the post file naturally is a key, value pair of the following form:  

  > (key,value) -> (#occurences, sentence)  

  Python on the other hand, was able to easily accomodate this file when I used a hashtable of the form:  

  > (key0,value0) -> (first 5 words, length + sentence)  
  > (key1,value1) -> (last 5 words, length + sentence)  

  I wasn't able to fit ideally all these keys in though, since I run out of memory in Python when I do this:  

  > (key0,value0) -> (first 5 words + len(sentence), sentence)  
  > (key1,value1) -> (first 5 words + len(sentence)-1, sentence)  
  > (key2,value2) -> (first 5 words + len(sentence)+1, sentence)  
  > (key3,value3) -> (last 5 words + len(sentence), sentence)  
  > (key4,value4) -> (last 5 words + len(sentence)-1, sentence)  
  > (key5,value5) -> (last 5 words + len(sentence)+1, sentence)  

  But it turns out that doesn't really matter becauase candidates of word difference of length 1 seems to be not too common so the 3X memory overhead might not be worth it anyway because we might not do 3X the calculation if we don't.  Now timing this shit we get:  

  ```
  time cut -d' ' -f2- sentences.txt | sort | uniq -c > blah
  real	0m29.445s
  user	0m21.072s
  sys	0m4.224s
  time python sent.py 
  dupcount 426873920
  0
  100000
  200000
  300000
  400000
  500000
  600000
  700000
  800000
  900000
  1000000
  1100000
  1200000
  1300000
  1400000
  1500000
  1600000
  1700000
  1800000
  1900000
  2000000
  2100000
  2200000
  2300000
  2400000
  2500000
  2600000
  2700000
  2800000
  2900000
  3000000
  3100000
  3200000
  3300000
  3400000
  3500000
  3600000
  3700000
  3800000
  3900000
  4000000
  4100000
  4200000
  4300000
  4400000
  4500000
  4600000
  4700000
  4800000
  4900000
  100000 of 8760257
  28040
  200000 of 8760257
  47823
  300000 of 8760257
  65407
  400000 of 8760257
  95570
  500000 of 8760257
  145115
  600000 of 8760257
  168397
  700000 of 8760257
  193268
  800000 of 8760257
  206886
  900000 of 8760257
  234898
  1000000 of 8760257
  255622
  1100000 of 8760257
  279110
  1200000 of 8760257
  292717
  1300000 of 8760257
  319495
  1400000 of 8760257
  342831
  1500000 of 8760257
  375200
  1600000 of 8760257
  420858
  1700000 of 8760257
  443893
  1800000 of 8760257
  463295
  1900000 of 8760257
  485010
  2000000 of 8760257
  524519
  2100000 of 8760257
  542224
  2200000 of 8760257
  566411
  2300000 of 8760257
  590140
  2400000 of 8760257
  623584
  2500000 of 8760257
  641066
  2600000 of 8760257
  661043
  2700000 of 8760257
  682005
  2800000 of 8760257
  712653
  2900000 of 8760257
  764240
  3000000 of 8760257
  778969
  3100000 of 8760257
  810058
  3200000 of 8760257
  841268
  3300000 of 8760257
  856163
  3400000 of 8760257
  874848
  3500000 of 8760257
  903247
  3600000 of 8760257
  927595
  3700000 of 8760257
  943796
  3800000 of 8760257
  974198
  3900000 of 8760257
  995232
  4000000 of 8760257
  1030832
  4100000 of 8760257
  1043596
  4200000 of 8760257
  1063386
  4300000 of 8760257
  1114481
  4400000 of 8760257
  1146079
  4500000 of 8760257
  1164857
  4600000 of 8760257
  1210258
  4700000 of 8760257
  1320604
  4800000 of 8760257
  1340757
  4900000 of 8760257
  1377940
  5000000 of 8760257
  1400441
  5100000 of 8760257
  1433647
  5200000 of 8760257
  1461384
  5300000 of 8760257
  1479838
  5400000 of 8760257
  1585252
  5500000 of 8760257
  1621039
  5600000 of 8760257
  1657095
  5700000 of 8760257
  1676752
  5800000 of 8760257
  1694253
  5900000 of 8760257
  1744936
  6000000 of 8760257
  1777772
  6100000 of 8760257
  1818957
  6200000 of 8760257
  1848721
  6300000 of 8760257
  1892812
  6400000 of 8760257
  1997802
  6500000 of 8760257
  2022604
  6600000 of 8760257
  2065023
  6700000 of 8760257
  2082792
  6800000 of 8760257
  2100635
  6900000 of 8760257
  2119309
  7000000 of 8760257
  2153008
  7100000 of 8760257
  2174184
  7200000 of 8760257
  2214521
  7300000 of 8760257
  2239638
  7400000 of 8760257
  2258092
  7500000 of 8760257
  2327849
  7600000 of 8760257
  2356109
  7700000 of 8760257
  2375250
  7800000 of 8760257
  2420564
  7900000 of 8760257
  2451222
  8000000 of 8760257
  2464696
  8100000 of 8760257
  2485650
  8200000 of 8760257
  2500550
  8300000 of 8760257
  2518316
  8400000 of 8760257
  2533962
  8500000 of 8760257
  2555189
  8600000 of 8760257
  2582686
  8700000 of 8760257
  2600872
  uniqcount 2620033
  total 429493953
  
  real	1m35.945s
  user	1m34.688s
  sys	0m1.124s
  ```  

  So the total algorithm takes about 2 minutes.  Not too shabby.