from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import recommend_movies  # This must match the file and function name

app = Flask(__name__)
CORS(app)

# Simple GET route to test if the server is running
@app.route('/')
def home():
    return 'Flask and CORS are working!'

# POST route to get movie recommendations based on user input
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()  # Ensures JSON body is parsed
    user_input = data.get("query", "").lower() if data else ""
    movies = recommend_movies(user_input)
    return jsonify({"recommendations": movies})

if __name__ == '__main__':
    app.run(debug=True)
