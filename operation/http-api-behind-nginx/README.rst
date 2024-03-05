#############################
CrateDB HTTP API behind Nginx
#############################


*****
About
*****

Nginx configuration for hosting the CrateDB HTTP API endpoint on a subdirectory
path. Here: `/db`.


*****
Usage
*****

Start CrateDB::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 --name=cratedb crate/crate:5.0.1 -Cdiscovery.type=single-node -Ccluster.routing.allocation.disk.threshold_enabled=false

Start Nginx::

    wget https://raw.githubusercontent.com/crate/cratedb-examples/main/stacks/http-api-behind-nginx/nginx.conf
    nginx -c $(pwd)/nginx.conf

Then, navigate to http://localhost:7070/db/.
