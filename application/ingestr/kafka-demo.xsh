#!/usr/bin/env xonsh

# Demo for loading data from Kafka topic to CrateDB table.
# Accompanies `kafka-compose.yml` and `.env` files.

# End-to-end test feeding data through a pipeline implemented with Apache Kafka,
# ingestr, and CrateDB. The data source is a file in NDJSON format, the
# data sink is a database table in CrateDB.


$XONSH_SHOW_TRACEBACK = True
$INGESTR_DISABLE_TELEMETRY = True


# Compute path to directory of current program.
from pathlib import Path
HERE = Path(__file__).parent.absolute()

# Define infrastructure definition file for Podman or Docker.
$COMPOSE_FILE = HERE / "kafka-compose.yml"

# Load environment variables from dotenv file.
source-bash -n source @(HERE / ".env")


class Infrastructure:
    """
    Manage services: Kafka and CrateDB.

    - Spin up services using Docker Compose.
    - Create and delete Kafka topic.
    """

    def start(self):
        title "Starting services"
        result = ![ docker compose --file $COMPOSE_FILE up --detach ]
        if result.returncode != 0:
            echo "ERROR: Failed to start services"
            exit 1
        echo "Done."
        return self

    def stop(self):
        title "Stopping services"
        docker compose --file $COMPOSE_FILE down --remove-orphans
        echo "Done."
        return self

    def setup(self):
        self.kafka_create_topic()
        return self

    def teardown(self):
        self.kafka_delete_topic()
        return self

    def kafka_create_topic(self):
        title "Creating Kafka topic"
        result = ![ docker compose --file $COMPOSE_FILE run --rm --no-TTY create-topic ]
        if result.returncode != 0:
            echo "ERROR: Failed to create Kafka topic"
            exit 1
        echo "Done."
        return self

    def kafka_delete_topic(self):
        title "Deleting Kafka topic"
        docker compose --file $COMPOSE_FILE run --rm --no-TTY delete-topic
        echo "Done."
        return self


class Datawrapper:
    """
    Wrap actions around data:

    - Acquire data from public resource.
    - Publish data to Kafka topic.
    - Load data from Kafka topic into CrateDB table.
    - Verify data in CrateDB table.
    """

    def acquire(self):
        """Acquire raw data from the Internet"""

        if p"nyc-yellow-taxi-2017-subset.ndjson".exists():
            return self

        title "Acquiring NDJSON data"

        # Acquire NYC Taxi 2017 dataset in JSON format (~90 MB).
        wget --no-clobber --continue "https://gist.githubusercontent.com/kovrus/328ba1b041dfbd89e55967291ba6e074/raw/7818724cb64a5d283db7f815737c9e198a22bee4/nyc-yellow-taxi-2017.tar.gz"

        # Extract archive.
        result = ![ tar -xvf nyc-yellow-taxi-2017.tar.gz ]
        if result.returncode != 0:
            echo "ERROR: Failed to extract archive"
            exit 1

        # Create a subset of the data (5000 records) for concluding the first steps.
        cat nyc-yellow-taxi-2017.json | head -n 5000 > nyc-yellow-taxi-2017-subset.ndjson

        echo "Done."
        return self

    def publish(self):
        """Publish data to Kafka topic"""

        # Publish data to the Kafka topic.
        title "Publishing NDJSON data to Kafka topic"
        result = ![ cat nyc-yellow-taxi-2017-subset.ndjson | docker compose --file $COMPOSE_FILE run --rm --no-TTY publish-topic ]
        if result.returncode != 0:
            echo "ERROR: Failed to publish data to Kafka topic"
            exit 1
        echo "Done."

        # Wait a bit for the data to transfer and converge successfully.
        sleep 3

        return self

    def load(self):
        """Load data into CrateDB"""

        # Invoke ingestr job.
        title "Invoking ingestr job"

        result = ![
            uvx --python=3.12 --prerelease=allow --with-requirements=requirements.txt \
                ingestr ingest --yes \
                --source-uri "kafka://?bootstrap_servers=localhost:9092&group_id=test_group&value_type=json&select=value" \
                --source-table "demo" \
                --dest-uri "cratedb://crate:crate@localhost:5432/?sslmode=disable" \
                --dest-table "doc.kafka_demo"
        ]
        if result.returncode != 0:
            echo "ERROR: Failed to ingest data using ingestr"
            exit 1
        echo "Done."
        return self

    def display(self):
        """Display fragments of data that arrived in CrateDB"""
        from pprint import pprint

        title "Displaying data in CrateDB"

        query_cratedb('REFRESH TABLE "kafka_demo";')
        pprint(query_cratedb('SELECT * FROM "kafka_demo" LIMIT 5;')["rows"])
        pprint(query_cratedb('SELECT COUNT(*) FROM "kafka_demo";')["rows"])

        return self

    def verify(self):
        """Verify fragments of data that arrived in CrateDB"""
        title "Verifying data in CrateDB"
        $size_reference=5000
        $size_actual=query_cratedb('SELECT COUNT(*) FROM "kafka_demo";')["rows"][0][0]
        if int($size_actual) >= $size_reference:
            print_color("{BOLD_GREEN}")
            echo "SUCCESS: Database table contains expected number of at least $size_reference records."
            print_color("{RESET}")
        else:
            print_color("{BOLD_RED}")
            echo "ERROR:   Expected database table to contain at least $size_reference records, but it contains $size_actual records."
            print_color("{RESET}")

            # FIXME: Exiting from code is not the nicest thing. But well, this is currently a script anyway.
            exit 2

        return self


@aliases.register("title")
def title(args):
    """Print a prominent section header."""
    label = args[0]
    guard = '-' * len(label)
    print(guard)
    print_color("{BOLD_YELLOW}" + label + "{RESET}")
    print(guard)


def query_cratedb(sql, url=None):
    """Submit a query to CrateDB using its HTTP interface and return results."""
    import base64
    import json
    import urllib.parse
    import urllib.request

    url = url or __xonsh__.env.get("CRATEDB_HTTP_URL_NOAUTH")
    url += "/_sql?pretty"

    username = __xonsh__.env.get("CRATEDB_USERNAME")
    password = __xonsh__.env.get("CRATEDB_PASSWORD")

    request = urllib.request.Request(
        url,
        data=json.dumps({"stmt": sql}).encode("utf8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    b64auth = base64.standard_b64encode(("%s:%s" % (username, password)).encode()).decode()
    request.add_header("Authorization", "Basic %s" % b64auth)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


def main():
    infra = Infrastructure()
    data = Datawrapper()

    # Standard path.
    infra.start().setup()
    data.acquire().publish().load().display().verify()

    # Fast paths.
    # data.display().verify()
    # data.verify()

    if not __xonsh__.env.get("KEEPALIVE"):
        infra.stop()


if __name__ == "__main__":
    main()
