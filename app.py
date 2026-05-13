from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello from Flask App! - Version2', 'status': 'success'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Run on all interfaces (0.0.0.0) so it's accessible from outside container
    app.run(host='0.0.0.0', port=5000, debug=False)
