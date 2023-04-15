from flask import Flask, request, jsonify
#from chatbot import get_completions
#from bota import get_completions
from bot import get_completions

app = Flask(__name__)

@app.route('/api/ask', methods=['POST'])
def ask():
    # Get the user's question and language preference from the request
    prompt = request.form['prompt']
    language = request.form['language']

    # Retrieve completions for the given prompt and language
    completions = get_completions(prompt, language)

    # Return the completions as a JSON response
    return jsonify(completions)

@app.route('/api/completions')
def completions():
    prompt = request.args.get('prompt')
    language = request.args.get('language')
    completions = get_completions(prompt, language)
    return jsonify(completions=completions)

@app.route('/')
def index():
    return '''
        <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>Chatbot</title>
                <style>
                    body {
                        background-color: #f2f2f2;
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }

                    #header {
                        background-color: #007bff;
                        color: #fff;
                        padding: 20px;
                        text-align: center;
                    }

                    h1 {
                        margin: 0;
                        font-size: 36px;
                        font-weight: bold;
                    }

                    form {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        margin-top: 50px;
                    }

                    label {
                        font-size: 20px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }

                    input[type="text"], select {
                        padding: 10px;
                        font-size: 16px;
                        border: none;
                        border-radius: 5px;
                        margin-bottom: 20px;
                        width: 100%;
                    }

                    button[type="submit"] {
                        background-color: #007bff;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 16px;
                    }

                    button[type="submit"]:hover {
                        background-color: #0069d9;
                    }

                    ul {
                        list-style-type: none;
                        padding: 0;
                        margin-top: 50px;
                    }

                    li {
                        background-color: #fff;
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        margin-bottom: 10px;
                        box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
                    }

                    #footer {
                        background-color: #f2f2f2;
                        color: #666;
                        font-size: 14px;
                        padding: 10px;
                        text-align: center;
                        position: absolute;
                        bottom: 0;
                        width: 100%;
                    }
                </style>
            </head>
            <body>
                <h1>Chatbot</h1>
                <form id="question-form">
                    <label for="prompt">Enter your question:</label>
                    <input type="text" id="prompt" name="prompt" required>

                    <label for="language">Select language:</label>
                     <select id="language" name="language">
                       <option value="en">English</option>
                        <option value="sl">Slovenian</option>
                    </select>

                    <button type="submit">Ask</button>
                </form>

                <ul id="completions"></ul>

                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script>
                    $(function() {
                        $('#question-form').on('submit', function(event) {
                            event.preventDefault();

                            $.ajax({
                                url: '/api/ask',
                                method: 'POST',
                                data: $(this).serialize(),
                                success: function(response) {
                                
                  $('#completions').empty();
                  $.each(response, function(index, completion) {
                    $('#completions').append('<li>' + completion + '</li>');
                  });
                },
                error: function() {
                  alert('An error occurred.');
                }
              });
            });
          });
        </script>
    '''

if __name__ == '__main__':
    app.run(debug=True)