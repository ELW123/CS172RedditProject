@echo off
set /p subreddit_input=Enter subreddits, limits, and search queries (e.g. cats 10 kitten dogs 5 puppy):

python project.py %subreddit_input%