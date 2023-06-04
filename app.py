from flask import Flask, render_template, request
import logging
import sys
import json
import os

logging.disable(sys.maxsize)
import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.search import IndexSearcher, Query
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import Version
from java.nio.file import Paths

app = Flask(__name__)

# Path to the directory where the index is located
index_dir = "index"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")

    results = []
    try:
        directory = FSDirectory.open(File(index_dir).toPath())
        reader = DirectoryReader.open(directory)
        searcher = IndexSearcher(reader)

        analyzer = StandardAnalyzer()
        query_parser = QueryParser("body", analyzer)
        lucene_query = query_parser.parse(query)

        hits = searcher.search(lucene_query, 10)

        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            result = {
                "title": doc.get("title"),
                "body": doc.get("body"),
                "id": doc.get("id"),
                "upvotes": doc.get("upvotes"),
                "url": doc.get("url"),
                "permalink": doc.get("permalink"),
                "score": hit.score
            }
            results.append(result)

    except Exception as e:
        print("An error occurred during search:", str(e))

    return render_template("results.html", query=query, results=results)

if __name__ == "__main__":
    app.run()
