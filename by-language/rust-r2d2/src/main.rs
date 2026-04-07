use std::time::Duration;

use postgres::{NoTls, Row};
use r2d2_postgres::{
    r2d2::{Pool},
    PostgresConnectionManager,
};

#[cfg(test)]
mod tests;

fn main() -> Result<(), Box<dyn std::error::Error>> {

    // Connect to database.
    let pg_manager = PostgresConnectionManager::new(
        "postgresql://crate:crate@localhost:5432/?sslmode=disable"
            .parse()
            .unwrap(),
        NoTls,
    );
    let pg_pool = Pool::builder()
        .max_size(5)
        .connection_timeout(Duration::from_secs(2))
        .build(pg_manager)
        .expect("Postgres pool failed");
    let mut pg_conn = pg_pool.get().unwrap();

    // Invoke query.
    let result = pg_conn.query("SELECT mountain, height FROM sys.summits ORDER BY height DESC LIMIT 3", &[]);
    let rows = result.unwrap().into_iter().collect::<Vec<Row>>();

    // Display results.
    for row in rows {
        let mountain: &str = row.get(0);
        let height: i32 = row.get(1);
        println!("{}: {}", mountain, height);
    }
    Ok(())
}
