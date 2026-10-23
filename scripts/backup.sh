#!/bin/sh
# Nightly, from the worker's cron: copy data/ and out/ into the private data repo and push.
# Copies, never deletes, so a bad day on the mini can't erase yesterday's backup.
set -eu
: "${DATA_REPO_URL:?set DATA_REPO_URL in .env}"
dest=/app/.backup
[ -d "$dest/.git" ] || git clone -q "$DATA_REPO_URL" "$dest"
mkdir -p "$dest/data" "$dest/out"
cp -R /app/data/. "$dest/data/"
cp -R /app/out/. "$dest/out/"
cd "$dest"
git add -A
git -c user.name=jobagent -c user.email=jobagent@localhost commit -qm "backup $(date +%F)" || exit 0
git push -q origin HEAD
