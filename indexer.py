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
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "text": doc.get("Context")
        })
    print(topkdocs)


index_dir = "index"
query = 'web data'

create_index(index_dir)
retrieve(index_dir, query)

