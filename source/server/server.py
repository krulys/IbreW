from flask import Flask

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
   app.run("localhost",port=8081,debug=True)