#!/usr/bin/env sh
set -e

echo "Running DB migrations (migrate only)..."
reflex db migrate

echo "Starting Reflex app..."
exec "$@"
