from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '欢迎来到我的网站！'

if __name__ == '__main__':
    app.run(port=5174)