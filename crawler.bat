@echo off
set /p subreddit_input=Enter subreddits, limits, post queries, and comment queries (e.g. dog 5 "dog" "dog" amex 5 "plat" "plat"):
REM Sort by relevance (default) 
REM Sort by hot 
REM Sort by new 
REM Sort by comments 
REM Sort by rising 
python script.py %subreddit_input%