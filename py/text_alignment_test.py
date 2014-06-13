
import numpy as np
from scipy import stats
from OSCSender import OSCSender
import time
# import matplotlib.pyplot as plt

def dp(M):
	r = len(M)
	c = len(M[0])

	D = np.zeros([r+1,c+1])

	D[0] = 1e6
	D[:,0] = 1e6
	D[0,0] = 0
	# print 'init', D
	D[1:r+1, 1:c+1] = M

	phi = np.zeros([r,c])

	for i in xrange(0,r):
		for j in xrange(0,c):
			dmax = min ([D[i, j], D[i, j+1], D[i+1, j]])
			tb = np.argmin ([D[i, j], D[i, j+1], D[i+1, j]]) + 1
			D[i+1,j+1] = D[i+1,j+1]+dmax
			phi[i,j] = tb

	i = r - 1
	j = c - 1
	p = [i]
	q = [j]

	while i > 0 and j > 0:
		tb = phi[i,j]
		if tb == 1:
			i = i-1
			j = j-1
		elif tb ==2:
			i = i-1
		elif tb ==3:
			j = j-1
		else:
			foo = 1
			# error??

		p.insert(0,i)
		q.insert(0,j)

	D = D[2:(r+1),2:(c+1)];

	return p,q,D

def lev_distance(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)] / (( len(str1)+len(str2) ) / 2)


def aw_dtw(true_text_words_full, spoken_text_words, predLength):
	# predLength = 5
	# fid = open('../data/text/three_little_pigs.txt', 'r');
	# true_text = fid.read()
	# fid.close()

	# fid = open('../data/text/imanol_test.txt', 'r');
	# spoken_text = fid.read()
	# fid.close()

	start_time = time.time()
	# your code

	true_text_words = true_text_words_full[:len(spoken_text_words)+predLength]
	distance_matrix = np.zeros([len(true_text_words), len(spoken_text_words)])

	for i in xrange(0,len(true_text_words)):
		for j in xrange(0,len(spoken_text_words)):
			distance_matrix[i,j] = lev_distance(true_text_words[i], spoken_text_words[j])


	# print 'dm', distance_matrix
	[p,q,D] = dp(distance_matrix)
	# print 'D', D
	# print p,q

	slope, intercept, foo, bar, bla = stats.linregress(np.array(q),np.array(p))

	# q_future = np.zeros(len(q)+predLength)
	q_future = slope * (np.array(range(len(q) + predLength))+1) + intercept

	# print p, q, q_future

	# plt.imshow(distance_matrix)
	# plt.plot(q,p)
	# plt.plot(np.array(range(len(q) + predLength))+1, q_future)
	# plt.show()

	print 'elapsed ', time.time() - start_time, ' for ', len(spoken_text_words)

	if len(q)-len(p) <= predLength:
		return q[len(q)-1]
	else:
		return q_future[len(q_future)-1]

	# print q_future




		# plt.imshow(distance_matrix)
		# plt.plot(q,p)
		# plt.show()
		# print p,q
		# plt.plot(p,q)


fid = open('../data/text/three_little_pigs.txt', 'r');
true_text = fid.read()
fid.close()
true_text_words = true_text.split()

fid = open('../data/text/imanol_test.txt', 'r');
spoken_text = fid.read()
fid.close()

sender = OSCSender('localhost', 7001)

predLength = 10

# =)
jarcodedFileNames = [25,42,57,72,82,98,110,117,160,172,187,200,219,226]
jarcodedFileNames = np.array(jarcodedFileNames)
# for i in xrange(1,20):

i = 1
while i*5 < len(true_text_words):
	inputlength = i * 5
	spoken_text_words = spoken_text.split()[:inputlength]
	next_q = aw_dtw(true_text_words, spoken_text_words, predLength)

	if next_q >= jarcodedFileNames[0]:
		audiotoplay = jarcodedFileNames[jarcodedFileNames < next_q][len(jarcodedFileNames[jarcodedFileNames < next_q])-1]
		jarcodedFileNames = jarcodedFileNames[jarcodedFileNames > next_q]
		sender.defineMessage("/audio", '../data/audio/' + str(audiotoplay)+'.mp3')
		sender.sendMessages()
	i = i+1
