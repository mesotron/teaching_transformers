"""
Extract training, validation and test data from the DeepMind Mathematics 
dataset; we will use a small portion of this data for our experiments. This 
script essentially preps files that are used as input by 
elaborate_remainder.py, which creates our final training, test, and 
validation data.

Note that this relies upon various files from the DeepMind Mathematics
dataset being present in math_path, in the subdirectories in which it
expects to see them, in order to run correctly; furthermore, the output was
separately renamed and truncated to yield the files in data/originals, and
the output of format_benchmarks.py depends on the random seed. To use 
exactly the same data that was used in the paper, simply use the files 
already present in data/originals.
"""

from paths import math_path
import re
import random
import math
from collections import defaultdict

# Name of the question type we are working with in the DeepMind math dataset
QUESTION_TYPE = 'numbers__div_remainder'
# Size of pool of instances to draw from for our interpolated test set
INTERPOLATED_MAX_INSTANCES = 10000
# Size of pool of instances to draw from for our 'same distribution' test set
SAMEDIST_MAX_INSTANCES = 2500
# Line at which to switch from treating lines from train-easy, train-medium, 
# and train-hard as comprising potential training data to comprising potential
# validation data. Set 5% of the file aside as potential validation data -
# VALIDATION_START_LINE is 95% of the way into the file.
# Ultimately ended up using far less training and test data for the experiments
# reported in the manuscript.
VALIDATION_START_LINE = 1266672

def load_training_set(n):
    """ Return a set containing the first n examples of the training set. """
    training_set = set()

    with open(math_path + 'train_' + QUESTION_TYPE + '.txt', 'r', encoding='utf-8') as in_file:
        i = 0
        for line in in_file:
            if i == n:
                break
            training_set.add(line)
            i += 1
    return training_set

def get_digit_distribution(input_path):
    """
    Return a string that contains the distribution of divisor and
    dividend lengths of the problems in the file given by `input_path`.
    """

    divisor_lengths = defaultdict(int)
    dividend_lengths = defaultdict(int)

    with open(input_path, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            m = re.search(r'when (\d+) is divided by (\d+)(\.|\?)\|(\d+)', line)
            divisor_lengths[len(m.group(1))] += 1
            dividend_lengths[len(m.group(2))] += 1
    upper =     max(divisor_lengths.keys()) + 1
    divisor_strings = [f'{x}: {divisor_lengths[x]}' for x in range(1, upper)]
    dividend_strings = [f'{x}: {dividend_lengths[x]}' for x in range(1, upper)]
    return 'divisor lengths\n' + '\n'.join(divisor_strings) + \
        '\ndividend lengths\n' + '\n'.join(dividend_strings) + '\n'

def inspect_digit_distributions():
    """
    Write a file named 'digit_distributions.txt' (in math_path) that contains
    the digit distributions of the 'easy', 'medium', 'hard', and interpolated
    test questions of type QUESTIONTYPE from the DeepMind Mathematics dataset.
    """

    with open(math_path + 'digit_distributions.txt', 'w') as out_file:
        out_file.write('Easy\n')
        out_file.write(get_digit_distribution(f'{math_path}easy_{QUESTION_TYPE}.txt'))
        out_file.write('Medium\n')
        out_file.write(get_digit_distribution(f'{math_path}medium_{QUESTION_TYPE}.txt'))
        out_file.write('Hard\n')
        out_file.write(get_digit_distribution(f'{math_path}hard_{QUESTION_TYPE}.txt'))
        out_file.write('Interpolated\n')
        out_file.write(get_digit_distribution(f'{math_path}test_{QUESTION_TYPE}.txt'))

def flatten_file(input_path, output_path):
    """
    Convert a file from the DeepMind Mathematics Dataset format in which every
    even line has questions and every odd line has answers to a file where every
    line has a question, a vertical pipe, and an answer.

    :param str input_path: Input filename with path
    :param str output_path: Output filename with path
    """

    with open(input_path, 'r', encoding='utf-8') as in_file:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            for i, input in enumerate(in_file):

                if i % 2 == 0:
                    # Every even line has questions
                    last_question = input
                else:
                    # Every odd line has answers
                    out_file.write(last_question.strip() + '|' + input.strip() + '\n')


def flatten_test_file():
    """
    Generate a 'flattened' version of the original 'interpolated' test set from
    the DeepMind mathematics dataset e.g., a file where each line consists of a
    question, a vertical pipe, and an answer
    """
    flatten_file(math_path + 'interpolate/' + QUESTION_TYPE + '.txt',
                 math_path + 'test_' + QUESTION_TYPE + '.txt');

def extract_interpolated_test_set(training_set, seed, n, set_id):
    """
    Extract a test set - ** using data from original 'interpolated' test set **
    - of size n using the given random seed; write to file with set_id in its
    name. Relies on the 'flattened' version of this test set generated by
    flatten_test_file.
    """
    random.seed(seed)
    test_set = set()

    with open(math_path + f'test_{QUESTION_TYPE}.txt', 'r', encoding='utf-8') as in_file:
        lines = [line for line in in_file]
        with open(math_path + f'interpolatedtest_{QUESTION_TYPE}_set{set_id}.txt', 'w', encoding='utf-8') as out_file:
            while len(test_set) < n:
                instance = lines[random.randint(0, INTERPOLATED_MAX_INSTANCES - 1)]
                if not instance in training_set:
                    test_set.add(instance)
            out_file.writelines(test_set)



def extract_same_distribution_test_set(training_set, seed, n, set_id):
    """
    Extract a test set - ** using data from same distribution as the training
    distribution ** - of size n using the given random seed; write to file with
    set_id in its name.
    """
    random.seed(seed)
    test_set = set()

    with open(math_path + f'easy_{QUESTION_TYPE}.txt', 'r', encoding='utf-8') as easy_file:
        with open(math_path + f'medium_{QUESTION_TYPE}.txt', 'r', encoding='utf-8') as medium_file:
            with open(math_path + f'hard_{QUESTION_TYPE}.txt', 'r', encoding='utf-8') as hard_file:
                easy_lines = [line for line in easy_file]
                medium_lines = [line for line in medium_file]
                hard_lines = [line for line in hard_file]
                with open(math_path + f'samedisttest_{QUESTION_TYPE}_set{set_id}.txt', 'w', encoding='utf-8') as out_file:
                    while len(test_set) < n:
                        lines = random.choice([easy_lines, medium_lines, hard_lines])
                        instance = lines[random.randint(0, SAMEDIST_MAX_INSTANCES - 1)]
                        if not instance in training_set:
                            test_set.add(instance)
                    out_file.writelines(test_set)


def interleave_training_files():
    """
    Generate training and validation data with an equal number of questions
    drawn from train-easy, train-medium, and train-hard. Analogous to the method
    said to be used in https://github.com/deepmind/mathematics_dataset - its
    README states 'Note the training data for each question type is split into
    "train-easy", "train-medium", and "train-hard". This allows training models
    via a curriculum. The data can also be mixed together uniformly from these
    training datasets to obtain the results reported in the paper.'
    """
    with open(math_path + 'train-easy/' + QUESTION_TYPE + '.txt', 'r', encoding='utf-8') as easy_file:
        with open(math_path + 'train-medium/' + QUESTION_TYPE + '.txt', 'r', encoding='utf-8') as medium_file:
            with open(math_path + 'train-hard/' + QUESTION_TYPE + '.txt', 'r', encoding='utf-8') as hard_file:
                with open(math_path + 'train_' + QUESTION_TYPE + '.txt', 'w', encoding='utf-8') as train_file:
                    with open(math_path + 'validation_' + QUESTION_TYPE + '.txt', 'w', encoding='utf-8') as validation_file:
                        out_file = train_file
                        for i, inputs in enumerate(zip(easy_file, medium_file, hard_file)):
                            if i % 2 == 0:
                                # Every even line has questions
                                last_questions = inputs
                            else:
                                # Every odd line has answers
                                for j in range(3):
                                    out_file.write(last_questions[j].strip() + '|' + inputs[j].strip() + '\n')
                            if i == VALIDATION_START_LINE:
                                out_file = validation_file


def generate_transcription_benchmark(count):
    """
    Generate a benchmark for grading the success of the initial transcription only
    :param int count: Number of examples to include in the benchmark
    """
    output_filename = math_path + 'validate-transcriptions_' + str(count) + '_' + QUESTION_TYPE + '.txt'
    with open(math_path + 'validation_' + QUESTION_TYPE + '.txt', 'r', encoding='utf-8') as in_file:
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            for i, line in enumerate(in_file):
                if (i == count):
                    break
                tokens = line.partition('|')
                tokens[0]

                m = re.search(r'when (.*?) is divided by (.*?)(\.|\?)', tokens[0])
                desired_transcription = m.group(2) + 'ſ' + m.group(1)
                out_file.write(tokens[0] + '|' + desired_transcription + '\n')

# Extract training, validation and test data from the DeepMind Mathematics dataset;
# we will use a small portion of this data for our experiments

interleave_training_files()
flatten_test_file();
training_set = load_training_set(1000)
extract_interpolated_test_set(training_set, 500, 500, 500)
extract_same_distribution_test_set(training_set, 500, 500, 500)
