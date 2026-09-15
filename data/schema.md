# Data model — `graph.json`

The whole knowledge graph is one JSON document. `build_graph.py` writes it to
`data/graph.json` (raw export) **and** inlines the same object into the self-contained
`index.html`, so the app carries its own data. Keeping the graph as one adjacency-style
document (not Neo4j) is a deliberate MVP choice — diff-able in git, trivially portable,
and large enough to serve the full multi-track graph without a server.

```jsonc
{
  "meta": {
    "version": "1.0.0",
    "generated": "YYYY-MM-DD",
    "disclaimer": "..."             // sourcing / not-official note, shown in the UI
  },

  "tracks": [                        // one per certification
    {
      "id": "de-assoc",
      "name": "Data Engineer Associate",
      "level": "associate",          // associate | professional
      "family": "data-engineering",  // groups assoc+pro of the same discipline
      "certUrl": "https://…",
      "color": "#FF3621"
    }
  ],

  "areas": [                         // product areas — the graph's "columns"
    { "id": "unity-catalog", "name": "Unity Catalog", "color": "#1B3139" }
  ],

  "nodes": [
    {
      "id": "uc-access-controls",              // stable kebab-case key
      "label": "Configure Unity Catalog access controls",
      "area": "unity-catalog",                 // -> areas[].id
      "tracks": ["de-assoc", "platform-admin"],// every cert that tests this skill
      "level": "associate",
      "domain": "Databricks Tooling",          // exam-guide section it came from
      "weight": 15,                            // exam-guide domain weight % (importance signal)
      "xp": 150,                               // XP awarded on mastery (derived from weight)
      "summary": "One-line description of the skill.",
      "links": [                               // navigation layer over existing content
        // academy = the on-demand Databricks Academy course that teaches this skill
        { "type": "academy","title": "…", "url": "https://…", "free": true, "onDemand": true },
        { "type": "docs",   "title": "…", "url": "https://docs.databricks.com/…" }
      ],
      "assessment": [                          // ORIGINAL practice questions only — never real exam bank
        {
          "q": "…",
          "options": ["…", "…", "…", "…"],
          "answer": 0,                         // index into options
          "explain": "Why the answer is correct."
        }
      ]
    }
  ],

  "edges": [
    { "from": "delta-tables", "to": "delta-merge", "type": "hard" }
    // type: "hard"   — cannot learn `to` without `from`
    //       "soft"   — `from` helps but is not required
    //       "cooccur"— often learned together, no causal direction
  ]
}
```

## Rules

- **Node IDs are stable.** Renaming a label is fine; changing an `id` breaks edges and
  saved learner progress.
- **A skill is one node even when it appears in several certs.** Deduped across tracks;
  the `tracks` array carries every cert that tests it. This is what surfaces cross-track
  overlap (e.g. Delta Lake / Unity Catalog shared by DE and DA).
- **XP is derived, not hand-set:** `xp = round(weight × 10)`, floored at 50, so node
  reward tracks real exam importance rather than a guess.
- **Edges form a DAG.** No cycles — the app relies on topological ordering for
  "unlocked next" and "shortest path to cert".
- **Assessments are original.** Practice scenarios written for placement/gating only.
  Real certification exam questions are confidential and must never be used as source.
