from flask import Flask
from flask import request
from flask import render_template


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


import numpy as np
from scipy import stats
from OSCSender import OSCSender
import time
# import matplotlib.pyplot as plt


true_text_words = ""
sender = OSCSender('localhost', 7001)
jarcodedFileNames = [25,42,57,72,82,98,110,117,160,172,187,200,219,226]
jarcodedFileNames = np.array(jarcodedFileNames)

def initialize():

    fid = open('../data/text/sonar_knights.txt', 'r');
    global true_text_words    # Needed to modify global copy of globvar
    true_text = fid.read()
    fid.close()
    true_text_words = true_text.split()

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


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/fairyteller/')
def fairytellerFunction():
    return render_template('fairyteller.html')

@app.route('/receive_string/', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def print_string():
    print request.data
    global true_text_words
    global sender
    global jarcodedFileNames
    predLength = 10
    next_q = aw_dtw(true_text_words, request.data, predLength)

    if next_q >= jarcodedFileNames[0]:
        audiotoplay = jarcodedFileNames[jarcodedFileNames < next_q][len(jarcodedFileNames[jarcodedFileNames < next_q])-1]
        jarcodedFileNames = jarcodedFileNames[jarcodedFileNames > next_q]
        sender.defineMessage("/audio", '../data/audio/' + str(audiotoplay)+'.mp3')
        sender.sendMessages()

    return ''

if __name__ == '__main__':
    initialize()
    app.run(debug=True, port=5000)





