import sqlite3
import openai
import nltk

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the prompts for legal, accounting, and business questions in Slovenian
legal_prompt = "Pravno vprašanje:"
accounting_prompt = "Računovodsko vprašanje:"
business_prompt = "Poslovno vprašanje:"

# Set up the maximum number of completions to retrieve from the OpenAI API
max_completions = 10

# Set up the name of the local database
db_name = "completions.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_name)

# Create the completions table if it does not exist
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS completions
             (prompt text, completion text)''')
conn.commit()

# Close the database connection
conn.close()

# Define a function to retrieve completions from the local database
def get_completions_from_db(prompt):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM completions WHERE prompt=?", (prompt,))
    row = c.fetchone()
    if row:
        completions = row[1].split("\n")
    else:
        completions = None
    conn.close()
    return completions

# Define a function to add completions to the local database
def add_completions_to_db(prompt, completions):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO completions VALUES (?, ?)", (prompt, "\n".join(completions)))
    conn.commit()
    conn.close()

# Define a function to retrieve completions from the OpenAI API
def get_completions_from_api(prompt, language=None):
    completions = []
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        n=max_completions,
        stop=None,
    )
    for choice in response.choices:
        text = choice.text.strip()
        completions.append(text)
    return completions

# Define a function to retrieve completions from the database or the OpenAI API
def get_completions(prompt, language=None):
    completions = get_completions_from_db(prompt)
    if not completions:
        engine = "davinci"

        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=1024,
            n=max_completions,
            stop=None,
            temperature=0.5,
            frequency_penalty=0,
            presence_penalty=0,
        )
        completions = []
        for choice in response.choices:
            text = choice.text.strip()
            completions.append(text)
        add_completions_to_db(prompt, completions)
    return completions

# Define a function to get user input and retrieve completions
def run_chatbot():
    while True:
        prompt = input("Enter your prompt: ")
        if not prompt:
            break
        completions = get_completions(prompt, language="sl")
        for i, completion in enumerate(completions):
            print(f"{i+1}. {completion}")

if __name__ == "__main__":
    # Download the NLTK data for tokenization
    nltk.download("punkt")
    # Run the chatbot
    run_chatbot()
