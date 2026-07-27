#!/usr/bin/env bash
# 鏡像 jhihsheng/OTID 的 computing_lab/ 進本 repo（唯讀鏡像；來源真相在 OTID repo）
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
git clone --depth 1 https://github.com/jhihsheng/OTID "$TMP/OTID"
if command -v rsync >/dev/null 2>&1; then
  rsync -av --delete --exclude '.git' "$TMP/OTID/computing_lab/" "$HERE/computing_lab/"
else
  # 無 rsync 時的等效鏡像（--delete 語意：先清掉再整份複製）
  rm -rf "$HERE/computing_lab"
  cp -a "$TMP/OTID/computing_lab" "$HERE/computing_lab"
fi
rm -rf "$TMP"
echo "computing_lab/ synced from jhihsheng/OTID — review 'git status', then commit."
