using GeoJSON.Net.Geometry;
using Newtonsoft.Json;
using Npgsql;
using NpgsqlTypes;
using System.Data;

namespace demo;

/// <summary>
/// Extension methods for reading and writing CrateDB GEO_SHAPE values as GeoJSON.Net types.
///
/// CrateDB communicates GEO_SHAPE over the PostgreSQL wire protocol as a JSON string,
/// not as PostGIS binary geometry. Npgsql's PostGIS/GeoJSON plugin (UseGeoJson /
/// NpgsqlDbType.Geometry) therefore cannot be used — it requires the server to expose
/// a PostGIS geometry OID which CrateDB does not.
///
/// These helpers wrap the JSON serialization/deserialization so call sites can work
/// with strongly-typed GeoJSON.Net objects (Point, Polygon, LineString, …) directly,
/// without scattering JsonConvert calls across the codebase.
/// </summary>
public static class CrateGeoShapeExtensions
{
    /// <summary>
    /// Adds a GEO_SHAPE parameter by serializing <paramref name="geometry"/> to a GeoJSON string.
    /// </summary>
    /// <typeparam name="T">Any GeoJSON.Net geometry type (Point, Polygon, LineString, …).</typeparam>
    public static void AddGeoShape<T>(this NpgsqlParameterCollection parameters, string name, T geometry)
        where T : IGeometryObject
    {
        parameters.AddWithValue(name, NpgsqlDbType.Json, JsonConvert.SerializeObject(geometry));
    }

    /// <summary>
    /// Reads a GEO_SHAPE column and deserializes it to <typeparamref name="T"/>.
    /// Returns <c>null</c> if the column value is NULL.
    /// </summary>
    /// <typeparam name="T">Any GeoJSON.Net geometry type (Point, Polygon, LineString, …).</typeparam>
    public static T? GetGeoShape<T>(this NpgsqlDataReader reader, string columnName)
        where T : class, IGeometryObject
    {
        var ordinal = reader.GetOrdinal(columnName);
        if (reader.IsDBNull(ordinal))
            return null;
        // CrateDB returns GEO_SHAPE as a JSON document over the wire.
        var json = reader.GetFieldValue<System.Text.Json.JsonDocument>(ordinal).RootElement.ToString();
        return JsonConvert.DeserializeObject<T>(json);
    }
}
