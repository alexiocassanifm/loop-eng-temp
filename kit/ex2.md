# Exercise 2 · Put a clock on it

**15 minutes · ring 2, `/loop` · branch: `./workshop reset ex2`**

`/loop` repeats a prompt: on a fixed interval (`/loop 2m …`) or at a pace Claude picks
after each iteration (`/loop …`, one minute to one hour). A loop on a fixed interval
never ends by itself. A self-paced loop ends when Claude decides the job is done, **if
your prompt says what done means.** Claude's documentation calls each repetition an
**iteration**, and one iteration holds the many turns you counted in exercise 1.

You run two loops **at the same time**, each in its own terminal. Each one spends
most of its life waiting.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`. **Prompts** go inside Claude Code and are the same everywhere.

## Loop A · watch a pipeline until it is green

This branch has a bug that makes CI fail. The pipeline takes about two minutes.

**Terminal 1:**

```bash
./workshop reset ex2
git push -u origin ex2-work
claude
```

The push starts CI. Paste this in Claude Code:

```text
/loop Watch the CI run of branch ex2-work. Each iteration, run:
gh run list --branch ex2-work --workflow CI --limit 1
- Still queued or in progress: say "waiting", nothing else, and check again in about
  two minutes.
- Failed: read why with gh run view <run id> --log-failed, fix the cause in the code,
  run the tests, then commit and push. The push starts a new CI run.
- Succeeded, on the commit that is at the tip of ex2-work: tell me how many iterations
  this loop took and what you fixed, then stop the loop. Do not check again.
```

**Expect:** a few `waiting` iterations, one fix and push, more `waiting`, then a
summary and the loop ends. Count the iterations.

### Variant · forget the stop

Once Loop A has ended, try the same watch with a fixed interval and **no stop rule**:

```text
/loop 1m Run gh run list --branch ex2-work --workflow CI --limit 1 and tell me the
status of the latest run.
```

Let it fire three times after the run is green. Every iteration costs tokens and tells
you the same thing. Then stop it. A fixed-interval loop does not stop itself, and
`Esc` only stops self-paced ones:

```text
What scheduled tasks do I have? Cancel the CI status one.
```

## Loop B · a fix going to production

**Terminal 2:** start the fake production log. It writes one line a minute, and a
regression comes later. Leave this terminal running.

```bash
./workshop deploy
```

**Terminal 3:**

```bash
claude
```

```text
/loop Watch deploy.log: a fix just went to production, and the log gets one line per
minute. Each iteration, read only the lines added since the previous one.
- Every new line says status=ok: say "quiet", then wait longer than last time before
  the next check: 1 minute, then 2, then 5, then stay at 5.
- Any new line says status=degraded: tell me the minute and the error_rate, and go
  back to checking every minute.
- Once the log has reached minute=20: summarise what you saw and stop the loop.
```

In the room, minutes stand in for hours.

**Expect:** the waits get longer while the log is quiet, drop back to one minute
around `minute=7`, and get longer again once the regression is over.

### Variant · a clock with no judgement

```text
/loop 1m Read the last line of deploy.log and tell me the status.
```

Count how many answers in a row are identical. Then cancel it as in Loop A.

## Watch for

- The forgotten stop: the loop keeps firing after the pipeline is green, and every
  iteration is paid for.
- The interval: one minute feels responsive and mostly buys identical answers.
- These loops die with your session. Which of these watches should have been a
  routine (`/schedule`), which keeps running with the laptop closed?
