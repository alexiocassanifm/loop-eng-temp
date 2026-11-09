# Failure shapes

The last part of a defect's key: `<repo>:<path/to/file>::<symbol>:<shape>`. Pick
the one that describes **what broke**, not how you found it. A closed list is what
lets two people who describe the same defect in different words land on the same
key.

| Shape | What it means | Example |
|---|---|---|
| `wrong-output` | Returns a value, and the value is wrong | a receipt prints `24.5 EUR` |
| `crash` | Raises or exits non-zero where it should not | a checkout with an empty cart raises |
| `silent-exit` | Exits successfully having done nothing | a review job goes green and posted no comment |
| `wrong-status` | Reports a state of the world that is not the state of the world | a check says "passed" because it never ran |
| `stale-read` | Reads a source that cannot see the whole truth, then answers as if it could | a dedup search that only reads open issues |
| `doc-contradiction` | The documentation and the behaviour disagree | a handout says a command keeps your changes, and it discards them |
| `flaky` | Passes and fails on the same input | a test that depends on the clock |
| `perf` | Correct, but unacceptably slow or wasteful | a loop polling every minute for a two-minute pipeline |
| `coverage-gap` | Nothing is wrong in the code; the rule that should have caught it does not exist | no test would fail if discount codes were deleted |

For a skill, a prompt or a workflow, the anchor is the file and its section heading:
`.claude/skills/review-loop/SKILL.md::How to wait:silent-exit`.

The key **groups** defects rather than identifying one: two unrelated defects in one
symbol with the same shape share a key. That is the trade, and it covers the case
that actually happens: the same defect, found twice.
