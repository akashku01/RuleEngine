import unittest
from rule_engine import create_rule, combine_rules, evaluate_rule, save_rule, get_rule, Node

class RuleEngineTests(unittest.TestCase):

    def test_create_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        self.assertIsNotNone(ast, "AST should be created successfully.")
        self.assertEqual(ast.type, "operator")
        self.assertEqual(ast.value, "AND")
        self.assertEqual(ast.left.value, ("age", ">", 30))
        self.assertEqual(ast.right.value, ("department", "=", "Sales"))

    def test_combine_rules(self):
        rules = [
            "age > 30 AND department = 'Sales'",
            "salary > 50000 OR experience > 5"
        ]
        combined_ast = combine_rules(rules)
        self.assertIsNotNone(combined_ast, "Combined AST should be created successfully.")
        self.assertEqual(combined_ast.type, "operator")
        self.assertEqual(combined_ast.value, "AND")
        self.assertEqual(combined_ast.left.type, "operator")
        self.assertEqual(combined_ast.right.type, "operator")

    def test_evaluate_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        result = evaluate_rule(ast, data)
        self.assertTrue(result, "The user should satisfy the rule.")

    def test_save_and_get_rule(self):
        rule_string = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule_string)
        save_rule(rule_string, ast)

        # Retrieve rule from DB
        rule_id = 1  # Assuming the rule was saved with ID 1
        rule_str, ast_from_db = get_rule(rule_id)

        self.assertEqual(rule_string, rule_str, "The rule strings should match.")
        self.assertEqual(ast.left.value, ast_from_db.left.value, "The left operand should match.")
        self.assertEqual(ast.right.value, ast_from_db.right.value, "The right operand should match.")

if __name__ == "__main__":
    unittest.main()
