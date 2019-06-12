# This is how you can run mongo on your local with docker with auto-restart on boot

# Create a container from the mongo image, 
#  run is as a daemon (-d), expose the port 27017 (-p),
#  set it to auto start (--restart)
#  and with mongo authentication (--auth)
# Image used is https://hub.docker.com/_/mongo/
docker pull mongo
docker run --name ultimate-mongo-container --restart=always --volume=/home/n1ght0wl/my-docker-volumes/mongo-volume -d -p 27017:27017 mongo mongod --auth

# Using the mongo "localhost exception" (https://docs.mongodb.org/v3.0/core/security-users/#localhost-exception) 
# add a root user

# bash into the container
sudo docker exec -i -t YOURCONTAINERNAME bash

# connect to local mongo
mongo

# create the first admin user
use admin
db.createUser({user:"user",pwd:"password",roles:[{role:"root",db:"admin"}]})

# exit the mongo shell
exit
# exit the container
exit

# test using a mongo client
mongo -u "user" -p "password" localhost:27017 --authenticationDatabase "admin"