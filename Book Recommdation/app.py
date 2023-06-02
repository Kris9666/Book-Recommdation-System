from flask import Flask, render_template, request
import numpy as np
import pickle


app = Flask(__name__)

popular_df = pickle.load(open('popular.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

@app.route('/famous_books')
def famous_books():
    return render_template('popular.html',
                            book_name = list(popular_df['Book-Title'].values),
                            author = list(popular_df['Book-Author'].values),
                            rating = list(popular_df['Avg-Rating'].values),
                            votes = list(popular_df['Num-Rating'].values),
                            image = list(popular_df['Image-URL-M'].values)
                        )


@app.route('/recommend')
def recommend():
    return render_template('index.html')

@app.route('/recommend_books', methods=['POST', 'GET'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(df.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:5]

    data = []
    for i in similar_item:
        suggestion = []
        temp_df = books[books['Book-Title'] == df.index[i[0]]]
        suggestion.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        suggestion.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        suggestion.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(suggestion)

    print(data)
        
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
