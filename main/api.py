from flask import Flask, request, jsonify

app = Flask(__name__)
data_store = []  # Almacén para guardar los datos enviados

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json.get('data')
    if data:
        data_store.append(data)
        return jsonify({'message': 'Data received', 'data': data}), 200
    else:
        return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
