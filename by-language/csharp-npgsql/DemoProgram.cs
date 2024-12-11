using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using CommandLine;
using Npgsql;
using NpgsqlTypes;

namespace demo
{
    public static class DemoProgram
    {
        public static async Task Main(string[] args)
        {
            await Parser.Default.ParseArguments<Options>(args)
                .WithParsedAsync<Options>(async options =>
                {
                    var connString = $"Host={options.Host};Port={options.Port};SSL Mode={options.SslMode};" +
                                     $"Username={options.Username};Password={options.Password};Database={options.Database}";
                    Console.WriteLine($"Connecting to {connString}\n");
                    await using var conn = new NpgsqlConnection(connString);
                    conn.Open();
                    await DatabaseWorkloads.SystemQueryExample(conn);
                    await DatabaseWorkloads.BasicConversationExample(conn);
                    await DatabaseWorkloads.UnnestExample(conn);
                    conn.Close();
                });

        }

        public class Options
        {
            [Option('h', "host", Required = false, HelpText = "Host name to connect to", Default = "localhost")]
            public string? Host { get; set; }

            [Option('p', "port", Required = false, HelpText = "Port number to connect to", Default = 5432)]
            public int Port { get; set; }

            // Controls whether SSL is used, depending on server support. Can be Require, Disable, or Prefer.
            // https://www.npgsql.org/doc/connection-string-parameters.html#security-and-encryption
            [Option('s', "ssl-mode", Required = false, HelpText = "Which SSL mode to use", Default = "Disable")]
            public string? SslMode { get; set; }

            [Option('u', "username", Required = false, HelpText = "Username to authenticate with", Default = "crate")]
            public string? Username { get; set; }
            [Option('w', "password", Required = false, HelpText = "Password to authenticate with", Default = "")]
            public string? Password { get; set; }
            [Option('d', "database", Required = false, HelpText = "Database to use", Default = "testdrive")]
            public string? Database { get; set; }
        }
        
    }

    public class DatabaseWorkloads
    {
        public static async Task<List<string>> SystemQueryExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running SystemQueryExample");
            var mountains = new List<string>();
            await using (var cmd = new NpgsqlCommand("SELECT mountain FROM sys.summits ORDER BY 1 LIMIT 25", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                while (await reader.ReadAsync())
                {
                    mountains.Add(reader.GetString(0));
                }

                Console.WriteLine($"Mountains: {string.Join(",", mountains)}");
            }

            Console.WriteLine();
            return mountains;
        }

        public static async Task<List<int>> BasicConversationExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running BasicConversationExample");
            
            // Submit DDL, create database schema.
            await using (var cmd = new NpgsqlCommand("DROP TABLE IF EXISTS testdrive.basic", conn))
            {
                cmd.ExecuteNonQuery();
            }

            await using (var cmd = new NpgsqlCommand("CREATE TABLE testdrive.basic (x int)", conn))
            {
                cmd.ExecuteNonQuery();
            }

            // Insert single data point.
            await using (var cmd = new NpgsqlCommand("INSERT INTO testdrive.basic (x) VALUES (@x)", conn))
            {
                cmd.Parameters.AddWithValue("x", -999);
                cmd.ExecuteNonQuery();
            }

            // Insert multiple data points.
            await using (var cmd = new NpgsqlCommand("INSERT INTO testdrive.basic (x) VALUES (@x)", conn))
            {
                await using (var transaction = conn.BeginTransaction())
                {
                    cmd.Transaction = transaction;
                    cmd.Parameters.Add("@x", NpgsqlDbType.Integer);

                    for (var i = 1; i < 10; i++)
                    {
                        cmd.Parameters["@x"].Value = i * 10;
                        cmd.ExecuteNonQuery();
                    }

                    transaction.Commit();
                }
            }

            // Flush data.
            await using (var cmd = new NpgsqlCommand("REFRESH TABLE testdrive.basic", conn))
            {
                cmd.ExecuteNonQuery();
            }

            // Query back data.
            var data = new List<int>();
            await using (var cmd = new NpgsqlCommand("SELECT x FROM testdrive.basic ORDER BY 1 ASC LIMIT 10", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                while (await reader.ReadAsync())
                {
                    var value = reader.GetInt32(0);
                    data.Add(value);
                    Console.WriteLine(value);
                }

            }

            Console.WriteLine();
            return data;
        }

        public static async Task<int> UnnestExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running AsyncUnnestExample");

            // Submit DDL, create database schema.
            await using (var cmd = new NpgsqlCommand("DROP TABLE IF EXISTS testdrive.unnest", conn))
            {
                await cmd.ExecuteNonQueryAsync();
            }

            await using (var cmd2 = new NpgsqlCommand(
                             connection: conn,
                             cmdText: "CREATE TABLE IF NOT EXISTS testdrive.unnest (id int, name text)"
                         ))
            {
                await cmd2.ExecuteNonQueryAsync();
            }

            // Insert multiple data points.
            var records = Enumerable
                .Range(0, 10)
                .Select(i => (Id: i, Name: $"My identifier is {i}"))
                .ToArray();
            var cmd3 = new NpgsqlCommand();
            cmd3.Connection = conn;
            cmd3.CommandText = "INSERT INTO testdrive.unnest (id, name) SELECT * FROM UNNEST(@i, @n) AS d";
            cmd3.Parameters.Add(new NpgsqlParameter<int[]>("i", records.Select(e => e.Id).ToArray()));
            cmd3.Parameters.Add(new NpgsqlParameter<string[]>("n", records.Select(e => e.Name).ToArray()));
            await cmd3.ExecuteNonQueryAsync();

            // Flush data.
            await using (var cmd = new NpgsqlCommand("REFRESH TABLE testdrive.unnest", conn))
            {
                cmd.ExecuteNonQuery();
            }

            // Query back data.
            var resultCount = -1;
            await using (var cmd = new NpgsqlCommand("SELECT COUNT(*) FROM testdrive.unnest", conn))
            {
                await using (var reader = cmd.ExecuteReader())
                {
                    await reader.ReadAsync();
                    resultCount = reader.GetInt32(0);
                    Console.WriteLine($"Wrote {resultCount} records");
                }
            }

            Console.WriteLine();
            return resultCount;
        }

    }
}