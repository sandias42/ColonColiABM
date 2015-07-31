import itertools

l = list(itertools.product(range(10),range(5)))
m = list(itertools.product(xrange(10),xrange(5)))+list(itertools.product(xrange(1),xrange(2)))
for i in itertools.islice(m, 49, None):
	if l[i[0]] == m[i[0]]:
		print("Match")
	else:
		print("No match")