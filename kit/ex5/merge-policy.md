# Merge policy · worksheet

Write the policy in three columns. The column decides who enforces each line.

| What the merge routine checks | What GitHub enforces | What stays human |
|---|---|---|
| The review has run on the latest push (label `reviewed`) | CI `tests` is a required check | Paths in `.github/CODEOWNERS` |
| Every finding has a fix or a reply | Code-owner review is required | |
| The diff stays inside the paths the issue named | | |
| Severity at or below: ___ | | |
| _your rule_ | _your rule_ | _your path_ |

The first column is a prompt: it **persuades**. The second is configuration: it
**refuses**. The routine's job is to turn on auto-merge (`gh pr merge --auto`);
GitHub decides whether the merge happens. `./workshop setup` applied the second
column's defaults as the `main` ruleset.

## The trap in a copy that only you own

A routine acts as **your** GitHub user. So a pull request the repair routine opened
is, for GitHub, a pull request **you** opened, and GitHub does not let an author
approve their own pull request. In your copy that means:

- a PR touching a code-owned path can only merge through the ruleset's admin bypass,
  which is you, by hand;
- nothing but the prompt stops the merge routine from using that same bypass
  (`gh pr merge --admin`). Say in the prompt that it must never, and know that this
  line persuades.

In a team, the code owner is a different person, and the separation is real. Write
down which situation you are in.

## Merge routine · prompt starter

```text
You are the merge routine. You run when a pull request gets the label `reviewed`.
Check, in order, and stop at the first that fails, commenting why:
1. The PR was opened by the repair routine (its body says `Fixes #<n>`).
2. Every review finding has a fix or a reply.
3. Only the paths the issue named are changed.
4. The issue's severity is at or below <S>.
If all hold, run `gh pr merge --auto --squash`. Never use `--admin`. Never
approve a pull request.
```
