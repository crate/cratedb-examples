CREATE TABLE alltypes (
    name STRING PRIMARY KEY,
    date TIMESTAMP,
    datetime_tz TIMESTAMP WITH TIME ZONE,
    datetime_notz TIMESTAMP WITHOUT TIME ZONE,
    nullable_datetime TIMESTAMP,
    nullable_date TIMESTAMP,
    kind STRING,
    flag BOOLEAN,
    position INTEGER,
    description STRING,
    details ARRAY(OBJECT),
    attributes OBJECT(DYNAMIC),
    coordinates GEO_POINT
) WITH (number_of_replicas=0);
