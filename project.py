import praw
import json
import sys
import threading
from simhash import Simhash

if len(sys.argv) < 2:
    print("Usage: python script.py subreddit1 limit1 post_query1 comment_query1 [subreddit2 limit2 post_query2 comment_query2 ...] [sort_method]")
    sys.exit(1)

subreddits = []
i = 1
while i < len(sys.argv) - 1:
    subreddit_name = sys.argv[i]
    limit = int(sys.argv[i+1])
    post_search_query = sys.argv[i+2]
    comment_search_query = sys.argv[i+3]
    subreddits.append((subreddit_name, limit, post_search_query, comment_search_query))
    i += 4

sort_method = sys.argv[-1] if len(sys.argv) % 4 == 2 else 'relevance'

# Fill in your own stuff here
reddit = praw.Reddit(client_id='ID',
                    client_secret='Secret',
                    user_agent='Agent')

data = {"posts": []}

# Define a function to process each post and its comments
def process_post(post, post_search_query, comment_search_query):
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

    post_exists = False
    post_url_simhash = Simhash(post.url)

    for existing_post_data in data["posts"]:
        existing_post_url_simhash = Simhash(existing_post_data["url"])
        if post_url_simhash.distance(existing_post_url_simhash) <= 3:
            post_exists = True

    if post_exists:
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            if comment_search_query in comment.body:
                post_data["comments"].append(comment.body)
                print("Comment:", comment.body)
                print()

        if len(post_data["comments"]) > 0:
            data["posts"].append(post_data)

# Define a function to process a batch of posts on a separate thread
def process_posts(posts, post_search_query, comment_search_query):
    for post in posts:
        process_post(post, post_search_query, comment_search_query)

# Process each subreddit on a separate thread
threads = []
for subreddit_name, limit, post_search_query, comment_search_query in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = list(subreddit.search(query=post_search_query, sort=sort_method, limit=limit))
    thread = threading.Thread(target=process_posts, args=(top_posts, post_search_query, comment_search_query))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Write the results to a JSON file
with open("reddit_data.json", "w") as outfile:
    json.dump(data, outfile)