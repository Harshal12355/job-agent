#!/bin/sh
# Runs on the Mac mini. From your laptop: ssh mini '~/job-agent/scripts/deploy.sh'
set -eu
cd "$(dirname "$0")/.."
git pull --ff-only
docker compose --profile dashboard up -d --build --remove-orphans
docker compose ps --format 'table {{.Service}}\t{{.Status}}'
