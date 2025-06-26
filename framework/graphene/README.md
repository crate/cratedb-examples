# Example Flask Graphene-SQLAlchemy project showing GraphQL against CrateDB

This example project derived from the
[graphene-sqlalchemy flask_sqlalchemy example](https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy)
demos how GraphQL queries can be run against data stored in CrateDB using
Graphene-SQLAlchemy. This way, the data is accessible both via SQL and GraphQL.

To run this example, you will need an instance of CrateDB. You can get an
instance of
[CrateDB running locally with docker](https://cratedb.com/docs/guide/install/container/index.html#install-container)

The project contains two models, one named `Department` and another named
`Employee`.

## Getting started

First, it is a good idea (but not required) to create a virtual environment for
this project. We'll do this using
[venv](https://docs.python.org/3/library/venv.html) to keep things simple:

```bash
python -m venv ./graphql-demo
source ./graphql-demo/bin/activate
```

Now we will need to get the source of the project. Do this by cloning the whole
cratedb-examples repository:

```bash
# Get the example project code
git clone https://github.com/crate/cratedb-examples.git
cd cratedb-examples/topic/graphql
```

Now we can install our dependencies:

```bash
pip install -r requirements.txt
```

Now the following command will set up the database, and start the server:

```bash
python ./app.py

```

Now head on over to
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) and run some
GraphQL queries, for example:

```graphql
{
  allEmployees(sort: [NAME_ASC, ID_ASC]) {
    edges {
      node {
        id
        name
        department {
          id
          name
        }
        role {
          id
          name
        }
      }
    }
  }
}
```
