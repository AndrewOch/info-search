from flask import request, render_template, Flask

from search_service import preprocess_query, titles, urls
from vector_search import vector_search

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = preprocess_query(request.form['query'])
        title_matches = [doc_id for doc_id, title in titles.items() if query.lower() in title.lower()]

        raw_results = vector_search(query)
        vector_search_results = [doc_id for doc_id, _ in raw_results if doc_id not in title_matches]

        combined_results = title_matches[:10] + vector_search_results
        combined_results = combined_results[:10]

        results = [{
            'doc_id': doc_id,
            'score': titles.get(doc_id, 'No title found'),
            'title': titles.get(doc_id, 'No title found'),
            'url': urls.get(doc_id, 'No URL found')
        } for doc_id in combined_results]

        return render_template('search.html', query=query, results=results)
    return render_template('search.html', query='', results=[])


if __name__ == '__main__':
    app.run(debug=True)
