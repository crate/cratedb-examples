package io.crate.test;

import io.quarkus.test.common.QuarkusTestResourceLifecycleManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.testcontainers.cratedb.CrateDBContainer;
import org.testcontainers.utility.DockerImageName;

import java.util.HashMap;
import java.util.Map;

public class CrateDBTestResource implements QuarkusTestResourceLifecycleManager {

    private static final Logger log = LoggerFactory.getLogger(CrateDBTestResource.class);
    private CrateDBContainer cratedb;

    @Override
    public Map<String, String> start() {
        startContainer();

        Map<String, String> conf = new HashMap<>();
        conf.put("quarkus.datasource.jdbc.url", cratedb.getJdbcUrl());
        conf.put("quarkus.datasource.username", cratedb.getUsername());
        conf.put("quarkus.datasource.password", cratedb.getPassword());
        conf.put("quarkus.datasource.db-kind","postgresql");
        conf.put("quarkus.hibernate-orm.dialect","com.wamas.core.kpiserver.crate.CrateDbDialect");
        return conf;
    }

    @Override
    public void stop() {
        cratedb.stop();
    }


    private void startContainer() {
        // Run CrateDB latest.
        DockerImageName image = dockerImageLatest();
        cratedb = new CrateDBContainer(image);
        cratedb.start();
    }

    public static DockerImageName dockerImageLatest() {
        return DockerImageName.parse("crate:latest").asCompatibleSubstituteFor("crate");
    }
}
