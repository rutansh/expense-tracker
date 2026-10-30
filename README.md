# expense-tracker

A basic command line expense tracker (`expenses.py`, `cli.py`, tests). It is a practice
codebase for the shared agents and skills in
[`agent-hub`](https://github.com/rutansh/agent-hub), which are installed here with APM.
Use it for **both** small features and big epics.

```bash
uv run python cli.py add 12.50 food --note "lunch"
uv run python cli.py list
uv run python cli.py summary
```

## Setup (once)

```bash
brew install apm
apm install              # pulls the agents and skills pinned in apm.lock.yaml
uv sync
uv run pytest            # 11 tests pass
```

After `apm install`:

```
.cursor/agents/    architect, planner, builder
.agents/skills/    start-task, implement-feature, jira-tickets, stacked-mrs, connect-tools, ...
```

## Credentials (only if you want agents to create tickets or open MRs)

Coding and testing need no credentials. Add your own to a git-ignored `.env` file:

```bash
cp .env.example .env     # fill in only the tools you use
source .agents/skills/connect-tools/scripts/connect.sh   # loads .env and checks the tools
```

| Tool | Used for | Variables |
| --- | --- | --- |
| `acli` | Jira tickets | `JIRA_SITE`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY` |
| `glab` | Stacked MRs on GitLab | `GITLAB_TOKEN`, `GITLAB_HOST` |
| `gh` | Chained PRs on GitHub | `GH_TOKEN` |

`.env` is ignored by git and by Cursor. Never paste tokens into the chat.

## Try it

Open this folder in Cursor and start every task the same way:

> Use start-task. <what you want>

The agent asks whether it is a **small feature** or a **big epic** and runs the matching flow.

### Small feature (one MR)

- "Add a `--category` filter to `list`."
- "Add a `delete` command for an expense by id."
- "Make `summary` also print the grand total."

Expected: the agent reads `expenses.py`, `cli.py` and `tests/`, writes tests first, implements
the change, runs `uv run pytest`, and asks before pushing anything.

### Big epic (design, tickets, stack of MRs)

- "Add monthly budgets per category with overspend alerts and a monthly report that can be
  exported as CSV."

Expected: `architect` asks design questions (where budgets live, how alerts are delivered,
report format) and writes `docs/epics/<slug>/design.md`; `planner` splits it into tasks and
creates the Jira tickets; `builder` implements each task and ships a stack of merge requests.
You approve at the end of each phase.

## Update the shared agents and skills

Change the version in `apm.yml` (for example `#v0.4.0`), then `apm install --update`.
