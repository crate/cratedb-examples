#nullable enable
using System;
using System.Collections.Generic;
using System.Data;
using System.Text.Json;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Npgsql;
using NpgsqlTypes;

namespace demo
{

    public class AllTypesRecord
    {
        [JsonProperty("null_integer", NullValueHandling = NullValueHandling.Ignore)]
        public int? NullInteger { get; set; }
        [JsonProperty("integer")]
        public int? Integer { get; set; }
        [JsonProperty("bigint")]
        public long? Bigint { get; set; }
        [JsonProperty("float")]
        public float? Float { get; set; }
        [JsonProperty("double")]
        public double? Double { get; set; }
        [JsonProperty("decimal")]
        public decimal? Decimal { get; set; }
        // TODO: Review the handling of the `BIT` type here.
        //[JsonProperty("bit")]
        //public BitArray Bit { get; set; }
        [JsonProperty("bool")]
        public bool? Bool { get; set; }
        [JsonProperty("text")]
        public string? Text { get; set; }
        [JsonProperty("char")]
        public string? Char { get; set; }
        [JsonProperty("timestamp_tz")]
        public string? Timestamp { get; set; }
        [JsonProperty("timestamp_notz")]
        public string? TimestampNoTz { get; set; }
        [JsonProperty("ip")]
        public string? Ip { get; set; }

        [JsonProperty("array")]
        public IList<string>? Array { get; set; }
        [JsonProperty("object")]
        public Dictionary<string, string>? Object { get; set; }
        [JsonProperty("geopoint")]
        public Dictionary<string, double>? Geopoint { get; set; }
        [JsonProperty("geoshape")]
        public Dictionary<string, string>? Geoshape { get; set; }
        [JsonProperty("float_vector")]
        public IList<string>? FloatVector { get; set; }
    }

    public class DatabaseWorkloadsTypes
    {

        public DatabaseWorkloadsTypes(NpgsqlConnection conn)
        {
            this.conn = conn;
        }
        
        private NpgsqlConnection conn;

        public async Task CreateTable()
        {
            Console.WriteLine("Running CreateTable");

            // Submit DDL, create database schema.
            await using (var cmd = new NpgsqlCommand("DROP TABLE IF EXISTS testdrive.example", conn))
            {
                cmd.ExecuteNonQuery();
            }

            await using (var cmd = new NpgsqlCommand("""
                CREATE TABLE testdrive.example (
                    -- Numeric types
                    null_integer INT,
                    integer INT,
                    bigint BIGINT,
                    float FLOAT,
                    double DOUBLE,
                    decimal DECIMAL(8, 2),
                    -- Other scalar types
                    bit BIT(8),
                    bool BOOLEAN,
                    text TEXT,
                    char CHARACTER(5),
                    timestamp_tz TIMESTAMP WITH TIME ZONE,
                    timestamp_notz TIMESTAMP WITHOUT TIME ZONE,
                    ip IP,
                    -- Container types
                    "array" ARRAY(STRING),
                    "object" OBJECT(DYNAMIC),
                    "array_object" ARRAY(OBJECT(DYNAMIC)),
                    -- Geospatial types
                    geopoint GEO_POINT,
                    geoshape GEO_SHAPE,
                    -- Vector type
                    float_vector FLOAT_VECTOR(3)
                );
            """, conn))
            {
                cmd.ExecuteNonQuery();
            }
        }

        public async Task InsertRecord()
        {
            Console.WriteLine("Running InsertRecord");

            // Insert single data point.
            await using (var cmd = new NpgsqlCommand("""
            INSERT INTO testdrive.example (
                null_integer,
                integer,
                bigint,
                float,
                double,
                decimal,
                bit,
                bool,
                text,
                char,
                timestamp_tz,
                timestamp_notz,
                ip,
                "array",
                "object",
                geopoint,
                geoshape,
                float_vector
            ) VALUES (
                @null_integer,
                @integer,
                @bigint,
                @float,
                @double,
                @decimal,
                @bit,
                @bool,
                @text,
                @char,
                @timestamp_tz,
                @timestamp_notz,
                @ip,
                @array,
                @object,
                @geopoint,
                @geoshape,
                @float_vector
            );
            """, conn))
            {
                cmd.Parameters.AddWithValue("null_integer", DBNull.Value);
                cmd.Parameters.AddWithValue("integer", 42);
                cmd.Parameters.AddWithValue("bigint", 42);
                cmd.Parameters.AddWithValue("float", 42.42);
                cmd.Parameters.AddWithValue("double", 42.42);
                cmd.Parameters.AddWithValue("decimal", 42.42);
                cmd.Parameters.AddWithValue("bit", "01010101");
                cmd.Parameters.AddWithValue("bool", true);
                cmd.Parameters.AddWithValue("text", "foobar");
                cmd.Parameters.AddWithValue("char", "foo");
                cmd.Parameters.AddWithValue("timestamp_tz", "1970-01-02T00:00:00+01:00");
                cmd.Parameters.AddWithValue("timestamp_notz", "1970-01-02T00:00:00");
                cmd.Parameters.AddWithValue("ip", "127.0.0.1");

                // Container types
                cmd.Parameters.AddWithValue("array", NpgsqlDbType.Json, new List<string>{"foo", "bar"});
                cmd.Parameters.AddWithValue("object", NpgsqlDbType.Json, new Dictionary<string, string>{{"foo", "bar"}});

                // Geospatial types

                // GEO_POINT
                // Alternatively to `NpgsqlPoint`, you can also use `List<double>{85.43, 66.23}`.
                cmd.Parameters.AddWithValue("geopoint", new NpgsqlPoint(85.43, 66.23));

                // GEO_SHAPE
                // While `GEO_POINT` is transparently marshalled as `NpgsqlPoint`,
                // `GEO_SHAPE` is communicated as scalar `string` type, using WKT or GeoJSON format.
                // TODO: Possibly support transparently converging `GEO_SHAPE` to one of
                //       `NpgsqlLSeg`, `NpgsqlBox`, `NpgsqlPath`, `NpgsqlPolygon`, `NpgsqlCircle`.
                cmd.Parameters.AddWithValue("geoshape", "POLYGON ((5 5, 10 5, 10 10, 5 10, 5 5))");

                // Vector type
                cmd.Parameters.AddWithValue("float_vector", new List<double> {1.1, 2.2, 3.3});

                cmd.ExecuteNonQuery();
            }

            await RefreshTable();

        }

        public async Task RefreshTable()
        {
            // Flush data.
            await using (var cmd = new NpgsqlCommand("REFRESH TABLE testdrive.example", conn))
            {
                cmd.ExecuteNonQuery();
            }
        }

        public async Task<DataTable> AllTypesNativeExample()
        {
            Console.WriteLine("Running AllTypesNativeExample");

            // Provision data.
            await CreateTable();
            await InsertRecord();

            // Query back data.
            await using (var cmd = new NpgsqlCommand("SELECT * FROM testdrive.example", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var dataTable = new DataTable();
                dataTable.Load(reader);
                var payload = JsonConvert.SerializeObject(dataTable);
                Console.WriteLine(payload);
                return (DataTable) dataTable;
            }

        }

        public async Task<JsonDocument> ObjectJsonDocumentExample()
        {
            Console.WriteLine("Running ObjectJsonDocumentExample");

            // Provision data.
            await CreateTable();

            await using (var cmd = new NpgsqlCommand("""
            INSERT INTO testdrive.example (
              "object"
            ) VALUES (
              @object
            )
            """, conn))
            {
                cmd.Parameters.AddWithValue("object", NpgsqlDbType.Json, JsonDocument.Parse("""{"foo":"bar"}"""));
                cmd.ExecuteNonQuery();
            }

            // Flush data.
            await RefreshTable();

            // Query back data.
            await using (var cmd = new NpgsqlCommand("SELECT * FROM testdrive.example", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                reader.Read();
                var obj = reader.GetFieldValue<JsonDocument>("object");
                Console.WriteLine(obj);
                return obj;
            }
        }

        public async Task<List<JsonDocument>> ArrayJsonDocumentExample()
        {
            Console.WriteLine("Running ArrayJsonDocumentExample");

            // Provision data.
            await CreateTable();
            await InsertRecord();

            // Query back data.
            await using (var cmd = new NpgsqlCommand("SELECT * FROM testdrive.example", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                reader.Read();
                // TODO: System.InvalidCastException: Reading as 'System.Text.Json.JsonDocument' or [1]
                //       is not supported for fields having DataTypeName 'character varying[]'.
                //       [1] `System.Collections.Generic.List`1[[System.Text.Json.JsonDocument]`
                var obj = reader.GetFieldValue<List<JsonDocument>>("array");
                Console.WriteLine(obj);
                return obj;
            }
        }

        public async Task InsertPoco()
        {
            /***
             * Verify Npgsql POCO mapping with CrateDB.
             * https://www.npgsql.org/doc/types/json.html#poco-mapping
             */
            Console.WriteLine("Running InsertPoco");

            // Insert single data point.
            await using (var cmd = new NpgsqlCommand("""
                INSERT INTO testdrive.example (
                    "array_object",
                    "object"
                ) VALUES (
                    @array,
                    @object
                );
            """, conn))
            {
                cmd.Parameters.AddWithValue("object", NpgsqlDbType.Json, new BasicPoco { name = "Hotzenplotz" });
                cmd.Parameters.AddWithValue("array", NpgsqlDbType.Json, new List<BasicPoco>
                {
                    new BasicPoco { name = "Hotzenplotz" },
                    new BasicPoco { name = "Petrosilius", age = 42 },
                });
                cmd.ExecuteNonQuery();
            }

            // Flush data.
            await RefreshTable();

        }

        public async Task<BasicPoco> ObjectPocoExample()
        {
            Console.WriteLine("Running ObjectPocoExample");

            // Provision data.
            await CreateTable();
            await InsertPoco();

            // Query back data.
            await using (var cmd = new NpgsqlCommand("SELECT * FROM testdrive.example", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                reader.Read();
                var obj = reader.GetFieldValue<BasicPoco>("object");
                Console.WriteLine(obj);
                return obj;
            }
        }

        public async Task<List<BasicPoco>> ArrayPocoExample()
        {
            Console.WriteLine("Running ArrayPocoExample");

            // Provision data.
            await CreateTable();
            await InsertPoco();

            // Query back data.
            await using (var cmd = new NpgsqlCommand("SELECT * FROM testdrive.example", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                reader.Read();
                var obj = reader.GetFieldValue<List<BasicPoco>>("array_object");
                Console.WriteLine(obj[0]);
                Console.WriteLine(obj[1]);
                return obj;
            }
        }

    }

}
