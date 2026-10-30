# demo-big-epic

**Demo:** hand an AI team a big epic. An architect asks the design questions, a planner
creates the Jira tickets, and a builder ships a stack of merge requests.

The code is a tiny todo app (`todo.py`, `cli.py`, tests). The shared agents and skills come
from [`agent-hub`](https://github.com/rutansh/agent-hub) through APM.

## Setup (once)

```bash
brew install apm
gh auth login            # agent-hub is private
apm install              # pulls the agents and skills pinned in apm.lock.yaml
uv sync && uv run pytest # 6 tests pass
```

## Credentials (optional, for the full flow)

The agents use three CLIs. Put your own credentials in a git-ignored `.env` file:

```bash
cp .env.example .env     # then open .env and fill in the tools you use
source .agents/skills/connect-tools/scripts/connect.sh   # loads .env and checks each tool
```

| Tool | Why | Variables in `.env` | Install |
| --- | --- | --- | --- |
| `acli` | Create real Jira tickets | `JIRA_SITE`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY` | [Atlassian CLI](https://developer.atlassian.com/cloud/acli/guides/update-install-guide/) |
| `glab` | Stacked MRs on GitLab | `GITLAB_TOKEN`, `GITLAB_HOST` | `brew install glab` |
| `gh` | Chained PRs on GitHub | `GH_TOKEN` | `brew install gh` |

You do not need to run the script yourself: `start-task` runs the `connect-tools` skill at
the start of an epic and tells you what is missing. `.env` is ignored by git and by Cursor.
Never paste tokens into the chat.

Without credentials the agents fall back (tickets written to a markdown file; chained PRs
via `gh` for GitHub repos) and tell you they did.

## The demo

Open this folder in Cursor and type:

> Use start-task. I want to add team workspaces: users can create a workspace, invite
> teammates, share task lists, and get notified when a shared task is completed.

What should happen:

| Step | Who | What you see |
| --- | --- | --- |
| 1 | `start-task` | Asks **small feature or big epic?** Answer: **big epic**. Asks for the Jira project key. |
| 2 | `architect` | Reads the code, then asks design questions (data model, permissions, how notifications are delivered, storage). Writes `docs/epics/team-workspaces/design.md`. |
| 3 | `planner` | Splits the design into small tasks, shows the list for approval, creates the Jira epic and child tickets, writes `plan.md`. |
| 4 | `builder` | Implements each task with tests, saves each as one diff, shows the stack, and after approval opens the chain of MRs. |

You approve at the end of every phase.

## Files the agents create

```
docs/epics/team-workspaces/
  design.md     # architect output
  plan.md       # planner output, with Jira keys and task status
```

## What this shows

- Big work is designed before it is coded.
- Tickets and merge requests stay small and reviewable.
- The whole workflow installs into any repo with one `apm install`.

See also: [`demo-small-feature`](https://github.com/rutansh/demo-small-feature) for the
single-agent small feature flow.
