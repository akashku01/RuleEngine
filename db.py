import sqlite3
import json

# Connect to SQLite database (or create it if it doesn't exist)
def connect_db():
    return sqlite3.connect('rule_engine.db')

# Initialize tables in the database
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create the rules table
    cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY,
                        rule_string TEXT,
                        ast BLOB
                    )''')

    # Create the attributes table
    cursor.execute('''CREATE TABLE IF NOT EXISTS attributes (
                        id INTEGER PRIMARY KEY,
                        attribute_name TEXT,
                        data_type TEXT
                    )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Save a new rule to the database
def save_rule(rule_string, ast):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Serialize AST as JSON string
    serialized_ast = json.dumps(ast, default=str)  # Convert AST to string representation
    cursor.execute('''INSERT INTO rules (rule_string, ast) 
                      VALUES (?, ?)''', (rule_string, serialized_ast))
    
    conn.commit()
    conn.close()

# Retrieve a rule by its ID
def get_rule(rule_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT rule_string, ast FROM rules WHERE id = ?''', (rule_id,))
    rule = cursor.fetchone()
    
    conn.close()
    if rule:
        # Deserialize AST from JSON
        return rule[0], json.loads(rule[1])
    return None, None

# Save attribute metadata to the database
def save_attribute(attribute_name, data_type):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO attributes (attribute_name, data_type) 
                      VALUES (?, ?)''', (attribute_name, data_type))
    
    conn.commit()
    conn.close()

# Example usage
if __name__ == '__main__':
    init_db()
    # Example of saving a rule and an attribute
    save_attribute("age", "integer")
    save_attribute("department", "string")
    
    example_rule = "age > 30 AND department = 'Sales'"
    example_ast = {'type': 'operator', 'value': 'AND', 'left': {'type': 'operand', 'value': ('age', '>', 30)}, 'right': {'type': 'operand', 'value': ('department', '=', 'Sales')}}
    save_rule(example_rule, example_ast)
