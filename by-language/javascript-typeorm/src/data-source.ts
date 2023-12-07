import "reflect-metadata"
import { DataSource } from "typeorm"
import { User } from "./entity/User"

export const AppDataSource = new DataSource({
    type: "cratedb-postgres",
    host: "localhost",
    port: 5432,
    username: "crate",
    password: "",
    database: "test",
    synchronize: true,
    logging: true,
    entities: [User],
    migrations: [],
    subscribers: [],
})
