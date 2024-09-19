import random

class GrammarError(Exception):
    pass

class Symbol:
    def generate(self):
        raise NotImplementedError("Generate method must be implemented by subclasses.")


class Terminal(Symbol):
    def __init__(self, value):
        self.value = value

    def generate(self):
        yield self.value


class Variable(Symbol):
    def __init__(self, name, grammar):
        self.name = name
        self.grammar = grammar

    def generate(self):
        rule = self.grammar.get_rule(self.name)
        yield from rule.generate()


class Option:
    def __init__(self, weight, symbols):
        if not isinstance(weight, int) or weight < 1:
            raise GrammarError("Option weight must be a positive integer.")
        if not all(isinstance(symbol, Symbol) for symbol in symbols):
            raise GrammarError("Option symbols must be a list of Symbol instances")
        self.weight = weight
        self.symbols = symbols

    def generate(self):
        for symbol in self.symbols:
            yield from symbol.generate()


class Rule:
    def __init__(self, options):
        if not all(isinstance(option, Option) for option in options):
            raise GrammarError("Rule options must be a list of Options instances.")
        self.options = options

    def generate(self):
        weights = [option.weight for option in self.options]
        chosen_option = random.choices(self.options, weights=weights)[0]
        yield from chosen_option.generate()


class Grammar:
    def __init__(self):
        self.rules = {}

    def add_rule(self, name, rule):
        self.rules[name] = rule

    def get_rule(self, name):
        if name not in self.rules:
            raise GrammarError(f"Variable '{name}' does not exist in the grammar rules.")
        return self.rules[name]

    @staticmethod
    def get_file(file):
        grammar = Grammar()
        lines = file.read().splitlines()
        index = 0

        while index < len(lines):
            line = lines[index]
            if line.startswith("{"):
                index += 1
                var_name = lines[index].strip()
                index += 1
                options = []
                while not lines[index].startswith("}"):
                    parts = lines[index].split(" ", 1)
                    weight = int(parts[0])
                    symbols = []
                    if len(parts) > 1:
                        for symbol in parts[1].split():
                            if symbol.startswith("[") and symbol.endswith("]"):
                                symbols.append(Variable(symbol[1:-1], grammar))
                            else:
                                symbols.append(Terminal(symbol))
                    else:
                        symbols.append(Terminal(""))
                    options.append(Option(weight, symbols))
                    index += 1
                grammar.add_rule(var_name, Rule(options))
            index += 1
        return grammar

    def sentence_generator(self, var_name):
        start_var = Variable(var_name, self)
        return " ".join(word for word in start_var.generate())