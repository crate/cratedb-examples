# Using CrateDB with turbodbc (OCI)

The [dockerfiles](./dockerfiles) folder includes Dockerfiles that exercise
installing the turbodbc driver. They are handy if you can't install it
on your machine. Follow the instructions how to build OCI images and how
to invoke the `demo.py` program using them.

## Build

Make the upcoming build more verbose.
```shell
export BUILDKIT_PROGRESS=plain
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
```

Build images.
```shell
docker build --tag local/turbodbc-demo-archlinux --file=dockerfiles/archlinux.Dockerfile .
docker build --tag local/turbodbc-demo-centos --file=dockerfiles/centos.Dockerfile .
docker build --tag local/turbodbc-demo-debian --file=dockerfiles/debian.Dockerfile .
docker build --tag local/turbodbc-demo-opensuse --file=dockerfiles/opensuse.Dockerfile .
```

Invoke demo program.
```shell
for OS in archlinux centos debian opensuse; do
  docker run --rm -it --volume=$(pwd):/src --network=host \
    local/turbodbc-demo-${OS} python3 /src/demo.py
done
```
