# Using CrateDB with TypeORM


## About

[TypeORM] is an ORM that can run in NodeJS, Browser, Cordova, PhoneGap, Ionic,
React Native, NativeScript, Expo, and Electron platforms and can be used with
TypeScript and JavaScript (ES5, ES6, ES7, ES8).


## Details

This example shows the canonical TypeORM example project using CrateDB. It has
been scaffolded using this command:
```shell
npx typeorm init --name . --database postgres --express
```
A few adjustments have been made because CrateDB does not support the `SERIAL`
data type.


## Data Model

The data model for the `User` entity is defined in [`User.ts`](./src/entity/User.ts).


## Usage

```shell
# Install dependencies.
npm install

# Run program.
npm start
```


## Development

Link a TypeORM working tree to a downstream project.

```shell
cd /path/to/somewhere
git clone https://github.com/crate-workbench/typeorm --branch cratedb
cd typeorm
npm run package
cd build/package
npm link

cd /path/to/here
npm link typeorm
```

### References
- https://orkhan.gitbook.io/typeorm/DEVELOPER
- https://medium.com/dailyjs/how-to-use-npm-link-7375b6219557


[TypeORM]: https://typeorm.io/
