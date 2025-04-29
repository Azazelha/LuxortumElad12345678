from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Привіт, Luxortum працює!'

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)