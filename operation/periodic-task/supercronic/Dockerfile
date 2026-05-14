FROM ghcr.io/crate/cratedb-toolkit:0.0.48

# Define a crontab. If you need help, consider those resources.
# https://crontab.guru/
# https://github.com/aptible/supercronic/tree/main/cronexpr

COPY <<EOF /etc/periodic-tasks.txt
SQL_SUMMITS='SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3'

@hourly                         echo "Hourly greetings from scheduler"
#* * * * * * *                   echo "Ping from scheduler"  # each second
*/15 * * * * * *                ctk shell --command "\${SQL_SUMMITS}"
*/15 * * * * * *                crash --hosts "\${CRATEDB_HTTP_URL}" --command "\${SQL_SUMMITS}"
0 */1 * * * * *                 unset CRATEDB_CLUSTER_URL; ctk --verbose save "crate://crate:crate@cratedb:4200/sys/summits" "file+deltalake:///var/delta/summits?mode=overwrite"
* * * * *                       /scripts/every-minute
0,10,20,30,40,50 6-22 * * *     /scripts/daytime-service-task
EOF

RUN supercronic -test /etc/periodic-tasks.txt
ENTRYPOINT ["supercronic", "-passthrough-logs", "/etc/periodic-tasks.txt"]
