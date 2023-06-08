from flask import Flask, request, render_template
import lucene
from org.apache.lucene.store import NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BoostQuery
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause

app = Flask(__name__)

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    analyzer = StandardAnalyzer()

    # Parse queries
    titleQuery = QueryParser("Title", analyzer).parse(query)
    bodyQuery = QueryParser("Body", analyzer).parse(query)

    # Boost title field by a factor of 2
    boostedTitleQuery = BoostQuery(titleQuery, 2.0)

    # Combine queries
    combinedQuery = BooleanQuery.Builder()
    combinedQuery.add(boostedTitleQuery, BooleanClause.Occur.SHOULD)
    combinedQuery.add(bodyQuery, BooleanClause.Occur.SHOULD)

    topDocs = searcher.search(combinedQuery.build(), 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "title": doc.get("Title"),
            "text": doc.get("Body")
        })
    return topkdocs

@app.route("/")
def home():
    return 'hello!~!!'

@app.route("/abc")
def abc():
    return 'hello alien'

@app.route('/input', methods = ['GET'])
def input():
    return render_template('input.html')

@app.route('/output', methods = ['POST'])
def output():
    form_data = request.form
    query = form_data['query']
    print(f"this is the query: {query}")
    lucene.getVMEnv().attachCurrentThread()
    docs = retrieve('reddit_lucene_index/', str(query))
    print(docs)
    return render_template('output.html', lucene_output = docs)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

if __name__ == "__main__":
    app.run(debug=True)