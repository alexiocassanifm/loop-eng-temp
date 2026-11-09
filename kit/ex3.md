# Exercise 3 · Same task, two evaluators

**15 minutes for the core, run 1 · ring 3, `/goal`. Run 2 and Compare: advanced, optional, +15 minutes**

One task. The exit condition is judged by a model reading the session (`/goal`). In
the advanced track it is then judged by checks that run (`/fairmind-loop`), and you
compare what each one accepted as done.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

## Run 1 · `/goal`

```bash
./workshop reset ex3-goal
claude
```

Paste the goal. It is one condition, taken from `TICKET.md`, and it starts the work
straight away: the condition is also the instruction.

```text
/goal TICKET.md is implemented with tests for what it asks: discount codes work as TICKET.md describes and the test suite passes
```

Claude keeps working until the goal's evaluator, a small model reading the
conversation, judges the condition met. When it stops:

```text
Commit your work on this branch with the message "DISC-1 via /goal". Then list, in
one line each, every case you tested. For FREE100, say whether the order still pays
for shipping.
```

**Keep this answer:** it is what `/goal` accepted as done. Then `/exit`.

## The end of the core path

`TICKET.md` never says what `FREE100` does to shipping. `/goal`'s evaluator judged
from the conversation and ran nothing. So who decided what `FREE100` does to
shipping?

That question is the point of run 1. Write your answer down before you go on.

---

## Advanced (optional) · Run 2 · `/fairmind-loop`

Needs the plugin, see README.

```bash
./workshop reset ex3-loop
claude
```

Same code and same ticket as before your run 1, plus a prepared contract: a brief
(`.fairmind/design/DISC-1.md`) and checks (`.fairmind/gate/`). Paste:

```text
/fairmind-loop DISC-1
The brief is .fairmind/design/DISC-1.md and the checks are .fairmind/gate/. Use them
as they are: do not write new checks and do not edit these. I have no Fairmind
workspace. Keep the budget at six iterations. Stop at the first green evaluation.
```

It asks questions as it goes. The answers:

| If it asks… | Answer |
|---|---|
| whether you have a Fairmind workspace, or for a project or session | **no**, the loop runs on git, python3 and bash alone |
| whether to write or generate checks | **no**, use the prepared ones |
| to fix or replace a quarantined check | **no**, leave it quarantined |
| the budget | **six iterations** |
| to continue past the first green evaluation | **no**, stop there |

### 1 · Read the brief before the checks

While it prepares, open `.fairmind/design/DISC-1.md` in your editor. The brief says
what to build; the checks only say what is measured. Find the sentence the ticket
never says.

### 2 · Watch admission quarantine a check

One check is badly written on purpose. When the loop reports admission, ask:

```text
Which check did admission quarantine, and why? Quote the reason recorded in
.fairmind/loop-state.json, and tell me what a check has to do to be admitted.
```

### 3 · Let the gate refuse at least once

**Expect:** at least one red evaluation, where the gate names the check that failed,
then a fix, then a green evaluation. The exercise ends at the first green
(`confirmation 1/3`). Reaching `passed_pending_human` takes three greens and a
completeness review: that is the overflow, not the exercise.

## Advanced (optional) · Compare

In the same session:

```text
Run the checks in .fairmind/gate/ against the code on branch ex3-goal-work, the
/goal run. Use a temporary git worktree for it and remove it afterwards. Which checks
fail there? For each one, say what the brief asked for and what that code does.
```

What did the goal accept that the gate refused? The ticket hides one edge case.
Which run caught it?

## Watch for

- The reset between the runs is not optional: on code `/goal` already changed, every
  check passes before the loop starts, admission quarantines all of them, and the
  loop refuses to arm.
- Editing a check instead of the code: admission refuses that too.
