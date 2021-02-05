SELECT uid,nameid,name,unit,value,timestamp
FROM
    (SELECT
           uid,
           nameid,
           name,
           unit,
           timestamp,
           value,
           FIRST_VALUE(value) OVER (w) AS "max",
           -- FIRST_VALUE(timestamp) OVER (w) AS "max_ts",
           LAST_VALUE(value) OVER (w) AS "min",
           -- LAST_VALUE(timestamp) OVER (w) AS "min_ts"
    FROM telemetry_01
    WHERE "nameid" in
        ('43CAB42B447E4578DEEDF43B211A3FFE174445529A21948318B05ECD9E2C76E6',
         '01DB60764B125AF8102F10E21E45470BC7C2D0A095F43C24FC83B55BCA726726',
         '507744F768594E94A2D65BE1F7FC69ABA27317D942224626EB56E8212F7655E5',
         '32B4D18C6FE2250049F27737E1EC2E4B56623491592D03FEF55FCC2B8E4ADBB5')
        AND "timestamp" >= '2021-01-22T02:54:44.6100000Z'
        AND "timestamp" < '2021-01-22T03:59:19.2480000Z'
    WINDOW "w" AS (PARTITION BY uid, nameid, name, unit,
                    FLOOR((EXTRACT(EPOCH FROM timestamp)) / 300)
                    ORDER BY "value" DESC
                    RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
    ORDER BY 1,2,3,4,5) s
WHERE value = max OR value = min
