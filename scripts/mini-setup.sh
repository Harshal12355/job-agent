#!/bin/sh
# One time, on the Mac mini, from an admin account: stay awake, come back after power cuts.
set -eu
sudo pmset -a sleep 0 disksleep 0 displaysleep 10 autorestart 1 womp 1
pmset -g | grep -E ' (sleep|disksleep|autorestart|womp) '
cat <<'EOF'

Still to do by hand (System Settings):
  1. General > Sharing > Remote Login: on, only for the jobagent user
  2. Docker Desktop > Settings > General: "Start Docker Desktop when you sign in"
  3. Docker Desktop > Settings > Resources: 4 CPUs, 6 GB memory (leave room for your friend)
  4. Tailscale: install, sign in, then run:  tailscale serve --bg 8501
EOF
