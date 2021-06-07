using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Npgsql;
using NpgsqlTypes;

namespace demo
{
    public static class DemoProgram
    {
        private static async Task SystemQueryExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running SystemQueryExample");
            await using (var cmd = new NpgsqlCommand("SELECT mountain FROM sys.summits ORDER BY 1 LIMIT 25", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var mountains = new List<string>();
                while (reader.Read())
                {
                    mountains.Add(reader.GetString(0));
                }

                Console.WriteLine($"Mountains: {string.Join(",", mountains)}");
            }

            Console.WriteLine();
        }

        private static async Task BasicConversationExample(NpgsqlConnection conn)
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
            using (var cmd = new NpgsqlCommand("INSERT INTO testdrive.basic (x) VALUES (@x)", conn))
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
            await using (var cmd = new NpgsqlCommand("SELECT x FROM testdrive.basic ORDER BY 1 ASC LIMIT 10", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                while (await reader.ReadAsync())
                    Console.WriteLine(reader.GetInt32(0));
            }

            Console.WriteLine();
        }

        private static async Task AsyncUnnestExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running AsyncUnnestExample");

            // Submit DDL, create database schema.
            await using (var cmd = new NpgsqlCommand("DROP TABLE IF EXISTS testdrive.unnest", conn))
            {
                await cmd.ExecuteNonQueryAsync();
            }
            await using var cmd2 = new NpgsqlCommand(
                connection: conn,
                cmdText: "CREATE TABLE IF NOT EXISTS testdrive.unnest (id int, name text)"
            );
            await cmd2.ExecuteNonQueryAsync();

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
            await using (var cmd = new NpgsqlCommand("SELECT COUNT(*) FROM testdrive.unnest", conn))
            {
                await using (var reader = cmd.ExecuteReader())
                {
                    await reader.ReadAsync();
                    Console.WriteLine($"Wrote {reader.GetInt32(0)} records");
                }
            }

            Console.WriteLine();
        }

        public static async Task Main(string[] args)
        {
            var host = args[0];
            var port = args[1];

            var connString = $"Host={host};Port={port};Username=crate;Password=;Database=testdrive";
            Console.WriteLine($"Connecting to {connString}\n");
            await using (var conn = new NpgsqlConnection(connString))
            {
                conn.Open();
                await SystemQueryExample(conn);
                await BasicConversationExample(conn);
                await AsyncUnnestExample(conn);
                conn.Close();
            }
        }
    }
}