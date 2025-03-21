use postgres::{Client, NoTls};
use std::env;

mod tests;

pub fn main() {

    // Read port number from command-line arguments.
    // Use port 5432 by default.
    let mut args: Vec<String> = env::args().collect();
    if args.len() == 1 {
        args.push("5432".to_string());
    }

    // Connect to database.
    let mut client = Client::connect(format!("host=localhost port={} user=crate", &args[1]).as_str(), NoTls).unwrap();

    // Submit DDL.
    client
        .simple_query("DROP TABLE IF EXISTS testdrive.rust;")
        .unwrap();
    client
        .simple_query("CREATE TABLE testdrive.rust (id int primary key, x int not null, name text not null);")
        .unwrap();

    // Submit basic INSERT statement.
    client
        .execute(
            "INSERT INTO testdrive.rust (id, x, name) VALUES (1, 10, 'Arthur')",
            &[],
        )
        .unwrap();

    // Submit prepared INSERT statement.
    let stmt = match client
        .prepare("INSERT INTO testdrive.rust (id, x, name) values ($1, $2, $3)") {
            Ok(stmt) => stmt,
            Err(e) => {
                println!("Preparing insert failed: {:?}", e);
                return;
            }
        };
    let id = 2;
    let x = 20;
    let name = "Trillian";
    client.execute(&stmt, &[&id, &x, &name]).unwrap();

    // Synchronize writes.
    client.execute("REFRESH TABLE testdrive.rust", &[]).unwrap();

    // Query records.
    for row in client.query("SELECT id, x, name FROM testdrive.rust", &[]).unwrap() {
        let id: i32 = row.get("id");
        let x: i32 = row.get("x");
        let name: &str = row.get("name");
        println!("id={} x={} name={}", &id, &x, &name);
        assert!(id == 1 || id == 2, "id = {} but should be 1 or 2", id);
    }
}
