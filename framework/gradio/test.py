import logging
import shlex
import subprocess
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest
from gradio_client import Client


logger = logging.getLogger()

GRADIO_SERVER_PORT = "7861"
GRADIO_API_URL = f"http://localhost:{GRADIO_SERVER_PORT}"


def run(command: str, env=None, timeout: int = None):
    """
    Invoke a command in a subprocess.
    """
    env = env or {}
    env["PATH"] = ""
    subprocess.call(shlex.split(command), env=env, timeout=timeout)


def check_url(url):
    """
    Check if a service is reachable.

    Makes a simple GET request to path of the HTTP endpoint. Service is
    available if returned status code is < 500.
    """
    try:
        r = urlopen(url)
        return r.code < 500
    except HTTPError as e:
        # If service returns e.g. a 404 it's ok
        return e.code < 500
    except Exception:
        # Possible service not yet started
        return False


@pytest.fixture(scope="session", autouse=True)
def run_server():

    def server_thread():
        print("sys.exec:", sys.executable)
        try:
            run(f"{sys.executable} basic_sys_summits.py", env={"GRADIO_SERVER_PORT": GRADIO_SERVER_PORT}, timeout=5)
        except subprocess.TimeoutExpired:
            pass

    thread = threading.Thread(target=server_thread)
    try:
        thread.start()
    except KeyboardInterrupt:
        pass

    while not check_url(GRADIO_API_URL):
        logger.info("Waiting for Gradio API to come up")
        time.sleep(0.2)


def test_read_sys_summits():
    """
    Verify reading CrateDB's built-in `sys.summits` database table through the Gradio API.

    - https://www.gradio.app/guides/getting-started-with-the-python-client
    - https://www.gradio.app/docs/python-client/
    - https://www.gradio.app/docs/gradio/dataframe
    """

    # Connect to Gradio API, and submit a request.
    client = Client(GRADIO_API_URL)
    result = client.predict(api_name="/predict")

    # Verify result.
    assert "mountain" in result["value"]["headers"]
    assert len(result["value"]["data"]) > 80
    assert result["value"]["data"][0][5] == "Mont Blanc"
