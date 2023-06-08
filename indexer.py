import lucene
import os
import json
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def create_index(data, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)
    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    for post in data["posts"]:
        title = post['title']
        body = post['body']
        doc = Document()
        doc.add(Field('Title', str(title), metaType))
        doc.add(Field('Body', str(body), contextType))
        writer.addDocument(doc)
    writer.close()

def index_data():
    with open('reddit_data.json') as json_file:
        data = json.load(json_file)
    create_index(data, 'reddit_lucene_index/')

if __name__ == "__main__":
    index_data()
