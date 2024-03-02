# app.py

from flask import Flask, render_template, request, g, jsonify
import psycopg2
import vector_database_module as db_module
import sentiment_analysis_module as sentiment_module
import openai

app = Flask(__name__)

# PostgreSQL connection parameters
DB_NAME = 'conversation'
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '5432'

# OpenAI API key
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            db = g._database = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
        except psycopg2.OperationalError as e:
            # Handle connection error gracefully
            error_message = f"Error connecting to the database: {e}"
            print(error_message)
            return None, error_message
    return db, None

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/conversation', methods=['POST'])
def conversation():
    user_input = request.form.get('user_input')
    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400
    
    db, db_error = get_db()
    if db is None:
        return jsonify({'error': 'Database connection error', 'details': db_error}), 500
    
    # Save user input to vector database
    try:
        db_module.save_user_input(db, user_input)
    except Exception as e:
        return jsonify({'error': f'Error saving user input: {str(e)}'}), 500
    
    # Generate response using OpenAI model
    try:
        response = generate_response(user_input)
    except Exception as e:
        return jsonify({'error': f'Error generating response: {str(e)}'}), 500
    
    # Perform sentiment analysis
    try:
        sentiment = sentiment_module.analyze_sentiment(response)
    except Exception as e:
        return jsonify({'error': f'Error analyzing sentiment: {str(e)}'}), 500
    
    # Save response and sentiment to vector database
    try:
        db_module.save_response(db, response, sentiment)
    except Exception as e:
        return jsonify({'error': f'Error saving response: {str(e)}'}), 500
    
    return render_template('conversation.html', user_input=user_input, response=response, sentiment=sentiment)

def generate_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        # Handle OpenAI API error gracefully
        error_message = f"Error generating response from OpenAI: {e}"
        print(error_message)
        raise

if __name__ == '__main__':
    app.run(debug=True)
