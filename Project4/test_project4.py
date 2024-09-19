import unittest
from unittest.mock import patch, mock_open
import random
from grammar import GrammarError, Terminal, Variable, Option, Rule, Grammar

class MockRandom:
    @staticmethod
    def choices(population, weights):
        return [population[0]]

class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.grammar = Grammar()

    def test_add_rule(self):
        rule = Rule([Option(1, [Terminal('test')])])
        self.grammar.add_rule('test_rule', rule)
        self.assertIn('test_rule', self.grammar.rules)

    def test_get_rule(self):
        rule = Rule([Option(1, [Terminal('test')])])
        self.grammar.add_rule('test_rule', rule)
        self.assertEqual(self.grammar.get_rule('test_rule'), rule)

    def test_get_rule_invalid(self):
        with self.assertRaises(GrammarError):
            self.grammar.get_rule('invalid_rule')

    def test_terminal_generate(self):
        terminal = Terminal('hello')
        self.assertEqual(list(terminal.generate()), ['hello'])

    def test_variable_generate(self):
        rule = Rule([Option(1, [Terminal('test')])])
        self.grammar.add_rule('test_rule', rule)
        variable = Variable('test_rule', self.grammar)
        self.assertEqual(list(variable.generate()), ['test'])

    def test_variable_invalid(self):
        with self.assertRaises(GrammarError):
            variable = Variable('invalid_rule', Grammar())
            list(variable.generate())

    def test_option_generate(self):
        option = Option(1, [Terminal('hello'), Terminal('world')])
        self.assertEqual(list(option.generate()), ['hello', 'world'])

    def test_option_invalid_weight(self):
        with self.assertRaises(GrammarError):
            Option(0, [Terminal('hello')])

    def test_option_invalid_symbols(self):
        with self.assertRaises(GrammarError):
            Option(1, ['invalid'])

    @patch('random.choices', MockRandom.choices)
    def test_rule_generate(self):
        random.seed(1)
        rule = Rule([
            Option(1, [Terminal('hello')]),
            Option(1, [Terminal('world')])
        ])
        self.assertEqual(list(rule.generate()), ['hello'])

    @patch('builtins.open', new_callable=mock_open, read_data="{\ntest_rule\n1 hello\n}\n")
    def test_grammar_from_file(self, mock_open):
        with open('dummy_file', 'r') as file:
            grammar = Grammar.get_file(file)
            self.assertIn('test_rule', grammar.rules)
            self.assertIsInstance(grammar.rules['test_rule'], Rule)
            self.assertEqual(grammar.sentence_generator('test_rule'), 'hello')
