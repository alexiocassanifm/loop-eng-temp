# Exercise 1 · Watch the loop you already run

**10 minutes · ring 1, the agentic loop · branch: `./workshop reset ex1`**

One prompt to Claude Code goes around a loop many times: the model asks for a tool,
the harness runs it, the result goes back in, until the model answers without asking
for a tool. Claude's documentation calls each time around the loop a **turn**. Here
you count those turns, then make the harness record them for you.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

## The task

`python3 -m shop` prints a receipt with amounts like `24.5 EUR`. Money should always
show two decimals: `24.50 EUR`.

## Steps

### 1 · Start clean

```bash
./workshop reset ex1
```

**Expect:** `on branch ex1-work, starting point of ex1`.

### 2 · Run the task headless, streaming every event to a file

One line: copy all of it.

```bash
claude -p "Receipts must always show two decimals, like 24.50 EUR. Fix it and add a test." --output-format stream-json --verbose --permission-mode acceptEdits > run.jsonl
```

It prints nothing for a minute or two: every event goes into `run.jsonl`.
`--verbose` is required, because in print mode stream-json refuses without it.
`--permission-mode acceptEdits` lets it edit files; the test commands it runs are
pre-approved in `.claude/settings.json`.

### 3 · Count the tool calls, and the turns

```bash
./workshop events run.jsonl
```

**Expect:** the run turn by turn, each with the tool calls it asked for (`Bash`,
`Read`, `Edit`…), then the totals and the last message Claude wrote. One turn is the
model answering once. One answer can ask for several tools, so there are usually
fewer turns than tool calls.

### 4 · Make the harness log every tool call

```bash
./workshop hook
```

It writes `.claude/settings.local.json` and prints it. **Read it before going on:** a
`PostToolUse` hook with matcher `*` runs a command after every tool call. The hook gets
the event as JSON on its stdin; the command appends the event's `tool_name` to
`tool-log.txt`. The file only ever grows: every run, and every interactive session
while the hook is on, adds its lines after the ones already there. It is gitignored
and `./workshop reset` removes it.

Put the code back the way it was, so Claude has the same work to do again, and empty
the log, so it shows this run alone:

```bash
git stash -u
./workshop clear-log
```

Run the step 2 command again, then compare what the hook saw with what the stream
recorded:

```bash
./workshop events run.jsonl
```

Open `tool-log.txt` in your editor, next to that output.

**Expect:** the same tools in the same order, **or fewer**. The hook fires on
successful calls only; a call that fails, marked `FAILED` in the list, fires
`PostToolUseFailure`, which this hook does not listen to.

### 5 · Find the moment it decided to stop

```bash
claude
```

```text
Open run.jsonl. It is the event stream of a headless Claude Code run. Find the last
assistant message that contains no tool_use block and quote it. Then tell me what
decided that the loop should end there: a test, a hook, a limit, or the model
itself?
```

## Variant · make the hook catch the failures too

In the same session:

```text
Add a PostToolUseFailure hook to .claude/settings.local.json that runs exactly the
same command as the PostToolUse one. Then tell me why PostToolUse alone missed the
failed calls.
```

Exit Claude Code, then run `git stash -u`, `./workshop clear-log` and the step 2 command
again, and read `tool-log.txt`.

## Watch for

- How many turns read and how many write.

## What to take away

Claude Code is already a loop, and the model alone decides when it ends. If it ran
the tests, it chose to, and it read the result itself. A hook is code the harness runs
whatever the model thinks: ring 3 uses that to give the loop an exit the model does
not judge.
