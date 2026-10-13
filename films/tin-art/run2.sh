#!/usr/bin/env bash
# Headless film run: Opus 5.5 at max effort, all permissions inside this folder, full event log.
cd "$(dirname "$0")"
claude -p "$(cat PROMPT2.md)" \
  --model claude-opus-5-5 --effort max \
  --dangerously-skip-permissions \
  --output-format stream-json --verbose \
  > logs/run.jsonl 2> logs/run.err
echo "exit $?" >> logs/run.err
