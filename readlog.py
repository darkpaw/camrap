
# read the position log
# for use with ipython --pylab


# run readlog.py
# plot(xpoints)
# plot(ypoints)
# plot(xpoints, ypoints)


import csv
points = []


def loadlog():
	f = open("poslog.csv", 'rU')
	r = csv.reader(f)                                                                                              
	for idx, row in enumerate(r):
		if idx > 2:
			points.append(row)


loadlog()
print len(points)
xpoints = map(lambda pt: float(pt[0]), points)
ypoints = map(lambda pt: float(pt[1]), points)
