namespace demo;

public class BasicPoco
{

    public string? name { get; set; }
    public int? age { get; set; }

    public override bool Equals(object obj)
    {
        var other = (BasicPoco) obj;
        return name == other.name && age == other.age;
    }

    public override int GetHashCode()
    {
        return base.GetHashCode();
    }

    public override string ToString() => "Name: " + name + " Age: " + age;

}
