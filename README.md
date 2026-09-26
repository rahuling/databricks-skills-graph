# Databricks Skills Knowledge Graph

An interactive prerequisite graph of Databricks certification skills. Every certification
decomposes into a graph of sub-skills connected by prerequisite / correlation edges. Learners
can traverse it top-down (goal → required sub-skills) or bottom-up (what I know → what unlocks
next), take practice questions to place themselves, and follow a gamified loop — XP per skill,
day streaks, badges, and a "shortest path to any skill" roadmap.

> ⚠️ **Not an official Databricks product.** This is a community / enablement resource. Nodes are
> seeded from the **published** certification exam-guide domains, their percentage weightings, and
> Academy learning paths. Exam *objectives* are referenced; no confidential exam questions are used.
> Practice questions are original scenarios for self-placement only. Always verify against the
> [current official exam guides](https://www.databricks.com/learn/certification).

## What's in it

- **7 certification tracks** — Data Engineer Associate/Professional, Machine Learning
  Associate/Professional, Data Analyst Associate, Generative AI Engineer Associate, Platform
  Administrator — plus a shared Foundations layer.
- **79 skill nodes** across 19 product areas (Delta Lake, Unity Catalog, Lakeflow, MLflow,
  Vector Search, Databricks SQL, Genie, …), deduped so a skill shared by several certs is one
  node carrying every track that tests it.
- **103 typed prerequisite edges** — hard prerequisite, soft prerequisite, and "often learned
  together" — forming a validated DAG.
- **Exam weightings as importance signal.** Each node carries its exam-guide domain weight; XP is
  derived from it (`xp = max(50, round(weight% × 10))`).
- **Practice questions** on key nodes for self-placement (original scenarios).
- **Navigation layer over real content** — every node links out to docs.databricks.com pages and
  Databricks Academy on-demand courses.

## Run it

**`index.html` is fully self-contained** — the entire knowledge graph is embedded inline, so
there is no build step, server, or `data/` dependency to run it. Just:

```bash
open index.html          # double-click it, or drop it on any static host
```

Progress (mastered skills, XP, streak, badges) is saved in your browser's `localStorage` only —
nothing is sent anywhere. Use **Reset progress** to clear it.

### Host it

Because it's one file, hosting is trivial — commit it and enable **GitHub Pages** on the `main`
branch (root), and it's live at `https://<user>.github.io/databricks-skills-graph/`. Or drop
`index.html` on any static host / intranet share.

## How to use the graph

| Action | What it does |
|---|---|
| **Track dropdown** | Filter the graph to one certification (or *All tracks* for the full map). |
| **Graph / List toggle** | Force-layered DAG view, or a ranked checklist per track. |
| **Click a node** | Open its detail drawer: summary, exam domain, prerequisites, what it unlocks, learning links, and a practice question. |
| **Start learning / Mark mastered** | Track your status. Mastering banks XP, advances your level, and can unlock badges. |
| **🧭 Path** | Highlights the shortest chain of prerequisites you still need to reach that skill. |

Node status: **mastered** (green ✓) · **learning** (amber) · **available** — all hard prereqs met
(blue) · **locked** (grey 🔒).

## Live site

Deployed to GitHub Pages at **https://rahuling.github.io/databricks-skills-graph/** by
[`.github/workflows/pages.yml`](.github/workflows/pages.yml) on every push to `main`. The workflow
reruns `build_graph.py` (so the DAG is re-validated and `index.html` is rebuilt from source) and
publishes:

| URL | Source |
|---|---|
| `/` | `landing.html`: landing page (stats, track cards, area coverage, animated graph preview), rendered live from `data/graph.json` |
| `/app.html` | `index.html`: the interactive graph. `app.html?track=<id>` (or `?track=all`) opens a specific track |
| `/data/graph.json` | Raw graph export |
 Pull requests run the build as a check without
deploying.

One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Editing / extending the graph

[`build_graph.py`](build_graph.py) is the source of truth. It holds the node/edge definitions
and the node→Academy-course mapping, validates node IDs, edge references, and that the edges form
a DAG (no cycles), then **regenerates the self-contained `index.html`** by injecting the graph
inline into [`index.template.html`](index.template.html). It also writes `data/graph.json` as a
raw export.

```bash
python3 build_graph.py   # -> data/graph.json  and  index.html (self-contained)
```

To add a skill, add an `n(...)` call and map it to an Academy course in `NODE_COURSE`; to add a
relationship, add an `e(from, to, type)`; then rerun the builder. See
[`data/schema.md`](data/schema.md) for the full data model.

## Files

| File | Role |
|---|---|
| `index.html` | The self-contained app (generated). Open or host this. |
| `landing.html` | GitHub Pages landing page (reads `data/graph.json`; served at `/`). |
| `index.template.html` | App shell (HTML/CSS/JS) with a `<!--__GRAPH_DATA__-->` inject point. |
| `build_graph.py` | Source of truth: node/edge/course definitions → builds `index.html` + `graph.json`. |
| `data/graph.json` | Raw graph export (nodes, edges, tracks, areas). |
| `data/schema.md` | Data-model reference. |

## Roadmap

- Expand practice questions to a full diagnostic per track (placement testing).
- SME validation pass on edges with Academy / product teams.
- Deep-link nodes to specific Academy *modules/videos* rather than course landing pages (today
  each node links to its on-demand course page).
- Optional leaderboard / shared progress (would need a backend — currently intentionally
  serverless and private).

## License

MIT — see [LICENSE](LICENSE). Databricks, Delta Lake, Unity Catalog, Lakeflow, MLflow, Mosaic AI
and related marks are trademarks of Databricks, Inc.; this project is not affiliated with or
endorsed by Databricks.
