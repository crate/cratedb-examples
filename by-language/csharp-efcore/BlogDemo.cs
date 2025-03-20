// Example program for EFCore with CrateDB.

// Npgsql Entity Framework Core provider for PostgreSQL
// https://github.com/npgsql/efcore.pg
using System;
using System.Linq;
using Microsoft.EntityFrameworkCore;

public class Blog
{
    public long Id { get; set; }
    public required string Name { get; set; }
}

public class BloggingContext : DbContext
{
    public DbSet<Blog> Blogs { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        => optionsBuilder.UseNpgsql(@"Host=localhost;Username=crate;Password=;Database=testdrive");
}

class BlogDemo
{
    public BloggingContext context;
    
    public static void Main(string[] args)
    {
        var blogDemo = new BlogDemo();
        blogDemo.run();
    }

    public BlogDemo()
    {
        // Provide context and turn off transactions.
        context = new BloggingContext();
        context.Database.AutoTransactionBehavior = AutoTransactionBehavior.Always;
        context.Database.AutoSavepointsEnabled = false;

        // CrateDB does not implement 'DROP DATABASE'.
        // await context.Database.EnsureDeleted();
        context.Database.EnsureCreated();
    }

    public void run()
    {
        RunDDL();
        EfCoreWorkload();
    }

    public void RunDDL()
    {
        context.Database.ExecuteSqlRaw("""
            CREATE TABLE IF NOT EXISTS "Blogs" 
            ("Id" bigint GENERATED ALWAYS AS NOW(), "Name" text);
        """);
    }

    public void EfCoreWorkload()
    {

        // Insert a Blog.
        context.Blogs.Add(new() { Name = "FooBlog" });
        context.SaveChanges();

        // For converging written data immediately, submit a cluster-wide flush operation.
        // https://cratedb.com/docs/crate/reference/en/latest/sql/statements/refresh.html#sql-refresh
        context.Database.ExecuteSqlRaw("""REFRESH TABLE "Blogs";""");

        // Query all blogs whose name starts with F.
        var fBlogs = context.Blogs.Where(b => b.Name.StartsWith("F")).ToList();

        // Output the results to the console.
        foreach (var blog in fBlogs)
        {
            Console.WriteLine($"Blog Id: {blog.Id}, Blog Name: {blog.Name}");
        }
    }
}
