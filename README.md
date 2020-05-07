# rt-share
Online editing of a file

## TODOs:
- make the editing work for text selections and multiple characters at a time;
- allow unicode characters (currently only ASCII are allowed);
- make each text cursor bound to the client;
- order the requests to make the mmap operations more efficient;

## Running locally
You should have docker-compose installed. To deploy the stack locally, execute the following commands:

```
git clone https://github.com/Mapharazzo/rt-share.git
cd rt-share
docker-compose up --build
```

Now the app should be available at http://localhost:5000

## Deploying to AWS
Tested with `docker-machine` utility.

To create each machine remotely on AWS, execute

```
docker-machine create --driver amazonec2 --amazonec2-region eu-central-1 --amazonec2-open-port 5000 --amazonec2-open-port 5001 --amazonec2-open-port 3000 --amazonec2-open-port 2377 --amazonec2-access-key <ACCESS_KEY> --amazonec2-secret-key <SECRET_KEY> <MACHINE_NAME>
```

Then, for the `docker swarm` part, make a node the manager by entering a SSH session on a machine using `docker machine ssh <MACHINE_NAME>`, then initialize the swarm using `docker swarm init`. Keep the command and key given as you will need to use it on the other nodes.
For each other machine, enter a SSH session using the same command as above and then execute the command with the key given by the node manager.