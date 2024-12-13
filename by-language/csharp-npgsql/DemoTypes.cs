#nullable enable
using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Reflection;
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

    public class DatabaseWorkloadsMore
    {

        public static async Task<DataTable> AllTypesExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running AllTypesExample");

            // Submit DDL, create database schema.
            await using (var cmd = new NpgsqlCommand("DROP TABLE IF EXISTS testdrive.example", conn))
            {
                cmd.ExecuteNonQuery();
            }

            await using (var cmd = new NpgsqlCommand(@"
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
                    ""array"" ARRAY(STRING),
                    ""object"" OBJECT(DYNAMIC),
                    -- Geospatial types
                    geopoint GEO_POINT,
                    geoshape GEO_SHAPE,
                    -- Vector type
                    ""float_vector"" FLOAT_VECTOR(3)
                );
            ", conn))
            {
                cmd.ExecuteNonQuery();
            }

            // Insert single data point.
            await using (var cmd = new NpgsqlCommand(@"
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
                ""array"",
                ""object"",
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
        ", conn))
            {
                Console.WriteLine(cmd);
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
                cmd.Parameters.AddWithValue("array", new List<string>{"foo", "bar"});
                // FIXME: System.NotSupportedException: Cannot resolve 'hstore' to a fully qualified datatype name. The datatype was not found in the current database info.
                // cmd.Parameters.AddWithValue("object", new Dictionary<string, string>(){{"foo", "bar"}});
                cmd.Parameters.AddWithValue("object", @"{""foo"": ""bar""}");
                cmd.Parameters.AddWithValue("geopoint", new List<double>{85.43, 66.23});
                cmd.Parameters.AddWithValue("geoshape", "POLYGON ((5 5, 10 5, 10 10, 5 10, 5 5))");
                cmd.Parameters.AddWithValue("float_vector", new List<double> {1.1, 2.2, 3.3});
                cmd.ExecuteNonQuery();
            }

            // Flush data.
            await using (var cmd = new NpgsqlCommand("REFRESH TABLE testdrive.example", conn))
            {
                cmd.ExecuteNonQuery();
            }

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

        public static async Task<DataTable> ContainerTypesExample(NpgsqlConnection conn)
        {
            Console.WriteLine("Running AllTypesExample");

            // Submit DDL, create database schema.
            await using (var cmd = new NpgsqlCommand("DROP TABLE IF EXISTS testdrive.container", conn))
            {
                cmd.ExecuteNonQuery();
            }

            await using (var cmd = new NpgsqlCommand(@"
                CREATE TABLE testdrive.container (
                    -- Container types
                    ""array"" ARRAY(STRING),
                    ""object"" OBJECT(DYNAMIC)
                );
            ", conn))
            {
                cmd.ExecuteNonQuery();
            }

            // Insert single data point.
            await using (var cmd = new NpgsqlCommand(@"
                INSERT INTO testdrive.container (
                    ""array"",
                    ""object""
                ) VALUES (
                    @array,
                    @object
                );
        ", conn))
            {
                Console.WriteLine(cmd);
                // FIXME: While doing conversations with ARRAY types works natively,
                //        it doesn't work for OBJECT types.
                //        Yet, they can be submitted as STRING in JSON format.
                cmd.Parameters.AddWithValue("array", new List<string>{"foo", "bar"});
                cmd.Parameters.AddWithValue("object", @"{""foo"": ""bar""}");
                cmd.ExecuteNonQuery();
            }

            // Flush data.
            await using (var cmd = new NpgsqlCommand("REFRESH TABLE testdrive.container", conn))
            {
                cmd.ExecuteNonQuery();
            }

            // Query back data.
            await using (var cmd = new NpgsqlCommand("SELECT * FROM testdrive.container", conn))
            await using (var reader = cmd.ExecuteReader())
            {
                var dataTable = new DataTable();
                dataTable.Load(reader);
                var payload = JsonConvert.SerializeObject(dataTable);
                Console.WriteLine(payload);
                return (DataTable) dataTable;
            }

        }

    }

}
