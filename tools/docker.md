# Docker
## Setup
config in `/etc/docker/daemon.json`

apply changes `sudo systemctl restart docker`

view system config `docker info`

docker memory `docker system df`, system memory `df -h`

cpu, mem, net usage `docker stats --no-stream`

rm cache `docker builder prune`

ids sha256 `-q` flag

force, no confirmation `-f` flag

## Dangling images
Dangling images are images which do not have a tag, and do not have a child image pointing to them. The main reason to keep them around is for build caching purposes. [link](https://stackoverflow.com/questions/45142528/what-is-a-dangling-image-and-what-is-an-unused-image)

list `docker images -f dangling=true`

remove `docker images --quiet --filter=dangling=true | xargs --no-run-if-empty docker rmi` or `docker rmi $(docker images -f dangling=true -q)`

