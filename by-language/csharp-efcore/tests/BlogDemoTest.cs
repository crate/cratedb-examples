using System.Data;
using Microsoft.EntityFrameworkCore;
using Npgsql;
using Xunit;

public class BlogDemoTest
{
    public NpgsqlConnection GetConnection(string? connectionString)
    {
        var dataSourceBuilder = new NpgsqlDataSourceBuilder(connectionString);
        // dataSourceBuilder.EnableDynamicJson();
        using var dataSource = dataSourceBuilder.Build();
        return dataSource.OpenConnection();
    }

    [Fact]
    public void TestBlogDemo()
    {
        // Invoke example database workload.
        var blogDemo = new BlogDemo();
        blogDemo.run();

        // Validate database content.
        var conn = GetConnection(blogDemo.context.Database.GetConnectionString());
        var cmd = new NpgsqlCommand("""SELECT * FROM testdrive."Blogs";""", conn);
        var reader = cmd.ExecuteReader();

        var data = new DataTable();
        data.Load(reader);
        
        // Check first record.
        var row = data.Rows[0];
        Assert.NotNull(row["Id"]);
        Assert.Equal("FooBlog", row["Name"]);
        
        conn.Close();
        conn.Dispose();
    }
    
}
