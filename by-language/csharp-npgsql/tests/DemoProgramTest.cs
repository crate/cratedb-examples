using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
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
        public async Task TestSystemQueryExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = DatabaseWorkloads.SystemQueryExample(conn);
            var mountains = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Check results.
            Assert.Equal("Mont Blanc - 4808 - (6.86444,45.8325)", mountains[0]);
        }

        [Fact]
        public async Task TestBasicConversationExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = DatabaseWorkloads.BasicConversationExample(conn);
            var results = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Check results.
            Assert.Equal(new List<int>() { -999, 10, 20, 30, 40, 50, 60, 70, 80, 90 }, results);
        }

        [Fact]
        public async Task TestUnnestExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = DatabaseWorkloads.UnnestExample(conn);
            var resultCount = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Check results.
            Assert.Equal(10, resultCount);
        }

        [Fact]
        public async Task TestAllTypesExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = DatabaseWorkloadsMore.AllTypesExample(conn);
            var dt = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Check results.
            var row = dt.Rows[0];

            // Numeric types
            Assert.Equal(DBNull.Value, row["null_integer"]);
            Assert.Equal(42, row["integer"]);
            Assert.Equal((Int64) 42, row["bigint"]);
            Assert.Equal(42.42, (float) row["float"], 0.01);
            Assert.Equal(42.42, (double) row["double"], 0.01);
            Assert.Equal(new decimal(42.42), row["decimal"]);

            // Other scalar types
            Assert.Equal(new List<bool> { false, true, false, true, false, true, false, true }, row["bit"]);
            Assert.True((bool) row["bool"]);
            Assert.Equal("foobar", row["text"]);
            Assert.Equal("foo  ", row["char"]);
            Assert.Equal(DateTime.Parse("1970-01-01T23:00:00.0000000"), row["timestamp_tz"]);
            Assert.Equal(DateTime.Parse("1970-01-02T00:00:00"), row["timestamp_notz"]);
            Assert.Equal("127.0.0.1", row["ip"]);

            // Container types
            // FIXME: While doing conversations with ARRAY types works natively,
            //        it doesn't work for OBJECT types.
            //        Yet, they can be submitted as STRING in JSON format.
            Assert.Equal(new List<string>{"foo", "bar"}, row["array"]);
            Assert.Equal("""{"foo":"bar"}""", row["object"]);

            // Geospatial types
            // TODO: Unlock native data types?
            //       GEO_POINT and GEO_SHAPE types can be marshalled back and forth using STRING.
            //       GEO_POINT is using a tuple format, GEO_SHAPE is using the GeoJSON format.
            // Assert.Equal(new List<double>{85.43, 66.23}, row["geopoint"]);  // TODO
            Assert.Equal("(85.42999997735023,66.22999997343868)", row["geopoint"].ToString());  // FIXME
            Assert.Equal("""{"coordinates":[[[5.0,5.0],[5.0,10.0],[10.0,10.0],[10.0,5.0],[5.0,5.0]]],"type":"Polygon"}""", row["geoshape"]);

            // Vector type
            Assert.Equal((new List<double>{1.1, 2.2, 3.3}).Select(d => (float) d).ToArray(), row["float_vector"]);
        }

        [Fact]
        public async Task TestContainerTypesExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = DatabaseWorkloadsMore.ContainerTypesExample(conn);
            var dt = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Check results.
            var row = dt.Rows[0];
            // FIXME: While doing conversations with ARRAY types works natively,
            //        it doesn't work for OBJECT types.
            //        Yet, they can be submitted as STRING in JSON format.
            Assert.Equal(new List<string>{"foo", "bar"}, row["array"]);
            Assert.Equal("""{"foo":"bar"}""", row["object"]);

            // Run a special query indexing into ARRAY types.
            await using (var cmd = new NpgsqlCommand("""SELECT "array[2]" AS foo FROM testdrive.container""", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var dataTable = new DataTable();
                dataTable.Load(reader);
                Assert.Equal("bar", dataTable.Rows[0]["foo"]);
            }

            // Run a special query indexing into OBJECT types.
            await using (var cmd = new NpgsqlCommand("""SELECT "object['foo']" AS foo FROM testdrive.container""", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var dataTable = new DataTable();
                dataTable.Load(reader);
                Assert.Equal("bar", dataTable.Rows[0]["foo"]);
            }

        }

    }
}
