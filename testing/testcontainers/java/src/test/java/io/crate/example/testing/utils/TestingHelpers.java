package io.crate.example.testing.utils;

import io.crate.example.testing.Application;
import org.testcontainers.utility.DockerImageName;

import java.sql.SQLException;

import static org.assertj.core.api.Assertions.assertThat;

public final class TestingHelpers {

    public static DockerImageName nameFromLabel(String label) {
        String fullImageName;
        if (label == null) {
            fullImageName = "crate:latest";
        } else {
            if (label.equals("nightly")) {
                fullImageName = "crate/crate:nightly";
            } else {
                fullImageName = String.format("crate:%s", label);
            }
        }
        return DockerImageName.parse(fullImageName).asCompatibleSubstituteFor("crate");
    }

    public static DockerImageName nameFromEnvironment() {
        String label = System.getenv("CRATEDB_VERSION");
        return nameFromLabel(label);
    }

    public static void assertResults(Application.Results results) throws SQLException {
        assertThat(results.metaData().getColumnCount()).isEqualTo(9);
        assertThat(results.rows()).hasSize(3);
        assertThat(results.rows().stream().map(r -> r[6]).toList()).containsExactly(
                "Mont Blanc",
                "Monte Rosa",
                "Dom");
    }
}
