#!/bin/sh

# This script can be used to rename the myproject, myapp, 
# and myusername (dockerhub username) to your own names.

project=newproject          # Django project name
app=newapp                  # First Django app name
dockeruser=mynewusername    # Docker Hub username

find . -type f -exec sed -i "s/myproject/$project/g" {} \;
find . -type f -exec sed -i "s/myapp/$app/g" {} \;
find . -type f -exec sed -i "s/myusername/$dockeruser/g" {} \; 

mv src/myapp src/$app
mv src/myproject src/$project
