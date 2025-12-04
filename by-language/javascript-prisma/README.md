# Using CrateDB with Prisma


## About

[Prisma] is a next-generation Node.js and TypeScript ORM.


## Details

This example shows how to use [Prisma Client] in a **simple Node.js script**, to
read and write data in a CrateDB database.

The folder has been scaffolded using this command:
```shell
npx try-prisma@latest --template javascript/script --install npm --name . --path .
```


## Usage

### Create the database

Run the following command to submit the SQL DDL to the database. This will create
database tables for the `User` and `Post` entities that are defined in
[`prisma/schema.prisma`](./prisma/schema.prisma).
```shell
npm install
npx prisma migrate dev --name init
```

### Execute the script
```shell
npm run dev
```



[Prisma]: https://www.prisma.io/
[Prisma Client]: https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client
[Simple Node.js Script Example]: https://github.com/prisma/prisma-examples/tree/latest/javascript/script
