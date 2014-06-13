from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/fairyteller/')
@app.route('/fairyteller/<name>')
def hello(name=None):
    return render_template('fairyteller.html', name=name)

@app.route('/do_something/', methods=['POST'])
def print_string():
    print request.json
    return ''

if __name__ == '__main__':
    app.run(debug=True)



