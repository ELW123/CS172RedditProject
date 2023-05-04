Reddit post collector

Run the crawler.bat file to run the python crawler. 

Input the arguements as a string in the following format: 

<Sub_Reddit_Name_1> <Post_limit_1> <Post_Search_Query_Term_1> <Comment_Search_Query_Term_1> ... <Sub_Reddit_Name_n> <Post_limit_n> <Post_Search_Query_Term_n> <Comment_Search_Query_Term_n> <sorting_method>

For example, the following command

```sh
python script.py dogs 2 cute puppy cats 2 cute kitten top
```

searches for the top 2 posts on r/dogs and r/cats that contain the word "cute" in their title or body, and the word "puppy" or "kitten" respectively in their comments. The results will be sorted by "top".


Only comments that have search query term will be processed. 
Collected post infomation will be written into the JSON file. 
