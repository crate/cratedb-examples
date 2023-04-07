package io.crate.example.testing.utils;

import io.crate.example.testing.Application;

import java.sql.SQLException;

import static org.assertj.core.api.Assertions.assertThat;

public final class TestingHelpers {

    public static void assertResults(Application.Results results) throws SQLException {
        assertThat(results.metaData().getColumnCount()).isEqualTo(9);
        assertThat(results.rows()).hasSize(3);
        assertThat(results.rows().stream().map(r -> r[6]).toList()).containsExactly(
                "Mont Blanc",
                "Monte Rosa",
                "Dom");
    }
}
