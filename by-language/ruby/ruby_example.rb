#
# Basic examples for connecting to CrateDB with Ruby, using both HTTP and PostgreSQL protocols.
#
# https://github.com/crate/cratedb-examples/tree/main/by-language/ruby
#

def demo_crate_ruby

  puts "=" * 42
  puts "Demo using `crate_ruby` library"
  puts "=" * 42

  # Use `crate_ruby` library.
  require 'crate_ruby'
  client = CrateRuby::Client.new(servers = ["localhost:4200"], opts = {username: "crate"})

  # Insert data.
  client.execute("CREATE TABLE IF NOT EXISTS testdrive (id INT PRIMARY KEY, data TEXT);")
  client.execute("DELETE FROM testdrive;")
  client.execute("INSERT INTO testdrive VALUES (0, 'zero'), (1, 'one'), (2, 'two')")
  client.execute("REFRESH TABLE testdrive;")

  # Query data.
  result = client.execute("SELECT * FROM testdrive ORDER BY id")

  puts "Columns and values:"
  p Columns: result.cols, Results: result.values
  puts

  puts "Results by row:"
  result.each do |row|
    puts row.inspect
  end

end


def demo_pg

  puts "=" * 42
  puts "Demo using `pg` library"
  puts "=" * 42

  # Use `pg` library.
  require 'pg'
  client = PG.connect("postgresql://crate@localhost:5432/doc")

  # Insert data.
  client.exec("CREATE TABLE IF NOT EXISTS testdrive (id INT PRIMARY KEY, data TEXT);")
  client.exec("DELETE FROM testdrive;")
  client.exec("INSERT INTO testdrive VALUES (0, 'zero'), (1, 'one'), (2, 'two')")
  client.exec("REFRESH TABLE testdrive;")

  # Query data.
  result = client.exec("SELECT * FROM testdrive ORDER BY id")

  puts "Columns and values:"
  p Columns: result.fields, Results: result.values
  puts

  puts "Results by row:"
  result.each do |row|
    puts row.inspect
  end

end


if __FILE__ == $0
  driver = ARGV[0]
  if driver == "crate_ruby"
    demo_crate_ruby()
  elsif driver == "pg"
    demo_pg()
  else
    raise "Unknown driver: #{driver}. Please use 'crate_ruby' or 'pg'."
  end
end
