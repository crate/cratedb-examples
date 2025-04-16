# Connect to CrateDB using SSL, with host name verification turned off.

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "sqlalchemy-cratedb>=0.42.0.dev2",
# ]
# ///
import sqlalchemy as sa


def main():
    engine = sa.create_engine("crate://localhost/?sslmode=require")
    with engine.connect() as connection:
        results = connection.execute(sa.text("SELECT 42;"))
        print(results.fetchall())


if __name__ == "__main__":
    main()
