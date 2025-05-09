def recommend_movies(intent):
    recommendations = {
        'action': ["John Wick", "Mad Max: Fury Road", "The Dark Knight"],
        'romance': ["The Notebook", "La La Land", "Pride and Prejudice"],
        'comedy': ["Superbad", "The Hangover", "Step Brothers"]
    }

    for genre in recommendations:
        if genre in intent:
            return recommendations[genre]
    
    return ["Sorry, I couldn’t find recommendations for that."]
