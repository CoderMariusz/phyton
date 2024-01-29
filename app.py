from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():

    JSON = {'h': 'Hello World'}
    return JSON

if __name__ == '__main__':
    app.run(debug=True)
