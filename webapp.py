from ctypes.wintypes import WORD
import time
from urllib import response
from flask import Flask, redirect, url_for, request, render_template
from lazydict import LazyDict
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', word="", ld={})


@app.route('/search', methods=['POST'])
def login():
    if request.method == 'POST':
        word = request.form['word'].strip().split(';')[0:10]
        word.sort()
        ld = []
        st = time.time()
        c = 0
        for w in word:
            t = time.time()
            ld.append(LazyDict(w).fetchAll(2))
            c += 1
            # time.sleep(2)
            print("Fetched {0}/{1} | Time left: {2:.2f}s".format(c,
                                                                 len(word), (time.time()-t) * (len(word) - c)))
        print(f"Took {time.time() - st}s to get {len(word)} word meaning")
        return render_template('index.html', word=word, ld=ld, items=range(len(word)))


if __name__ == '__main__':
    app.run(debug=True)
