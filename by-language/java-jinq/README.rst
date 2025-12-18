.. highlight:: sh

############################################################
Java Jinq demo application for CrateDB using PostgreSQL JDBC
############################################################


Jinq - Simple Natural Queries with Java.


*****
About
*****

In a nutshell
=============

A demo application using `CrateDB`_ with `Jinq`_ and the `PostgreSQL
JDBC driver`_.
It is intended as a basic example to demonstrate what works, and what not.
Currently, it is only a stub. Contributions are welcome.

Introduction
============

`Jinq`_ and `jOOQ`_ are in a similar area like `LINQ`_. We've picked up and
summarized a few quotes from blog posts and interviews by Dr. Ming-Yee Iu and
Lukas Eder, the main authors of Jinq and jOOQ.

Firstly, you may enjoy the guest post by Dr. Ming-Yee Iu `Java 8 Will
Revolutionize Database Access`_, which outlines how adding functional-support
to the Java language version 8 made a difference while aiming to write database
inquiries more fluently at that time (2014).

    Ever since Erik Meijer has introduced LINQ to the .NET ecosystem, us Java
    folks have been wondering whether we could have the same.

Two years later, Dr. Ming-Yee Iu gives an `insight into Language Integrated
Querying`_ at the `jOOQ Tuesdays series`_.

    LINQ makes a lot of sense for the C# ecosystem, but I think it is totally
    inappropriate for Java.

    Fortunately, Java programmers can use libraries such as Jinq and jOOQ
    instead, which provide most of the benefits of LINQ but don’t require tight
    language integration like LINQ.

Details
=======

From the documentation at http://www.jinq.org/, about what Jinq actually is,
and does.

    Jinq provides developers an easy and natural way to write database queries
    in Java. You can treat database data like normal Java objects stored in
    collections. You can iterate over them and filter them using normal Java
    commands, and all your code will be automatically translated into optimized
    database queries. Finally, LINQ-style queries are available for Java!

    With Jinq, you can write database queries using a simple, natural Java
    syntax. Using Java 8's new support for functional programming, you can
    filter and transform data in a database using the same code you would use
    for normal Java data.


********
Synopsis
********

The idea of Jinq is to write database queries using a simple, natural Java
syntax based on the functional programming support added with Java 8. Accessing
a database table using the Jinq API looks like this:

.. code-block:: java

    // Fetch records, with filtering and sorting, result iteration and printing.
    customers()
        .where(c -> c.getCountry().equals("UK"))
        .sortedDescendingBy(c -> c.getSalary())
        .forEach(c -> out.println(c.getName() + " " + c.getSalary()));

A few other concise `Jinq code examples`_ can be discovered at the Jinq code
base.



.. _CrateDB: https://github.com/crate/crate
.. _Jinq code examples: https://github.com/my2iu/Jinq/blob/main/sample/src/com/example/jinq/sample/SampleMain.java
.. _Insight into Language Integrated Querying: https://blog.jooq.org/jooq-tuesdays-ming-yee-iu-gives-insight-into-language-integrated-querying/
.. _Java 8 Will Revolutionize Database Access: https://blog.jooq.org/java-8-friday-java-8-will-revolutionize-database-access/
.. _Jinq: https://github.com/my2iu/Jinq
.. _jOOQ: https://github.com/jOOQ/jOOQ
.. _jOOQ Tuesdays series: https://www.jooq.org/tuesdays
.. _LINQ: https://en.wikipedia.org/wiki/Language_Integrated_Query
.. _PostgreSQL JDBC Driver: https://github.com/pgjdbc/pgjdbc
