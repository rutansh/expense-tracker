# demo-safety-desk

Demo project showing **selective install** of shared skills from
[`ai4pharma-skills`](https://github.com/rutansh/ai4pharma-skills) with APM.

Unlike `demo-trial-analyst` (which installs everything), this project only needs
one skill, so only `adverse-event-triage` is deployed.

```yaml
# apm.yml
dependencies:
  apm:
    - git: rutansh/ai4pharma-skills
      ref: v0.1.0
      skills:
        - adverse-event-triage
```

## Setup

```bash
brew install apm        # once per machine
gh auth login           # the skills repo is private; APM uses your GitHub auth
apm install             # deploys only the selected skill into .agents/skills/
```

## Try it

Open this folder in Cursor and ask the agent:

> Triage the cases in `data/ae-reports.md`

The agent should apply the `adverse-event-triage` skill: a priority-sorted table
(P1/P2/P3) plus the missing information needed for each P1/P2 case. Since no
reference safety document is provided, expectedness should be reported as
"unknown - reference document needed".

## Add another skill later

```bash
apm install rutansh/ai4pharma-skills --skill literature-review-brief
```

`--skill` is additive: it unions with the skills already pinned.

## Notes

- All data in `data/` is **fictional**, for demo purposes only.
- `apm.lock.yaml` is committed so everyone gets identical skills.
