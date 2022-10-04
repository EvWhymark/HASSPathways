#!/bin/bash

git add "../frontend/src/data/json/$1/courses.json"
git add "../frontend/src/data/json/$1/pathways.json"
git commit -m "Automated update of files"
git push
