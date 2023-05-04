import praw
import json
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <subreddit limit query>")
    sys.exit(1)

subreddit_input = sys.argv[1]
subreddit_list = subreddit_input.split()

subreddits = []
for i in range(0, len(subreddit_list), 3):
    subreddit_name = subreddit_list[i]
    limit = int(subreddit_list[i+1])
    search_query = subreddit_list[i+2]
    subreddits.append((subreddit_name, limit, search_query))



# Fill in your own stuff here
reddit = praw.Reddit(client_id='ID',
                    client_secret='Secret',
                    user_agent='Agent')

data = {"posts": []}

for subreddit_name, limit, search_query in subreddits:
    top = reddit.subreddit(subreddit_name).top(limit=limit)
    
    for post in top:
        post_data = {
            "title": post.title,
            "body": post.selftext,
            "id": post.id,
            "upvotes": post.score,
            "url": post.url,
            "permalink": post.permalink,
            "comments": []
        }
    
        print("Post Title:", post.title) # title
        print("Post Body Text:", post.selftext) # body
        print("Post ID:", post.id) # id
        print("Number of Upvotes:", post.score) # upvotes
        print("Post URL:", post.url) # image in post
        print("Post Permalink:", post.permalink) # url of post
    
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            if search_query in comment.body:
                post_data["comments"].append(comment.body)
                print("Comment:", comment.body)
                print()
    
        data["posts"].append(post_data)

with open("reddit_data.json", "w") as outfile:
    json.dump(data, outfile)