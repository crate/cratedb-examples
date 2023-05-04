<?php
/*
 * How to connect to CrateDB's PostgreSQL interface using PHP PDO (PDO_PGSQL).
 *
 * https://www.php.net/manual/en/ref.pdo-pgsql.php
 * https://www.php.net/manual/en/ref.pdo-pgsql.connection.php
 *
 * Prerequisites:
 *
 *  docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate:latest
 *
 * Synopsis:
 *
 *  # Connect to CrateDB on localhost.
 *  php basic.php 'pgsql:host=localhost;port=5432;user=crate'
 *
 *  # Connect to CrateDB Cloud.
 *  php basic.php 'pgsql:host=example.aks1.eastus2.azure.cratedb.net;port=5432;user=admin;password=<PASSWORD>'
 */

declare(strict_types=1);

error_reporting(E_ALL);


function print_header($title)
{
    print("\n");
    $armor = str_repeat("=", strlen($title));
    print("$armor\n");
    print("$title\n");
    print("$armor\n");
}


class DatabaseWorkload
{
    /**
     * @var string
     */
    private $dsn;

    function __construct(string $dsn)
    {
        $this->dsn = $dsn;
    }

    function ddl_dml_dql() {

        print_header("Run DDL, DML, and DQL statements subsequently");

        // Connect to CrateDB's PostgreSQL interface.
        $connection = new PDO($this->dsn);

        // Create database table.
        $connection->exec("DROP TABLE IF EXISTS testdrive");
        $connection->exec("CREATE TABLE testdrive (id INTEGER, name STRING, int_type INTEGER)");

        // Insert data.
        $statement = $connection->prepare('INSERT INTO testdrive (id, name, int_type) VALUES (?, ?, ?)');
        $statement->execute([5, 'foo', 1]);
        $statement->execute([6, 'bar', 2]);

        // Evaluate insert response.
        print("Total count: {$statement->rowCount()}\n");
        $response = $statement->fetchAll(PDO::FETCH_NUM);
        print_r($response);

        // Synchronize data.
        $connection->query("REFRESH TABLE testdrive");

        // Query data.
        $cursor = $connection->query("SELECT * FROM testdrive");
        print_r($cursor->fetchAll(PDO::FETCH_ASSOC));

        // Disconnect from database.
        // https://www.php.net/manual/en/pdo.connections.php
        // https://stackoverflow.com/questions/18277233/pdo-closing-connection
        $statement = null;
        $connection = null;
    }

}


function get_dsn_from_cli()
{
    global $argc, $argv;
    if ($argc != 2) {
        echo <<<"MESSAGE"
ERROR: Please provide a PHP PDO connection DSN as single command-line argument. Example:

    php basic.php 'pgsql:host=localhost;port=5432;user=crate'

MESSAGE;
        exit(1);
    }
    return $argv[1];
}


// Run only when invoked as a program.
if (!debug_backtrace())
{
    $dsn = get_dsn_from_cli();
    $work = new DatabaseWorkload($dsn);
    $work->ddl_dml_dql();
}
