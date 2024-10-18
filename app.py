from flask import Flask, jsonify, request
from flask_cors import CORS  # For handling CORS
import json



app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend to communicate with the backend

# Dummy database for storing rules
rules_db = [
    {"id": 1, "rule_string": "age > 30 AND department = 'Sales'", "ast": '{"type": "operator", "value": "AND", "left": {"type": "operand", "value": ["age", ">", 30]}, "right": {"type": "operand", "value": ["department", "=", "Sales"]]}'}
]

# Endpoint to get all rules
@app.route('/api/rules', methods=['GET'])
def get_rules():
    return jsonify(rules_db)

# Endpoint to save a new rule
@app.route('/api/rules', methods=['POST'])
def save_rule():
    data = request.get_json()
    new_rule = {
        "id": len(rules_db) + 1,
        "rule_string": data['rule_string'],
        "ast": json.dumps(data['ast'])  # Serialize AST into JSON string
    }
    rules_db.append(new_rule)
    return jsonify(new_rule), 201

# Endpoint to evaluate rule (dummy example)
@app.route('/api/rules/evaluate', methods=['POST'])
def evaluate_rule():
    data = request.get_json()
    # Simulating evaluation by returning a success message
    return jsonify({"message": "Rule evaluated successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
