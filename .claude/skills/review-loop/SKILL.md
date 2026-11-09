---
name: review-loop
description: Close the review loop on a pull request — wait for the Claude review, read both places it writes, answer every finding. Use right after opening a PR and after every push to it.
---

# Review loop

A pull request is delivered when its review has run, been read, and every finding
has a fix or a reply. Fill in the four sections below. Exercise 4 is writing them.

## When to run

Run this skill at two moments:

- Right after opening a pull request.
- After every push to an open pull request, including the pushes you make to fix
  findings in this loop.

The workflow "Claude review" starts at both moments, so each one produces a new
review to wait for and read.

## How to wait

A real review takes one to eight minutes. Block on the run instead of polling or
refreshing a page.

1. Get the id of the latest run on the branch:

   ```sh
   gh run list --workflow "Claude review" --branch <branch> --limit 1 --json databaseId -q ".[0].databaseId"
   ```

2. Wait for it to finish. Give the command a timeout longer than eight minutes, or
   run it in the background, so the shell does not kill it mid-review:

   ```sh
   gh run watch <run id>
   ```

3. Check how long the run took. A run that finished in about 15 seconds reviewed
   nothing: say so, and do not report the pull request as clean.

## Where to read

The review writes in two places. Read both every time.

The summary:

```sh
gh pr view <n> --comments
```

The findings on lines:

```sh
gh api repos/{owner}/{repo}/pulls/<n>/comments --jq '.[] | "\(.path):\(.line // .original_line)\n\(.body)\n"'
```

After a later push, `.line` becomes null for a finding whose line moved, which is
why the query falls back to `.original_line`. The finding stays in the output and
still needs an answer, but its number may not match the current file. Find the code
by reading the file, not by trusting the number.

## What to answer

The reviewer read the code; it did not run it. Treat each finding as a claim to test.

For each finding:

1. Reproduce it first, by running the code or writing a failing test. Change nothing
   before this step.
2. Reproduced: fix it and push.
3. Not reproduced, or you disagree: reply on the PR saying why.

Each push starts a new review. Go back to "How to wait" and answer what that run
finds as well.

The loop ends when every finding has a fix or a reply, never before.
