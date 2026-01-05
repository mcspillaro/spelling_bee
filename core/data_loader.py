import csv
from core.session_manager import Word

# Function to load words from a CSV file
def load_words_from_csv(file_path):
    words = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        # Using DictReader to read the CSV file
        reader = csv.DictReader(csvfile)

        required_fields = {'word', 'definition', 'sentence'}
        if not required_fields.issubset(reader.fieldnames): # Validating requirements
            raise ValueError(
                f"CSV file must contain the following headers: {', '.join(required_fields)}"
            )

        # Iterating through each row in the CSV and creating Word instances
        for row in reader:
            word_text = row["word"].strip()
            definition = row["definition"].strip()
            sentence = row["sentence"].strip()

            if not word_text or not definition or not sentence:
                continue  # Skip incomplete entries

            words.append(
                Word(
                    text=word_text,
                    definition=definition,
                    sentence=sentence
                )
            )
    return words