import logging

def main():
	fname = "/home/angelo/Downloads/post"
	f = open(fname, "r")
	[dupCount, count] = duplicateCount(f)
	f.close()
	print "dupcount " + str(dupCount)
	f = open(fname, "r")
	#dupCount = f.close()
	[hm, table] = pushMap(f,count)
	uniqueCount = processTable(hm,table)
	print "uniqcount " + str(uniqueCount)
	print "total " + str(dupCount + uniqueCount)
	f.close()
	
def processTable(h,t):
	#h: hashtable with
	#("F/L " + first/last 5 words, [idx1,idx2 ...])
	#where t[idxN] = #occurences + " " + corresponding sentence in this key
	dblCount = 0
	normalCount = 0
	lenh = len(h)
	itr = 0
	for key, values in h.iteritems():
		#print key, values
		for i in range(0,len(values)-1):
			cand1 = t[values[i]].split(' ')
			cand1[-1] = cand1[-1].rstrip() #kill newline
			for j in range(i+1,len(values)):
				#key is F + first 5 words or
				#       L + last 5 words
				#value is lookup index for t
				#t[value] is the "count + sentence"
				cand2 = t[values[j]].split(' ')
				cand2[-1] = cand2[-1].rstrip() #kill newline
				interactions = int(cand1[0])*int(cand2[0])
				candidate = abs(len(cand1[1:]) - len(cand2[1:])) < 2
				# strip newline
				
				# if cand1[1:6]!=cand2[1:6] and key[0]=="F":
				# 	logging.error('fwrong')
				# if cand1[-5:]!=cand2[-5:] and key[0]=="L":
				# 	logging.error('Lwrong')
				# if cand1==cand2:
				# 	logging.error('cannot dup')
				
				if candidate:
					goodDist = closeEnough(cand1[1:], cand2[1:])
					if goodDist:
						#print "i,j: " + str(values[i]) + " " + str(values[j])
						if checkOtherSide(key[0], cand1[1:], cand2[1:]):
							dblCount+=interactions
						else:
							normalCount+=interactions
		itr+=1
		if itr % 100000 == 0:
			print str(itr) + " of " + str(lenh)
			print normalCount + dblCount/2
	return normalCount + dblCount/2

def closeEnough(sent1, sent2):
	# if len(sent1) - len(sent2) > 1:
	# 	logging.error('too high')
	# if len(sent2) - len(sent1) > 1:
	# 	logging.error('too high')
	s1 = sent1
	s2 = sent2
	p1 = 0
	p2 = 0
	s1shorter = len(s1) < len(s2)
	samelength = len(s1) == len(s2)
	L = len(s1) if len(s1) > len(s2) else len(s2)
	d = 0
	for i in range(L):
		#length delta 1
		if	((p1 == len(s1)) and (p2 == len(s2) - 1)) or \
		    ((p2 == len(s2)) and (p1 == len(s1) - 1)):
			d+=1
			continue
		#check for equality
		if s1[p1]==s2[p2]:
			p1+=1
			p2+=1
		else:
			d+=1 #difference detected
			if samelength:
				p1+=1
				p2+=1
			else:
				if s1shorter:
					p2+=1
				else:
					p1+=1
		if d > 1:
			return False

	return False if d > 1 else True

def checkOtherSide(side, sent1, sent2):
	#side is front or last
	#sent1,sent2 is sentence in list form
	#print side
	if (side=="F"):
		#check end
		return (sent1[-5:] == sent2[-5:])
	else:
		#check beginning
		return (sent1[0:5] == sent2[0:5])

def pushMap(f,cnt):
	hm = dict()
	table = [""]*cnt
	count = 0
	for l in f:
		line = l.lstrip()
		linesplit = line.split(' ')
		num = linesplit[0] #num occurences
		line = linesplit[1:] #sentence in array form
		#cannot store 6 keys of form:
		#F + len + sentence
		#F + len-1 + sentence
		#F + len+1 + sentence
		#L + len + sentence
		#L + len-1 + sentence
		#L + len+1 + sentence
		#because there is not enough RAM in this shitty computer, instead settle for
		#F + sentence
		#L + sentence
		#determining length in processing

		#("F " + sentence), ("L " + sentence)
		firstFive = "F " + " ".join(findFirstFive(line))
		lastFive  = "L " + " ".join(findLastFive(line))
		
		#("num occurences " + sentence)
		table[count] = str(num) + " " + " ".join(line)
		if firstFive in hm:
			hm[firstFive].append(count)
		else:
			hm[firstFive] = [count]

		if lastFive in hm:
			hm[lastFive].append(count)
		else:
			hm[lastFive] = [count]
		# print count
		# print table[count]
		# print firstFive
		# print lastFive
		# print hm[firstFive]
		# print hm[lastFive]
		# print '----'
		# if table[hm[firstFive][-1]].split(' ')[1:6] != firstFive.split(' ')[1:6]:
		# 	logging.error('table first 5 words not the same')
		# if table[hm[lastFive][-1]].split(' ')[-5:] != lastFive.split(' ')[1:6]:
		# 	print table[hm[lastFive][-1]].split(' ')[-5:]
		# 	print lastFive.split(' ')[1:6]
		# 	logging.error('table last 5 words not the same')
		
		if (count % 100000) == 0:
			print count
		count+=1
	return [hm, table]

def duplicateCount(f):
	total = 0
	count = 0;
	for line in f:
		num = int(line.lstrip().split(' ')[0])
		total += (num-1)*num/2
		count+=1
	return [total, count]

def findFirstFive(l):
	return l[0:5]

def findLastFive(l):
	return l[-5:]

  
if __name__ == "__main__":
	main()
