@echo off
set /p subreddit_input=Enter subreddits, limits, post queries, and comment queries (e.g. boba 5 "tea" "amazing" Porsche 5 "new" "drive"):
REM Sort by relevance (default) 
REM Sort by hot 
REM Sort by new 
REM Sort by comments 
REM Sort by rising 
python project.py %subreddit_input%
