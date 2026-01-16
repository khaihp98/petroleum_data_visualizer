@echo off
git init
git add .
git commit -m "Initial commit"
git status > git_log.txt 2>&1
dir /a .git >> git_log.txt 2>&1
