# Connect to CrateDB using SSL, with host name verification turned off.

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "psycopg[binary]",
# ]
# ///
import psycopg


def main():
    connection = psycopg.connect("postgresql://crate@localhost:5432/?sslmode=require")
    with connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        cursor.execute("SELECT 42")
        result = cursor.fetchall()
        print(result)
    connection.close()


if __name__ == "__main__":
    main()
