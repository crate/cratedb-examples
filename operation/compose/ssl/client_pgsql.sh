#!/usr/bin/env sh

psql "postgresql://crate@localhost:5432/?sslmode=require" -c "SELECT 42"
