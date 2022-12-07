using System;
using System.Collections.Generic;
using Npgsql;
using Xunit;

namespace demo.tests
{
    
    public class DatabaseFixture : IDisposable
    {
        public NpgsqlConnection Db { get; private set; }

        public DatabaseFixture()
        {
            var CRATEDB_DSN = Environment.GetEnvironmentVariable("CRATEDB_DSN");
            if (CRATEDB_DSN == null)
            {
                CRATEDB_DSN = $"Host=localhost;Port=5432;Username=crate;Password=;Database=testdrive";
            }
            Console.WriteLine($"Connecting to {CRATEDB_DSN}\n");
            Db = new NpgsqlConnection(CRATEDB_DSN);
            Db.Open();
        }

        public void Dispose()
        {
            Db.Close();
        }

    }
    
    public class DemoProgramTest : IClassFixture<DatabaseFixture>
    {
        
        DatabaseFixture fixture;
        DatabaseWorkloads program = new DatabaseWorkloads();

        public DemoProgramTest(DatabaseFixture fixture)
        {
            this.fixture = fixture;
        }

        [Fact]
        public void TestSystemQueryExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = program.SystemQueryExample(conn);
            task.Wait();

            // Check results.
            var mountains = task.Result;
            Assert.Equal("Acherkogel", mountains[0]);
        }

        [Fact]
        public void TestBasicConversationExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = program.BasicConversationExample(conn);
            task.Wait();

            // Check results.
            var results = task.Result;
            Assert.Equal(new List<int>() { -999, 10, 20, 30, 40, 50, 60, 70, 80, 90 }, results);
        }

        [Fact]
        public void TestAsyncUnnestExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = program.AsyncUnnestExample(conn);
            task.Wait();

            // Check results.
            var resultCount = task.Result;
            Assert.Equal(10, resultCount);
        }
        
    }
}
