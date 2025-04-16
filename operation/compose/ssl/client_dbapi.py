# Connect to CrateDB using SSL, with host name verification turned off.

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "crate",
# ]
# ///
from crate import client


def main():
    connection = client.connect("https://localhost:4200", verify_ssl_cert=False)
    cursor = connection.cursor()
    cursor.execute("SELECT 42")
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    print(results)


if __name__ == "__main__":
    main()

