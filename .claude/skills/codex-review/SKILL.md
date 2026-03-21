---
name: codex-review
description: "Run OpenAI Codex code review on current changes or review a plan/design. Use when user asks to review code, review implementation, or run codex review."
metadata:
  version: "1.4.0"
---

# Codex Code Review

Run OpenAI Codex CLI to review code changes or implementation plans.

## Mode Detection

Determine which mode to use based on what the user wants reviewed:

### Mode A — Code Diff Review (`codex review`)

Use when the user wants to review **actual code changes** (committed or uncommitted).

Indicators: "review my changes", "review this PR", "review the diff", or no specific context (default).

### Mode B — Plan / Design Review (`codex exec`)

Use when the user wants to review **a plan, design, or suggested implementation** that exists in conversation context — NOT as code diffs.

Indicators: "review the suggested implementation", "review this plan", "review the design", "review what was proposed", or when there are no relevant code changes on the branch.

## Compact Prompt

Always pass a compact-output instruction via heredoc stdin to reduce context window usage. `codex review` does NOT accept a prompt as a positional argument alongside flags, but it does read from stdin via heredoc.

```
COMPACT_PROMPT="Be concise. For each finding output ONLY: severity (critical/warning/info), file:line, and a one-line description. Group by severity. No code snippets unless critical. No preamble or summary paragraph."
```

## Mode A — Code Diff Review

1. Run `git status` to check for uncommitted changes
2. Choose the appropriate review target:

   **Uncommitted changes** (staged, unstaged, or untracked):
   ```bash
   codex review --uncommitted <<'EOF'
   $COMPACT_PROMPT
   EOF
   ```

   **Specific commit SHA**:
   ```bash
   codex review --commit <SHA> <<'EOF'
   $COMPACT_PROMPT
   EOF
   ```

   **Base branch comparison**:
   ```bash
   codex review --base <BRANCH> <<'EOF'
   $COMPACT_PROMPT
   EOF
   ```

   **No uncommitted changes** — review latest commit:
   ```bash
   codex review --commit HEAD <<'EOF'
   $COMPACT_PROMPT
   EOF
   ```

3. Present the output and offer to help fix issues

## Mode B — Plan / Design Review

Use `codex exec` in read-only sandbox mode. Pipe the plan text via stdin.

1. Collect the plan/design text from the conversation context
2. Write it to a temp file, then run:

   ```bash
   codex exec --sandbox read-only -o /dev/stdout - <<'PLAN_EOF'
   Review the following implementation plan for a codebase at $PWD.
   Identify issues, missing edge cases, security concerns, and incorrect assumptions.
   Be concise. List issues as bullet points with severity (critical/warning/info).

   --- PLAN ---
   <paste plan text here>
   PLAN_EOF
   ```

   Or if the plan references files that already exist, let codex read them:
   ```bash
   codex exec --sandbox read-only "$REVIEW_PROMPT"
   ```

   Where `$REVIEW_PROMPT` includes the plan text and instructions to read relevant files.

3. Present the output and offer to help address issues

## Custom Instructions

If the user provides arguments (e.g. "focus on security"), prepend them to the compact prompt in the heredoc:

```bash
# Mode A
codex review --uncommitted <<'EOF'
Focus on security. $COMPACT_PROMPT
EOF

# Mode B
codex exec --sandbox read-only "focus on security. $REVIEW_PROMPT"
```

## Notes

- The `codex` CLI must be installed and authenticated (`codex login`)
- Timeout should be generous (up to 5 minutes) as reviews can take time
- The compact prompt keeps output short; if the user wants full verbose output, they can say `/codex-review --verbose` and you should omit the heredoc
- For Mode B, always use `--sandbox read-only` since no writes are needed
