#!/bin/bash

courseChanges=$(git diff ../frontend/src/data/json/$1/courses.json | head)
if [[ $courseChanges != "" ]];
then
    git add ../frontend/src/data/json/$1/courses.json
fi

pathwayChanges=$(git diff ../frontend/src/data/json/$1/pathways.json | head)
if [[ $pathwayChanges != "" ]];
then
    git add ../frontend/src/data/json/$1/pathways.json
fi

if [[ $courseChanges != "" || $pathwayChanges != "" ]];
then
    git commit -m "Automated update of files"
    git push
fi
