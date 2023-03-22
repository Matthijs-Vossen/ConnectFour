import random

class Lines:

    def __init__(self, file_path):
        self.suggestions = []
        self.feedbacks = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('suggestions'):
                mode = 'suggestions'
            elif line.startswith('feedback'):
                mode = 'feedback'
            elif mode == 'suggestions' and line.strip() != '':
                self.suggestions.append(line.strip())
            elif mode == 'feedback' and line.strip() != '':
                self.feedbacks.append(line.strip())

    def get_random_suggestion(self, column):
        return random.choice(self.suggestions).format(column)

    def get_random_feedback(self, column):
        return random.choice(self.feedbacks).format(column)

""" file_path = 'lines/clippy_lines.txt'
column = 3
sf = Lines(file_path)
print(sf.get_random_suggestion(column))
print(sf.get_random_feedback(column)) """