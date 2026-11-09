# Exercise 5 · Close the loop on today

**30 minutes, in teams of two or three · ring 5, dogfooding · branch: `./workshop reset ex5`**

What broke during exercises 1 to 4 becomes a queue; a routine works the queue at
night; a second routine merges what passes the policy you write. Today you build the
first two steps and write the third one down.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

```bash
./workshop reset ex5
claude
```

## Steps

### 1 · File two defects you hit today

Pick two things that broke or surprised you in exercises 1 to 4. For each one, paste
this and replace the first line:

```text
Defect: <one line: what broke, e.g. "the /loop kept firing after CI was green">

File it as a GitHub issue in this repository, following the Defect template in
.github/ISSUE_TEMPLATE/defect.yml:
1. Derive the key <repo>:<path/to/file>::<symbol>:<shape> from WHAT BROKE, not from
   my wording. The shape comes from the closed list in kit/ex5/failure-shapes.md.
   For a skill, prompt or workflow, the symbol is the section heading.
2. Before creating anything, search every issue, open and closed:
   gh issue list --state all --search "<key> in:body"
   If one exists, comment on it with the new evidence instead, and stop there.
3. Otherwise create it with gh issue create --label defect, and a body with the
   template's sections: Key, What broke, Reproduce (commit, exact command, expected /
   actual, anchor), Evidence (verbatim output, never a paraphrase), Severity (S1-S4).
Show me the key and the full gh command, and wait for my OK before running it.
```

**Then file one of them twice**, in the **same copy** of the repository: the search
only sees the issues of the repository it runs in. Open a **second** session there
(`/exit`, then `claude`, or a second terminal). Your teammate, at your keyboard,
pastes the same prompt and describes the **same** defect in **different words**.

**Expect:** the second filing finds the first issue and comments on it. If it opens a
new issue instead, the key was written from the description, not from what broke:
compare the two keys.

### 2 · Write the repair routine's prompt, and run it once by hand

Open `kit/ex5/repair-routine.md` in your editor and change what your team disagrees
with. Then, **in a new session**:

```text
Read kit/ex5/repair-routine.md and follow the prompt in its text block exactly, as if
you were the routine, with <N> = 1. Print the ordered list of issues before touching
any code.
```

**Watch:** does it take the first issue of the list it printed, or the easiest one?

### 3 · Write the merge policy as rules

This one is a **team discussion**, not a prompt: the decisions are the exercise. Open
`kit/ex5/merge-policy.md` and fill in the three columns together. Decide, out loud:

- Which checks can only be written in the first column, where they persuade? Which
  can move to the second column, where GitHub refuses?
- What is the highest severity a routine may merge without a person?
- In your copy, who is the code owner, and who is the routine? (Read "The trap in a
  copy that only you own" before you answer.)

Once the worksheet is filled in:

```text
Turn the filled-in worksheet in kit/ex5/merge-policy.md into the final merge routine
prompt: start from its prompt starter, and make every rule in the first column a
numbered check. Keep "Never use --admin" and "Never approve a pull request".
Write it into the same file, under a heading "Merge routine · final prompt".
```

### 4 · Decide what stays human

As a team, list the paths no routine may merge without a person. Then:

```text
Add these paths to .github/CODEOWNERS, owned by the user already named there:
<your paths>
Commit on a new branch and open a pull request. Do not merge it.
```

If your team is behind, skip the hand run in step 2. Do not skip the merge policy.

## Scheduling it (if your plan has routines)

`/schedule` needs a **subscription login**. With `ANTHROPIC_API_KEY` set in your
shell, it is not offered: run both prompts by hand in a session instead, which is
what the steps above did.

The repair routine, on a schedule of an hour or more, off the hour:

```text
/schedule every night at 02:17, on this repository. The routine's prompt is the text
block of kit/ex5/repair-routine.md with <N> = 2: read the file here and copy that
text into the routine word for word.
```

The merge routine, on the pull request label `reviewed`, which `review.yml` adds when
a review has run:

```text
/schedule a routine on this repository. Its prompt is the "Merge routine · final
prompt" in kit/ex5/merge-policy.md: read the file here and copy that text into the
routine word for word. Trigger it on the GitHub event pull request labeled, filtered
to the label reviewed. It has no schedule.
```

The Claude GitHub App you installed for the review is also what delivers that event
to the routine. If the terminal cannot add the GitHub trigger, add it on the
routine's page at claude.ai/code/routines. A routine starts from a fresh clone of
`main`: the prompt travels inside the routine, but the code it works on is whatever
`main` holds.

## Watch for

- The duplicate becomes a new issue the first time: the key was written from the
  description, not from what broke.
- Run by hand, the routine picks the easiest issue instead of the first one.
- A routine acts as **your** GitHub user. GitHub cannot tell the PR it opened from
  the merge it makes. Put the separation where GitHub can see it.
