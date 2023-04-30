import praw
import json



# Fill in your own stuff here
reddit = praw.Reddit(client_id= ID, 
                     client_secret= SECRET,
                     user_agent= AGENT,        
                     username= USERNAME,  
                     password= PASSWORD)

top = reddit.subreddit("csMajors").top(limit=1)

data = {"posts": []}

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
        post_data["comments"].append(comment.body)
        print("Comment:", comment.body)
        print()

    data["posts"].append(post_data)

with open("reddit_data.json", "w") as outfile:
    json.dump(data, outfile)