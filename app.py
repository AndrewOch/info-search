from flask import request, render_template, Flask

from search_service import preprocess_query, titles, urls
from vector_search import vector_search

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = preprocess_query(request.form['query'])
        raw_results = vector_search(query)[:10]
        results = [{
            'doc_id': doc_id,
            'score': score,
            'title': titles.get(doc_id, 'No title found'),
            'url': urls.get(doc_id, 'No URL found')
        } for doc_id, score in raw_results]
        return render_template('search.html', query=query, results=results)
    return render_template('search.html', query='', results=[])


if __name__ == '__main__':
    app.run(debug=True)
