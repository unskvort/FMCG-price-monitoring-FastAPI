#!/usr/bin/env bash

set -a
source dev.env
set +a
export DATABASE_URL=sqlite:///./sqlite.db

pytest