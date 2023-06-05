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

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = FSDirectory.open(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    field_type = FieldType()
    field_type.setStored(True)
    field_type.setTokenized(True)

    data_file = "reddit_data.json"

    with open(data_file, "r") as infile:
        data = json.load(infile)
        for post in data["posts"]:
            doc = Document()
            doc.add(Field("title", post["title"], field_type))
            doc.add(Field("body", post["body"], field_type))
            doc.add(Field("id", post["id"], field_type))
            doc.add(Field("upvotes", str(post["upvotes"]), field_type))
            doc.add(Field("url", post["url"], field_type))
            doc.add(Field("permalink", post["permalink"], field_type))
            for i, comment in enumerate(post["comments"]):
                doc.add(Field("comment_" + str(i+1), comment, field_type))
            doc.add(Field("timestamp", post["timestamp"], field_type))
            writer.addDocument(doc)

    writer.commit()
    writer.close()


def retrieve(storedir, query):
    searchDir = FSDirectory.open(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    analyzer = StandardAnalyzer()
    parser = QueryParser('Context', analyzer)
    parsed_query = parser.parse(query)
    topDocs = searcher.search(parsed_query, 10).scoreDocs
    ranked_docs = rank_documents(top_docs, searcher)
    display_results(ranked_docs, searcher)
    
# should not overflow due to max_time_seconds
def rank_documents(docs: [ScoreDoc], searcher: IndexSearcher):
    ranked_docs = []
    max_time_seconds = sys.maxsize / 3600  # Maximum number of seconds that won't cause overflow
    for doc in docs:
        lucene_doc = searcher.doc(doc.doc)
        timestamp_str = lucene_doc.get("timestamp")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        upvotes = int(lucene_doc.get("upvotes"))
        time_elapsed_seconds = (datetime.now() - timestamp).total_seconds()
        time_elapsed_scaled = min(time_elapsed_seconds, max_time_seconds)
        relevance = upvotes + (1 / (time_elapsed_scaled / 3600))
        ranked_docs.append({"score": doc.score, "doc": lucene_doc, "relevance": relevance})
    ranked_docs.sort(key=lambda x: x["relevance"], reverse=True)
    return ranked_docs

def display_results(docs, searcher):
    for doc in docs:
        print("Score:", doc["score"])
        print("Title:", doc["doc"].get("title"))
        print("Relevance:", doc["relevance"])
        print("-----------")

index_dir = "index"
query = 'web data'

create_index(index_dir)
retrieve(index_dir, query)

