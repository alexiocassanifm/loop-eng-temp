# Loop engineering workshop

The exercises for **Loop Engineering with Claude Code**, a FairMind Academy workshop.
Five loops, each built on the one inside it, and one exercise on what a run carries
over to the next:

| Exercise | Loop |
|---|---|
| 1 · [Watch the loop you already run](kit/ex1.md) | the agentic loop: model, tool, result |
| 2 · [Put a clock on it](kit/ex2.md) | `/loop`: repetition on a clock |
| 3 · [Same task, two evaluators](kit/ex3.md) | `/goal`: an exit the maker does not judge; `/fairmind-loop` as an advanced track |
| 4 · [Write your own review loop](kit/ex4.md) | the pull request review loop |
| 5 · [Close the loop on today](kit/ex5.md) | dogfooding: defects → nightly repair → merge |
| [What the next run knows](kit/memory.md) | memory: what a new run starts with |

Everything runs on `shop/`, a checkout small enough to read in five minutes.
Amounts are integer cents; `python3 -m shop` prints a receipt.

## What you need

- A **GitHub account**.
- **Access to Claude**, one of:
  - an **Anthropic API key**, from the credits your facilitator gives you; or
  - a **Claude subscription** (Pro, Max, Team or Enterprise).

  Routines (`/schedule`, the optional part of exercise 5) need a subscription login;
  with an API key only, you run the same prompts by hand, which the exercise expects.
- macOS, Linux or Windows. On Windows, use PowerShell, with
  [Git for Windows](https://git-scm.com/downloads/win) installed: Claude Code runs its
  hooks and shell commands through the Git Bash it brings.

**On Windows**, type `py workshop` wherever these pages say `./workshop`, and `py`
where they say `python3`. Everything else is the same: the prompts you paste into
Claude Code, `git`, `gh` and `claude` do not change.

**Not yet tested on Windows: exercise 3, run 2** (the advanced track). The
`fairmind-coding` plugin runs its loop gate as `python3` inside Git Bash, and a Python
installed from python.org or with `winget` is called `python` and `py` there, not
`python3`. `./workshop doctor` checks it on Windows. If it shows `·`, do run 2
alongside someone on macOS or Linux.

## Before the workshop · 15 minutes

Do this the day before.

1. **Make your own copy.** On GitHub, **Use this template → Create a new repository**,
   in your own account. Do not fork this repository and do not clone it directly:
   your pushes, and the GitHub Actions they start, belong on your copy. Then clone
   your copy and `cd` into it.
2. **Install the tools:** [Claude Code](https://claude.com/claude-code),
   [GitHub CLI](https://cli.github.com) then `gh auth login`, git, Python 3.10 or
   later, and `python3 -m pip install pytest`. On Windows, in PowerShell:

   ```powershell
   winget install Anthropic.ClaudeCode
   winget install Git.Git
   winget install GitHub.cli
   winget install Python.Python.3.12
   py -m pip install pytest               # in a new terminal, after the installs
   ```

   Log Claude Code in with your subscription, **or** give it the API key in the
   terminal you will work in (every new terminal needs it again):

   ```bash
   export ANTHROPIC_API_KEY=<your key>          # macOS, Linux
   $env:ANTHROPIC_API_KEY = "<your key>"        # Windows PowerShell
   ```

3. **Trust your copy.** In the folder of your copy, run `claude` once, answer **yes**
   to the question about trusting the folder, then type `/exit`. Until you do, Claude
   Code ignores `.claude/settings.json`, which pre-approves the test and `git`/`gh`
   commands the exercises run, and `/goal` (exercise 3) is not available.
4. **Check:**

   ```bash
   ./workshop doctor      # every line under "tools" should be ✓   (Windows: py workshop doctor)
   ```

   Lines marked `·` belong to the sections below; they are not needed yet.

## Only for exercises 4 and 5

Make the copy **public**: branch rulesets, which exercise 5 uses, need a public
repository or a paid plan. Your exercise work will be visible.

1. **Let Claude review your pull requests.** Two things, both on your copy:
   - install the [Claude GitHub App](https://github.com/apps/claude) and give it
     access to your copy: the review posts through it;
   - give the review its credential, **one** of:

     ```bash
     gh secret set ANTHROPIC_API_KEY             # the API key; paste it when asked
     # or, on a subscription:
     claude setup-token                          # prints a long-lived token
     gh secret set CLAUDE_CODE_OAUTH_TOKEN       # paste it when asked
     ```

2. **Check, then set up:**

   ```bash
   ./workshop doctor      # the "exercises 4 and 5" lines should be ✓
   ./workshop setup       # labels, CODEOWNERS, the main ruleset
   ```

   `setup` commits one change to your `main` (it puts your username in
   `.github/CODEOWNERS`) and pushes it, then turns on the ruleset. Run it once. The
   GitHub App `doctor` cannot see, so check that one by hand.

## Only for the advanced track, exercise 3 run 2

Install `jq`, then the plugin (on Windows: `winget install jqlang.jq`). Inside Claude
Code:

```
/plugin marketplace add FairMind-Gen-AI-Studio/fairmind-plugins-public
/plugin install fairmind-coding@fairmind-plugins
```

## During the workshop

Each exercise starts from a clean branch:

```bash
./workshop reset ex2        # ex1, ex2, ex3-goal, ex3-loop, memory, ex4, ex5
```

It asks before discarding uncommitted changes, and builds the exercise on top of
your own `main`, so the pull requests you open go to your copy.

## What is in here

| Path | What |
|---|---|
| `shop/`, `tests/` | the application and its tests (`python3 -m pytest`) |
| `kit/` | one handout per exercise, `kit/memory.md` for the memory exercise, and `kit/ex5/` for the dogfooding exercise |
| `.github/workflows/ci.yml` | tests plus a clearly labelled simulated slow stage, about two minutes |
| `.github/workflows/review.yml` | Claude reviews every pull request, then labels it `reviewed` |
| `.github/ISSUE_TEMPLATE/defect.yml` | a defect with a stable key and a Reproduce block |
| `.github/CODEOWNERS`, `.github/rulesets/main.json` | the paths that stay human, and what GitHub enforces |
| `.claude/settings.json` | the commands the exercises may run without asking: tests, `git`, and the `gh` verbs that read or comment. Merging and raw API calls still ask |
| `.claude/settings.json` | the commands the exercises may run without asking: tests, `git`, and the `gh` verbs that read or comment. Merging and raw API calls still ask |
| `.claude/skills/review-loop/` | the skill you write in exercise 4 |
| `scripts/fake_deploy.py` | the fake production log for exercise 2 |
| `scripts/check_percent.py` | the check the Stop hook runs in the memory exercise |
| `workshop` | `doctor`, `setup`, `reset`, `events`, `hook`, `deploy` |

## If something goes wrong

| Symptom | Cause and fix |
|---|---|
| `./workshop doctor` shows ✗ | the line after the arrow says what to install or run; `·` lines are for later |
| Claude asks permission for every test or `git` command | the folder is not trusted: run `claude` there once and answer yes |
| `./workshop` does nothing on Windows | type `py workshop …` instead |
| `claude` says Git Bash was not found (Windows) | install Git for Windows, then open a new terminal |
| Claude asks permission for every test or `git` command | the folder is not trusted: run `claude` there once and answer yes |
| `./workshop` does nothing on Windows | type `py workshop …` instead |
| `claude` says Git Bash was not found (Windows) | install Git for Windows, then open a new terminal |
| `reset` says it could not start an exercise | your `main` has diverged from the template's; ask the facilitator |
| the review check is green and nothing was posted | it ran for ~15 s: the workflow file differs from `main`'s, or the app is not installed on your copy |
| the review check is red: no review credential | `gh secret set ANTHROPIC_API_KEY` on your copy (or the subscription token) |
| `/fairmind-loop` asks about a Fairmind workspace | answer **no**: the loop runs without one |
| `setup`: ruleset not created | your copy is private on a free plan; make it public |

## Two things that will bite

- **Edit `.github/workflows/review.yml` on `main` only.** The review action refuses to
  run when its workflow file differs from the default branch, and then exits green
  having reviewed nothing.
- **The routines act as you.** Anything a routine commits, opens or merges carries
  your GitHub identity. Exercise 5 is about what that means for a merge policy.
