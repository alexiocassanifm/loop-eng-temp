# Exercise 4 · Write your own review loop

**20 minutes · ring 4, the review loop · branch: `./workshop reset ex4`**

Opening a pull request starts `.github/workflows/review.yml`: Claude reads the diff,
posts findings on specific lines and one summary comment. A PR is delivered when that
review has run, been read in both places it writes, and every finding has a fix or a
reply.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

## Steps

### 1 · Fill in the skill

```bash
./workshop reset ex4
claude
```

`.claude/skills/review-loop/SKILL.md` has four stubbed sections: when to run, how to
wait, where to read, what to answer. Paste:

```text
Fill in the four sections of .claude/skills/review-loop/SKILL.md. Keep the headings
and the frontmatter; replace each HTML comment with instructions an agent can follow.
Use these facts, all measured on this repository:
- The review is the workflow "Claude review". It starts when a PR is opened and again
  on every push to it. A real review takes one to eight minutes.
- Wait with: gh run watch <run id>, where the id comes from
  gh run list --workflow "Claude review" --branch <branch> --limit 1 --json databaseId -q ".[0].databaseId"
  A run that finished in about 15 seconds reviewed nothing: say so, do not report it
  as clean.
- It writes in two places. The summary: gh pr view <n> --comments. The findings on
  lines: gh api repos/{owner}/{repo}/pulls/<n>/comments --jq '.[] | "\(.path):\(.line // .original_line)\n\(.body)\n"'
  After a later push, .line becomes null for a finding whose line moved; that is why
  the query falls back to .original_line.
- For each finding: reproduce it first (run the code or write a failing test) before
  changing anything. The reviewer read the code; it did not run it. Reproduced: fix it
  and push. Not reproduced, or you disagree: reply on the PR saying why.
- The loop ends when every finding has a fix or a reply, never before.
Show me the finished file.
```

Read what it wrote. It is your skill now: change anything you would do differently.
Then commit it and leave Claude Code:

```bash
git add .claude/skills/review-loop/SKILL.md
git commit -m "review-loop skill"
```

```text
/exit
```

### 2 · Open a PR and let the skill run the loop

```bash
git push -u origin ex4-work
gh pr create --fill
claude
```

A new session loads the skill you just wrote. Paste:

```text
/review-loop on the pull request of this branch.
```

Let the skill do the waiting, not you.

**Expect:** it finds the run, waits one to eight minutes, then lists the summary **and**
the inline findings.

### 3 · Answer every finding

If the skill has not already started on them:

```text
Work through every finding as the review-loop skill says: reproduce first, then fix
and push, or reply on the PR saying why not. After the push, run the review loop
again on the new review.
```

### 4 · Stop only on nothing unanswered

```text
List every finding of the latest review, each with the commit that fixed it or the
link to your reply. Is anything unanswered?
```

Then open the PR's **Actions** tab and look at how long each review run took.

One full review round is the exercise. A second round is the overflow: a review takes
one to eight minutes.

## Variant · read only one place

Remove the inline-findings command from the **Where to read** section of your skill,
then ask:

```text
/review-loop on the pull request of this branch. Report only what is unanswered.
```

What does the loop report now, and what did it stop seeing?

## Watch for

- Reading only the summary and missing the inline findings.
- Applying a finding without reproducing it first. The reviewer reads the code; it
  did not run it.
- A review that finished in about fifteen seconds probably reviewed nothing: read its log.
