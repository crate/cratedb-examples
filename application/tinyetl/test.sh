#!/bin/sh
set -e

sh install.sh
sh import.sh
sh query.sh
sh verify.sh
