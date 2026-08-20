#!/usr/bin/env bash
# Verifies that every ELF binary in a directory supports the requested glibc.
set -euo pipefail

ROOT=${1:?usage: check_glibc_compatibility.sh DIRECTORY [MAX_GLIBC_VERSION]}
MAX_GLIBC_VERSION=${2:-2.36}
highest_version=0
highest_file=

while IFS= read -r -d '' file; do
    if ! readelf -h "$file" >/dev/null 2>&1; then
        continue
    fi

    version=$(readelf --version-info "$file" 2>/dev/null \
        | grep -oE 'GLIBC_[0-9]+\.[0-9]+' \
        | sed 's/^GLIBC_//' \
        | sort -V \
        | tail -n 1 || true)

    if [ -n "$version" ] && [ "$(printf '%s\n%s\n' "$highest_version" "$version" | sort -V | tail -n 1)" = "$version" ]; then
        highest_version=$version
        highest_file=$file
    fi
done < <(find "$ROOT" -type f -print0)

echo "Highest required glibc version: $highest_version${highest_file:+ ($highest_file)}"

if [ "$(printf '%s\n%s\n' "$MAX_GLIBC_VERSION" "$highest_version" | sort -V | tail -n 1)" != "$MAX_GLIBC_VERSION" ]; then
    echo "error: build requires glibc $highest_version, newer than supported glibc $MAX_GLIBC_VERSION" >&2
    exit 1
fi
