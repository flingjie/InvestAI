#!/bin/bash
set -e

# 启动应用
echo "Starting monitor service ..."
exec uv run python run_monitor.py
