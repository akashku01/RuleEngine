import json
import re
import sqlite3


class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # "operator" or "operand"
        self.left = left  # Left child node
        self.right = right  # Right child node (only for operators)
        self.value = value  # Value for operand nodes

    # Method to serialize a Node object into a dictionary
    def to_dict(self):
        return {
            'type': self.type,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
            'value': self.value  # This will preserve the tuple or list structure as is
        }

    
    @staticmethod
    def from_dict(dct):
        left = Node.from_dict(dct['left']) if dct.get('left') else None
        right = Node.from_dict(dct['right']) if dct.get('right') else None

        
        value = dct['value']
        if isinstance(value, list) and len(value) == 3:
           
            value = tuple(value)
        elif isinstance(value, str) and value.startswith("'") and value.endswith("'"):
            value = value[1:-1] 

        return Node(dct['type'], left, right, value)

def connect_db():
    return sqlite3.connect("rule_engine.db")


# Function to create a rule AST from a rule string
def create_rule(rule_string):
    rule_string = rule_string.replace("(", "").replace(")", "")  # Remove parentheses
    if "AND" in rule_string:
        operator = "AND"
        left_str, right_str = rule_string.split("AND")
    elif "OR" in rule_string:
        operator = "OR"
        left_str, right_str = rule_string.split("OR")
    else:
        raise ValueError("Invalid operator in rule string")

    # Parse the left and right conditions (e.g., "age > 30")
    left_operand = parse_condition(left_str.strip())
    right_operand = parse_condition(right_str.strip())

    # Return the AST
    return Node(type="operator", value=operator, left=left_operand, right=right_operand)


# Function to parse individual conditions (e.g., "age > 30")
def parse_condition(condition_str):
    # Strip leading and trailing spaces
    condition_str = condition_str.strip()

    # Handle string literals by stripping extra quotes
    if condition_str.startswith("'") and condition_str.endswith("'"):
        condition_str = condition_str[1:-1]  # Remove quotes around string literals

    match = re.match(r"(\w+)\s*(>=|<=|>|<|==|=)\s*(\S+)", condition_str)
    if match:
        attribute = match.group(1)
        operator = match.group(2)
        value = match.group(3)

        # Ensure that string values are treated correctly (strip quotes if necessary)
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]  # Remove surrounding quotes if it's a string literal
        elif value.isdigit():
            value = int(value)
        
        return Node(type="operand", value=(attribute, operator, value))
    else:
        raise ValueError(f"Invalid condition: {condition_str}")


def combine_rules(rules):
    if not rules:
        return None

    # Start by creating the first rule's AST
    combined_ast = create_rule(rules[0])

    # Combine with subsequent rules using "AND" as a default operator
    for rule in rules[1:]:
        next_ast = create_rule(rule)
        combined_ast = Node(type="operator", value="AND", left=combined_ast, right=next_ast)

    return combined_ast


# Function to evaluate the rule AST against the provided data
def evaluate_rule(ast, data):
    if ast.type == "operand":
        attribute, operator, value = ast.value

        if isinstance(value, str):
            value = value.strip("'")  # Remove any extra quotes from string literals
        if isinstance(data[attribute], str):
            data_value = data[attribute].strip("'")  # Remove any quotes around string literals
        else:
            data_value = data[attribute]

        if operator == ">":
            return data_value > value
        elif operator == "<":
            return data_value < value
        elif operator == "==":
            return data_value == value
        elif operator == "=":
            return data_value == value
        return False
    elif ast.type == "operator":
        # Recursively evaluate the left and right parts of the AST
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)

        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result
        return False


# Function to save a rule into the database
def save_rule(rule_string, ast):
    conn = connect_db()
    cursor = conn.cursor()

    # Serialize AST as JSON using the to_dict method of Node
    serialized_ast = json.dumps(ast.to_dict())

    cursor.execute('''INSERT INTO rules (rule_string, ast) VALUES (?, ?)''', (rule_string, serialized_ast))

    conn.commit()
    conn.close()


# Function to retrieve a rule from the database
def get_rule(rule_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT rule_string, ast FROM rules WHERE id = ?''', (rule_id,))
    rule = cursor.fetchone()

    conn.close()
    if rule:
        # Deserialize AST from JSON using the from_dict method of Node
        ast = Node.from_dict(json.loads(rule[1]))
        return rule[0], ast
    return None, None
