import random

class Lines:
    """A class to read suggestions and feedbacks from a file.

    Attributes:
        suggestions (list): A list of suggestion strings.
        feedbacks (list): A list of feedback strings.
    """

    def __init__(self, file_path):
        """Initialize the Lines object with suggestions and feedbacks from a file.

        Args:
            file_path (str): The path to the file containing suggestions and feedbacks.
        """

        self.suggestions = []
        self.feedbacks = []

        # Read lines from file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Parse lines into suggestions and feedbacks
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
        """Return a random suggestion string formatted with a column name.

        Args:
            column (str): The name of the column to format into the suggestion string.

        Returns:
            str: A random suggestion string formatted with a column name.
        """
        return random.choice(self.suggestions).format(column)

    def get_random_feedback(self, column):
        """Return a random feedback string formatted with a column name.

        Args:
            column (str): The name of the column to format into the feedback string.

        Returns:
            str: A random feedback string formatted with a column name.
        """
        return random.choice(self.feedbacks).format(column)