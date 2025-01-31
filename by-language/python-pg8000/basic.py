import ssl

import pg8000

# When connecting to CrateDB Cloud you may want to use SSL
# ssl_context = ssl.create_default_context()

conn = pg8000.connect(
    user="crate",
    password="",
    host="localhost",
    port=5432,
    database="doc",
    # ssl_context=ssl_context,
)

query = """
    SELECT mountain,height
    FROM sys.summits
    WHERE height >= :minimum_height
    ORDER BY height DESC
    LIMIT :number_of_rows;
"""

ps = conn.prepare(query)
ps.run(minimum_height=4000, number_of_rows=10)
