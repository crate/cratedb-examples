<?php
/*
 * How to connect to CrateDB's PostgreSQL interface using AMPHP's PostgreSQL driver.
 * It is an asynchronous PostgreSQL client for PHP based on Amp.
 *
 * https://amphp.org/
 * https://github.com/amphp/postgres
 *
 * Prerequisites:
 *
 *  docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate:latest
 *  composer install
 *
 * Synopsis:
 *
 *  # Connect to CrateDB on localhost.
 *  php basic.php 'host=localhost port=5432 user=crate'
 *
 *  # Connect to CrateDB Cloud.
 *  php basic.php 'host=example.aks1.eastus2.azure.cratedb.net port=5432 user=admin password=<PASSWORD>'
 *
 */

declare(strict_types=1);

error_reporting(E_ALL);

require __DIR__ . '/vendor/autoload.php';

use Amp\Postgres;
use Revolt\EventLoop;


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

    function show_all_settings()
    {

        print_header("Display all settings using `SHOW ALL`");

        EventLoop::run(function () {

            // Connect to CrateDB's PostgreSQL interface.
            $config = Postgres\ConnectionConfig::fromString($this->dsn);
            /** @var Postgres\Connection $connection */
            $connection = yield Postgres\connect($config);

            // Query data.
            /** @var Postgres\ResultSet $result */
            $result = yield $connection->query('SHOW ALL');

            // Print results.
            while (yield $result->advance()) {
                $row = $result->getCurrent();
                \printf("%-35s = %s (%s)\n", $row['name'], $row['setting'], $row['description']);
            }

            // Close connection to database.
            $connection->close();
        });
    }

    function ddl_dml_dql()
    {

        print_header("Run DDL, DML, and DQL statements subsequently");

        EventLoop::run(function () {

            // Connect to CrateDB's PostgreSQL interface.
            $config = Postgres\ConnectionConfig::fromString($this->dsn);
            /** @var Postgres\Connection $connection */
            $connection = yield Postgres\connect($config);

            // Create database table.
            yield $connection->execute("DROP TABLE IF EXISTS testdrive");
            yield $connection->execute("CREATE TABLE testdrive (id INTEGER, name STRING, int_type INTEGER)");

            // Insert data.
            $statement = yield $connection->prepare('INSERT INTO testdrive (id, name, int_type) VALUES (?, ?, ?)');
            /** @var Postgres\PgSqlCommandResult $result */
            $result = yield $statement->execute([5, 'foo', 1]);
            $result = yield $statement->execute([6, 'bar', 2]);

            // Evaluate most recent insert response.
            print("Record count: {$result->getAffectedRowCount()}\n");

            // Synchronize data.
            $connection->query("REFRESH TABLE testdrive");

            // Query data.
            /** @var Postgres\ResultSet $result */
            $result = yield $connection->query("SELECT * FROM testdrive");

            // Print results.
            /** @var Result $result */
            while (yield $result->advance()) {
                $row = $result->getCurrent();
                print_r($row);
            }

            // Close connection to database.
            $connection->close();

        });

    }


    function use_pool()
    {

        print_header("Using a connection pool");

        EventLoop::run(function () {

            // Connect to CrateDB's PostgreSQL interface, using a connection pool.
            $config = Postgres\ConnectionConfig::fromString($this->dsn);
            /** @var Postgres\Pool $connection */
            $connection = Postgres\pool($config);

            // Query data.
            /** @var Postgres\ResultSet $result */
            $result = yield $connection->query('SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3');

            // Print results.
            while (yield $result->advance()) {
                $row = $result->getCurrent();
                print_r($row);
            }

            // Close connection to database.
            $connection->close();

        });

    }

}


function get_dsn_from_cli()
{
    global $argc, $argv;
    if ($argc != 2) {
        echo <<<"MESSAGE"
ERROR: Please provide a database connection string as single command-line argument. Example:

    php basic.php "host=localhost port=5432 user=crate"

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
    $work->show_all_settings();
    $work->ddl_dml_dql();
    $work->use_pool();
}
