from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def root():
    return redirect('/api/data')

@app.route('/api/data')
def home():
    return "DevOps Pipeline Working Successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)