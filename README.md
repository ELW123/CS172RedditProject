Reddit post collector part A:

Run the crawler.bat file to run the python crawler. 

Input the arguements as a string in the following format: 

```sh
<Sub_Reddit_Name_1> <Post_limit_1> <Post_Search_Query_Term_1> <Comment_Search_Query_Term_1> ... <Sub_Reddit_Name_n> <Post_limit_n> <Post_Search_Query_Term_n> <Comment_Search_Query_Term_n> <sorting_method>
```

For example, the following command

```sh
python script.py dogs 2 cute puppy cats 2 cute kitten top
```

searches for the top 2 posts on r/dogs and r/cats that contain the word "cute" in their title or body, and the word "puppy" or "kitten" respectively in their comments. The results will be sorted by "top".


Only comments that have search query term will be processed. 
Collected post infomation will be written into the JSON file. 

Reddit Post collector part B:

Deploy Program:
To run the indexer.py:
Python3 indexer.py 
Indexer will create reddit_lucene_index which is the indexed data 

To run the Flask App:
Make sure that reddit_lucene_index created 
Export FLASK_APP=app
flask run -h 0.0.0.0 -p 8888
Enter the query term into the search bar in the html form.
Click search and top 10 results will appear. 

