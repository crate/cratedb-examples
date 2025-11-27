using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using GeoJSON.Net.Geometry;
using Npgsql;
using NpgsqlTypes;
using Xunit;

namespace demo.tests
{

    public class DatabaseFixture : IDisposable
    {
        public NpgsqlDataSource Source { get; private set; }
        public NpgsqlConnection Db { get; private set; }

        public DatabaseFixture()
        {
            var CRATEDB_DSN = Environment.GetEnvironmentVariable("CRATEDB_DSN");
            if (CRATEDB_DSN == null)
            {
                CRATEDB_DSN = $"Host=localhost;Port=5432;Username=crate;Password=;Database=testdrive";
            }
            Source = DemoProgram.GetDataSource(CRATEDB_DSN);
            Db = Source.OpenConnection();
        }

        public void Dispose()
        {
            Db.Close();
            Source.Dispose();
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
        public async Task TestAllTypesNativeExample()
        {
            var conn = fixture.Db;

            // Provision data.
            var task = new DatabaseWorkloadsTypes(conn).AllTypesNativeExample();
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
            Assert.Equal(new List<string>{"foo", "bar"}, row["array"]);
            Assert.Equal("""{"foo":"bar"}""", row["object"]);

            // Note: While it works on the ingress side to communicate `Dictionary` types,
            //       this kind of equality check does not work on the egress side,
            //       presenting an error that indicates a different internal representation,
            //       or a programming error ;].
            //
            //       Expected: [["foo"] = "bar"]
            //       Actual:   {"foo":"bar"}
            // Assert.Equal(new Dictionary<string, string>{{"foo", "bar"}}, row["object"]);

            // Geospatial types
            // While `GEO_POINT` is transparently marshalled as `NpgsqlPoint`,
            // `GEO_SHAPE` is communicated as scalar `string` type, using the GeoJSON format.
            // TODO: Possibly support transparently converging `GEO_SHAPE` to one of
            //       `NpgsqlLSeg`, `NpgsqlBox`, `NpgsqlPath`, `NpgsqlPolygon`, `NpgsqlCircle`.
            Assert.Equal(new NpgsqlPoint(85.42999997735023, 66.22999997343868), row["geopoint"]);
            Assert.Equal("""{"coordinates":[[[5.0,5.0],[5.0,10.0],[10.0,10.0],[10.0,5.0],[5.0,5.0]]],"type":"Polygon"}""", row["geoshape"]);

            // Vector type
            Assert.Equal((new List<double>{1.1, 2.2, 3.3}).Select(d => (float) d).ToArray(), row["float_vector"]);
        }

        [Fact]
        public async Task TestContainerTypesExample()
        {
            var conn = fixture.Db;

            // Provision data.
            var task = new DatabaseWorkloadsTypes(conn).AllTypesNativeExample();
            await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Run an SQL query indexing into ARRAY types.
            await using (var cmd = new NpgsqlCommand("""SELECT "array[2]" AS foo FROM testdrive.example""", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var dataTable = new DataTable();
                dataTable.Load(reader);
                Assert.Equal("bar", dataTable.Rows[0]["foo"]);
            }

            // Run an SQL query indexing into OBJECT types.
            await using (var cmd = new NpgsqlCommand("""SELECT "object['foo']" AS foo FROM testdrive.example""", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var dataTable = new DataTable();
                dataTable.Load(reader);
                Assert.Equal("bar", dataTable.Rows[0]["foo"]);
            }

        }

        [Fact]
        public async Task TestObjectJsonDocumentExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = new DatabaseWorkloadsTypes(conn).ObjectJsonDocumentExample();
            var obj = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Validate the outcome.
            Assert.Equal("""{"foo":"bar"}""", JsonSerializer.Serialize(obj));
        }

        [Fact]
        public async Task TestObjectPocoExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = new DatabaseWorkloadsTypes(conn).ObjectPocoExample();
            var obj = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Validate the outcome.
            Assert.Equal(new BasicPoco { name = "Hotzenplotz" }, obj);

        }

        [Fact]
        public async Task TestArrayPocoExample()
        {
            var conn = fixture.Db;

            // Invoke database workload.
            var task = new DatabaseWorkloadsTypes(conn).ArrayPocoExample();
            var obj = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Validate the outcome.
            var reference = new List<BasicPoco>
            {
                new BasicPoco { name = "Hotzenplotz" },
                new BasicPoco { name = "Petrosilius", age = 42 },
            };
            Assert.Equal(reference, obj);

        }

        [Fact]
        public async Task TestGeoJsonTypesExample()
        {
            var conn = fixture.Db;

            // Provision data.
            var task = new DatabaseWorkloadsTypes(conn).GeoJsonTypesExample();
            var point = await task.WaitAsync(TimeSpan.FromSeconds(0.5));

            // Validate the outcome.
            var coords = new Point(new Position(85.43, 66.23)).Coordinates;
            Assert.Equal(coords.Latitude, point?.Coordinates.Latitude);
            Assert.Equal(coords.Longitude, point?.Coordinates.Longitude);

        }

    }
}
