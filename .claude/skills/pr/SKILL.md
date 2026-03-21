---
name: pr
description: "Create pull requests with conventional titles using gh CLI. Use when creating PRs, opening pull requests, or pushing branches for review."
metadata:
  version: "1.0.0"
---

# Create Pull Request

Create pull requests with conventional commit-style titles using the `gh` CLI. Never add co-author labels.

## Title Format

```
<type>(<scope>): <subject>
```

Same types and scopes as conventional commits — see `/commit` skill for the full list.

Keep titles under 72 characters. Use the description for details, not the title.

## Rules

1. **No co-author labels** — never add `Co-Authored-By` lines anywhere
2. Title follows conventional commit format: imperative mood, lowercase, no period
3. Description uses the structured template below
4. Always push the branch before creating the PR
5. Base branch defaults to `master` unless specified otherwise

## Steps

1. Check the current branch and understand the scope of changes:
   ```bash
   git branch --show-current
   git status
   git log --oneline master..HEAD
   git diff master...HEAD --stat
   ```

2. **If on `master`** — you cannot push directly. Create a new branch first:
   ```bash
   git checkout -b <type>/<short-description>
   ```
   Branch naming: `feat/add-report-notifications`, `fix/cron-duplicate`, `chore/bump-ui-kit`, etc.
   If there are uncommitted changes, they will carry over to the new branch.

3. If the branch has not been pushed yet:
   ```bash
   git push -u origin HEAD
   ```

4. Analyze **all** commits on the branch (not just the latest) to draft the title and summary

4. Create the PR using a HEREDOC for the body:
   ```bash
   gh pr create --title "type(scope): subject line here" --body "$(cat <<'EOF'
   ## Summary
   - Brief bullet points explaining the changes

   ## Test plan
   - [ ] How to verify these changes work
   EOF
   )"
   ```

5. Return the PR URL to the user

## Description Template

```markdown
## Summary
- 1-3 bullet points describing what changed and why

## Test plan
- [ ] Steps or checks to verify the changes
```

Keep it concise. No fluff, no emojis, no generated-by footers.

## Examples

**Title examples:**
```
feat(console-ui): add scheduled report notifications
fix(console-server): prevent duplicate cron triggers
refactor(cloud-router): extract auth middleware into module
chore: bump ui-kit to v0.15.0 across packages
fix(ai-engineer): handle streaming timeout on large contexts
```

**Full example:**
```bash
gh pr create --title "feat(console-ui): add scheduled report notifications" --body "$(cat <<'EOF'
## Summary
- Add email and Slack notifications for scheduled report runs
- Support configurable notification channels per report
- Handle delivery failures with retry logic

## Test plan
- [ ] Create a scheduled report and verify notification is sent
- [ ] Test failure retry by simulating a delivery error
- [ ] Verify notification preferences persist across sessions
EOF
)"
```

## Options

- To target a different base branch: `gh pr create --base <branch> ...`
- To create as draft: `gh pr create --draft ...`
- To add reviewers: `gh pr create --reviewer user1,user2 ...`
- To add labels: `gh pr create --label "bug,priority" ...`
