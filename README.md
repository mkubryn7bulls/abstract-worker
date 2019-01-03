Simple worker based on event bus

# Building
    docker-compose build

# Running
On a Docker swarm cluster:

    docker stack deploy --compose-file docker-compose.yml absta-worker
