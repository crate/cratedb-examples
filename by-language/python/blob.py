"""
## About
Access CrateDB's BLOB store from the command-line.

## Usage

For convenient interactive use, define two environment variables.
When not defining `--url` or `CRATEDB_HTTP_URL`, the program will
connect to CrateDB at `crate@localhost:4200` by default.

Synopsis::

    # Define the HTTP URL to your CrateDB instance.
    export CRATEDB_HTTP_URL=https://username:password@cratedb.example.net:4200/

    # Define the BLOB container name.
    export CRATEDB_BLOB_CONTAINER=testdrive

    # Upload an item to the BLOB store.
    python blob.py upload /path/to/file
    418a0143404fb2da8a1464ab721f6d5fb50c3b96

    # Download an item from the BLOB store.
    python blob.py download 418a0143404fb2da8a1464ab721f6d5fb50c3b96

Full command line example, without defining environment variables::

    python blob.py \
        --url=http://crate@localhost:4200/ --container=testdrive \
        upload /path/to/file

## References

- https://cratedb.com/docs/python/en/latest/blobs.html
- https://cratedb.com/docs/crate/reference/en/latest/general/blobs.html
- https://cratedb.com/docs/crate/reference/en/latest/sql/statements/create-blob-table.html
"""
import io
import logging
import os
import sys
import typing as t
from argparse import ArgumentError, ArgumentParser
from pathlib import Path

from crate import client
from crate.client.blob import BlobContainer
from crate.client.connection import Connection
from crate.client.exceptions import ProgrammingError

logger = logging.getLogger(__name__)


class CrateDbBlobContainer:
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name
        self.connection: Connection = None
        self.container: BlobContainer = None

    def connect(self):
        self.connection = client.connect(self.url)
        self.provision()
        self.container = self.connection.get_blob_container(self.name)

    def disconnect(self):
        self.connection.close()

    def upload(self, payload: t.Union[bytes, bytearray]) -> str:
        """
        Upload an item to the BLOB store.

        - https://cratedb.com/docs/python/en/latest/blobs.html#upload-blobs
        - https://cratedb.com/docs/crate/reference/en/5.4/general/blobs.html#uploading
        """
        file = io.BytesIO(payload)
        return self.container.put(file)

    def download(self, digest: str) -> bytes:
        """
        Download an item from the BLOB store.

        - https://cratedb.com/docs/python/en/latest/blobs.html#retrieve-blobs
        - https://cratedb.com/docs/crate/reference/en/5.4/general/blobs.html#downloading
        """

        payload = b""

        for chunk in self.container.get(digest):
            payload += chunk

        return payload

    def delete(self, digest: str) -> bool:
        """
        Delete an item from the BLOB store.
        """
        return self.container.delete(digest)

    def provision(self):
        """
        Create a new table for storing Binary Large Objects (BLOBs).

        - https://cratedb.com/docs/crate/reference/en/latest/sql/statements/create-blob-table.html
        """
        try:
            self.run_sql(f'CREATE BLOB TABLE "{self.name}";')
        except ProgrammingError as ex:
            if "RelationAlreadyExists" not in ex.message:
                raise

    def refresh(self):
        """
        Optionally synchronize data after write operations.
        """
        self.run_sql(f'REFRESH TABLE "{self.name}";')

    def run_sql(self, sql: str):
        """
        Run SQL statements on the connection.
        """
        return self.connection.cursor().execute(sql)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *excs):
        self.disconnect()


def setup_logging(level=logging.INFO):
    """
    What the function name says.
    """
    log_format = "%(asctime)-15s [%(name)-10s] %(levelname)-8s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


def truncate(value: bytes) -> bytes:
    """
    Truncate long string.

    https://stackoverflow.com/a/2873416
    """
    ellipsis_ = b"..."
    maxlength = 100
    strlength = maxlength - len(ellipsis_)
    return value[:strlength] + (value[strlength:] and ellipsis_)


def example(url: str, container_name: str):
    """
    An example conversation with the BLOB store (upload, download, delete).
    """

    # Define arbitrary content for testing purposes.
    content = "An example payload.".encode("utf-8")
    # content = b"\xde\xad\xbe\xef" * 256

    # Upload and re-download content payload.
    logger.info(f"Uploading: {truncate(content)!r}")
    with CrateDbBlobContainer(url=url, name=container_name) as container:
        identifier = container.upload(content)
        logger.info(f"Identifier: {identifier}")

        downloaded = container.download(identifier)
        logger.info(f"Downloaded: {truncate(downloaded)!r}")

        deleted = container.delete(identifier)
        logger.info(f"Deleted: {deleted}")


def read_arguments():
    parser = ArgumentParser()
    url = parser.add_argument("-u", "--url", type=str)
    container = parser.add_argument("-c", "--container", type=str)

    actions = parser.add_subparsers(
        dest="action",
        title="action",
        description="valid subcommands",
        help="additional help",
    )
    upload = actions.add_parser("upload", aliases=["up", "put"])
    download = actions.add_parser("download", aliases=["down", "get"])
    delete = actions.add_parser("delete", aliases=["del", "rm"])

    path = upload.add_argument("path", type=Path)
    download.add_argument("digest", type=str)
    delete.add_argument("digest", type=str)

    parser.set_defaults(
        url=os.environ.get("CRATEDB_HTTP_URL", "http://crate@localhost:4200/")
    )
    parser.set_defaults(container=os.environ.get("CRATEDB_BLOB_CONTAINER"))

    args = parser.parse_args()

    if not args.url:
        raise ArgumentError(
            url,
            "URL to database not given or empty. "
            "Use `--url` or `CRATEDB_HTTP_URL` environment variable",
        )

    if not args.container:
        raise ArgumentError(
            container,
            "BLOB container name not given or empty. "
            "Use `--container` or `CRATEDB_BLOB_CONTAINER` environment variable",
        )

    if not args.action:
        raise ArgumentError(
            actions, "Action not given: Use one of {upload,download,delete}"
        )

    if args.action == "upload" and not args.path.exists():
        raise ArgumentError(path, f"Path does not exist: {args.path}")

    if args.action in ["download", "delete"] and not args.digest:
        raise ArgumentError(path, "BLOB digest not given")

    return args


def main():
    args = read_arguments()
    with CrateDbBlobContainer(url=args.url, name=args.container) as container:
        if args.action == "upload":
            payload = args.path.read_bytes()
            logger.info(f"Upload: {truncate(payload)!r}")
            digest = container.upload(payload)
            print(digest)
        elif args.action == "download":
            payload = container.download(args.digest)
            sys.stdout.buffer.write(payload)
        elif args.action == "delete":
            container.delete(args.digest)
        else:
            raise KeyError(f"Action not implemented: {args.action}")


def run_example():
    example(
        url="http://crate@localhost:4200/",
        container_name="testdrive",
    )


if __name__ == "__main__":
    setup_logging()
    # run_example()
    main()
