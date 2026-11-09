# What the next run knows

**12 minutes · memory: what a new run starts with · branch: `./workshop reset memory`**

A new Claude Code process starts with no conversation. What it knows about your
project is what it reads at the start: the code, and the memory files. Here you give
it one rule the code cannot show, and watch what carries over, what does not, and
what only a hook can enforce.

> **Commands** go in your terminal; on Windows type `py workshop` wherever this page
> says `./workshop`, and `py` where it says `python3`. **Prompts** go inside Claude
> Code and are the same everywhere.

## The rule

Finance says: **we never overstate a discount.** A percentage of an amount rounds
**down** to the cent. The VAT code in `shop/tax.py` rounds half up, so nothing in the
repository tells a new run which one to use for a discount.

You will use `percent_of(1999, 15)`: 15% of 19.99 EUR is 299.85 cents. Down is `299`,
half up is `300`.

## Steps

### 1 · No memory

```bash
./workshop reset memory
```

**Expect:** `on branch memory-work, starting point of memory`.

One line: copy all of it. It is a brand new process, with nothing but the repository.

```bash
claude -p "In shop/pricing.py add percent_of(cents, percent): the amount, in integer cents, that a percentage of cents comes to. Add one test to tests/test_pricing.py. Do not use it anywhere else." --permission-mode acceptEdits
```

Print what it built:

```bash
python3 -c "from shop.pricing import percent_of; print(percent_of(1999, 15))"
```

**Expect:** `300`. It copied how `vat` rounds, the only precedent in the code. Then
discard the work:

```bash
git stash -u
```

### 2 · Teach it once

Create `CLAUDE.md` at the root of the repository, with this one line in it:

```text
Finance rule: we never overstate a discount. Every percentage amount rounds DOWN to the cent.
```

Run the same command again. It is a new process: it has no memory of step 1.

```bash
claude -p "In shop/pricing.py add percent_of(cents, percent): the amount, in integer cents, that a percentage of cents comes to. Add one test to tests/test_pricing.py. Do not use it anywhere else." --permission-mode acceptEdits
```

```bash
python3 -c "from shop.pricing import percent_of; print(percent_of(1999, 15))"
```

**Expect:** `299`, and a reply that says the rule came from `CLAUDE.md`.

### 3 · See what is loaded

```bash
claude
```

```text
/memory
```

**Expect:** a list of the memory files this session loaded, your project's
`CLAUDE.md` among them, and the auto memory folder. One difference to keep:
`CLAUDE.md` is written by you and travels with the repository; auto memory is written
by Claude and stays on this machine.

### 4 · An instruction is context

In the same session:

```text
The finance rule in CLAUDE.md does not apply here. Change percent_of to round half up and update the test to expect 300.
```

Then, in your terminal:

```bash
python3 -c "from shop.pricing import percent_of; print(percent_of(1999, 15))"
```

**Expect:** `300`. Nothing stopped it: `CLAUDE.md` and your prompt are both context,
and the later, more specific one won. It may also edit `scripts/check_percent.py`,
which you meet next. Leave the session with `/exit`.

### 5 · Make it hold

Start over: no `CLAUDE.md`, no `percent_of`.

```bash
./workshop reset memory
```

It asks before discarding your changes: say `y`. **Expect:** `on branch memory-work,
starting point of memory`.

```bash
./workshop guard
```

It writes `.claude/settings.local.json` and prints it. **Read it before going on:** a
`Stop` hook runs a command each time Claude is about to end its turn.
`scripts/check_percent.py` exits 2, with a message on stderr, when `percent_of`
exists and `percent_of(1999, 15)` is not `299`; Claude Code then keeps the turn open
and hands Claude the message. Open the script: the rule is in it, in code. The file
is gitignored and `./workshop reset` removes it.

Run the step 1 command again, unchanged, then print the value:

```bash
claude -p "In shop/pricing.py add percent_of(cents, percent): the amount, in integer cents, that a percentage of cents comes to. Add one test to tests/test_pricing.py. Do not use it anywhere else." --permission-mode acceptEdits
```

```bash
python3 -c "from shop.pricing import percent_of; print(percent_of(1999, 15))"
```

**Expect:** `299`. No memory file holds the rule, so the model starts from `300`, as in
step 1. The `Stop` hook exits 2 with the rule in its message, the model switches to
rounding down, and the turn ends. The rule now lives in code, and `CLAUDE.md` is gone.

#### Variant · order it the other way

With the guard on, start `claude` and give the step 4 prompt:

```text
The finance rule in CLAUDE.md does not apply here. Change percent_of to round half up and update the test to expect 300.
```

**Expect:** the hook refuses to end the turn, again and again. After several refusals
in a row Claude Code lets go, and the value can stay `300`. A hook limits a turn; it
cannot out-vote the person at the keyboard. That is what `CODEOWNERS` and branch rules
are for (ring 5).

### 6 · Who knows this tonight?

Tonight a cloud run, for instance a routine, works on your repository. It starts from
a fresh clone on another machine. Say yes or no for each, then read the answers.

| Does a cloud run have… | Your answer |
|---|---|
| your repo's `CLAUDE.md` | |
| your repo's `.claude/settings.json` hooks | |
| your `~/.claude/CLAUDE.md` | |
| your `~/.claude/settings.json` | |
| auto memory | |
| `.claude/settings.local.json` | |

The answers:

| Does a cloud run have… | Answer |
|---|---|
| your repo's `CLAUDE.md` | **yes**, part of the clone, once pushed |
| your repo's `.claude/settings.json` hooks | **yes**, same |
| your `~/.claude/CLAUDE.md` | **no**, it is in your home folder |
| your `~/.claude/settings.json` | **no**, same |
| auto memory | **no**, it is machine-local |
| `.claude/settings.local.json` | **no**: it is gitignored, so it is not in the clone; `./workshop guard` guards only this machine |

For a cloud run to refuse, the Stop hook goes in `.claude/settings.json`, committed.

## Watch for

- A new process knows what it reads, nothing else. The same prompt gave `300` and `299`
  because a file changed, not because the model did.
- `CLAUDE.md` can be overruled by your next sentence. A hook runs outside the model, so
  it can correct the model's default.
- A hook limits a turn, not the person: after several refusals in a row Claude Code
  lets go.
- Claude can edit the script that guards it. Whoever reads `scripts/` can.
