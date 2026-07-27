#!/usr/bin/env bash
# 鏡像 jhihsheng/OTID 的 computing_lab/ 進本 repo（唯讀鏡像；來源真相在 OTID repo）
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
git clone --depth 1 https://github.com/jhihsheng/OTID "$TMP/OTID"
rsync -av --delete --exclude '.git' "$TMP/OTID/computing_lab/" "$HERE/computing_lab/"
rm -rf "$TMP"
echo "computing_lab/ synced from jhihsheng/OTID — review 'git status', then commit."
