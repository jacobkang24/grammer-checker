# project4.py
#
# ICS 33 Spring 2024
# Project 4: Still Looking for Something

from grammar import Grammar, GrammarError

def main() -> None:
    file_path = input()
    num_sentences = int(input())
    var_name = input()

    try:
        with open(file_path, 'r') as file:
            grammar = Grammar.get_file(file)
            sentences = [grammar.sentence_generator(var_name) for _ in range(num_sentences)]
            for sentence in sentences:
                print(sentence)
    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")
    except GrammarError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
