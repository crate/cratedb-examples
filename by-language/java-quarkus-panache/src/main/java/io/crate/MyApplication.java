package io.crate;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.quarkus.arc.Unremovable;
import io.quarkus.runtime.Quarkus;
import io.quarkus.runtime.ShutdownEvent;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.enterprise.inject.Produces;

@ApplicationScoped
public class MyApplication {
    private static final Logger log = LoggerFactory.getLogger(MyApplication.class);

    void onStart(@Observes StartupEvent event) {
        log.info("starting the crate demo application.");

        MyEntity.populateWithData(1);

        List<MyEntity> data = MyEntity.listAll();

        log.info("Print populated data");

        for (MyEntity entity : data) {
            log.info(entity.toString());
        }
    }

    void onStop(@Observes ShutdownEvent event) {
        log.info("i have done my duty and may lay my head to rest.");
    }

    @Produces
    @Unremovable // Prevent quarkus from optimizing ObjectMapper away
    public ObjectMapper objectMapper() {
        return new ObjectMapper();
    }

    public static void main(String[] args) {
        Quarkus.run(args);
    }
}
