#!/usr/bin/env python3
"""Build data/graph.json for the Databricks Skills Knowledge Graph.

The node / edge taxonomy is seeded from the PUBLISHED Databricks certification
exam guides (domain names + percentage weightings) and Academy learning paths.
Exam *objectives* are referenced; no confidential exam-question content is used.
Practice ("assessment") questions are original scenario questions written for
placement / gating only.

Run:  python3 build_graph.py   ->  writes data/graph.json
"""
import json, os, datetime

# ---------------------------------------------------------------- tracks -----
# family groups the associate + professional of one discipline.
TRACKS = [
    {"id": "foundations",    "name": "Foundations",                    "level": "foundational", "family": "core",  "color": "#64748B",
     "certUrl": "https://www.databricks.com/learn/training/lakehouse-fundamentals"},
    {"id": "de-assoc",       "name": "Data Engineer Associate",        "level": "associate",    "family": "data-eng", "color": "#FF3621",
     "certUrl": "https://www.databricks.com/learn/certification/data-engineer-associate"},
    {"id": "de-pro",         "name": "Data Engineer Professional",     "level": "professional", "family": "data-eng", "color": "#B31B1B",
     "certUrl": "https://www.databricks.com/learn/certification/data-engineer-professional"},
    {"id": "da-assoc",       "name": "Data Analyst Associate",         "level": "associate",    "family": "analytics", "color": "#00A972",
     "certUrl": "https://www.databricks.com/learn/certification/data-analyst-associate"},
    {"id": "ml-assoc",       "name": "Machine Learning Associate",     "level": "associate",    "family": "ml",     "color": "#2272B4",
     "certUrl": "https://www.databricks.com/learn/certification/machine-learning-associate"},
    {"id": "ml-pro",         "name": "Machine Learning Professional",  "level": "professional", "family": "ml",     "color": "#154D7A",
     "certUrl": "https://www.databricks.com/learn/certification/machine-learning-professional"},
    {"id": "genai-assoc",    "name": "Generative AI Engineer Associate","level": "associate",   "family": "genai",  "color": "#8B5CF6",
     "certUrl": "https://www.databricks.com/learn/certification/generative-ai-engineer-associate"},
    {"id": "platform-admin", "name": "Platform Administrator",         "level": "specialty",    "family": "admin",  "color": "#D97706",
     "certUrl": "https://www.databricks.com/learn/certification"},
]

# ------------------------------------------------------------- product areas -
AREAS = [
    {"id": "platform",     "name": "Platform & Compute",   "color": "#475569"},
    {"id": "delta",        "name": "Delta Lake",           "color": "#00A972"},
    {"id": "unity-catalog","name": "Unity Catalog",        "color": "#1B3139"},
    {"id": "ingestion",    "name": "Ingestion",            "color": "#0EA5E9"},
    {"id": "transform",    "name": "Transformation",       "color": "#FF3621"},
    {"id": "pipelines",    "name": "Declarative Pipelines","color": "#F97316"},
    {"id": "jobs",         "name": "Lakeflow Jobs",        "color": "#EAB308"},
    {"id": "cicd",         "name": "CI/CD & DABs",         "color": "#84CC16"},
    {"id": "observability","name": "Monitoring & Optimize","color": "#14B8A6"},
    {"id": "dbsql",        "name": "Databricks SQL",       "color": "#22C55E"},
    {"id": "dashboards",   "name": "Dashboards & BI",      "color": "#10B981"},
    {"id": "genie",        "name": "AI/BI Genie",          "color": "#06B6D4"},
    {"id": "mlflow",       "name": "MLflow",               "color": "#2272B4"},
    {"id": "ml-dev",       "name": "Model Development",    "color": "#3B82F6"},
    {"id": "features",     "name": "Feature Engineering",  "color": "#6366F1"},
    {"id": "serving",      "name": "Model Serving",        "color": "#0891B2"},
    {"id": "mlops",        "name": "MLOps",                "color": "#7C3AED"},
    {"id": "genai",        "name": "Generative AI",        "color": "#8B5CF6"},
    {"id": "admin",        "name": "Administration",       "color": "#D97706"},
]

NODES, EDGES = [], []

def n(id, label, area, tracks, level, domain, weight, summary, links, assessment=None):
    """weight = exam-guide domain % (None when not published). xp derives from it."""
    xp = 100 if weight is None else max(50, round(weight * 10))
    NODES.append({
        "id": id, "label": label, "area": area, "tracks": tracks, "level": level,
        "domain": domain, "weight": weight, "xp": xp, "summary": summary,
        "links": links, "assessment": assessment or [],
    })

def e(frm, to, type="hard"):
    EDGES.append({"from": frm, "to": to, "type": type})

D = "https://docs.databricks.com/"        # docs base
def docs(t, u):  return {"type": "docs",   "title": t, "url": D + u}
def acad(t, u):  return {"type": "academy","title": t, "url": u}
AC = "https://www.databricks.com/learn/training/catalog"

# ============================================================ FOUNDATIONS ====
n("lakehouse-fundamentals", "Lakehouse Fundamentals", "platform", ["foundations"], "foundational",
  "Lakehouse Fundamentals", 0,
  "The lakehouse architecture, medallion pattern, and where Delta Lake and Unity Catalog fit.",
  [acad("Lakehouse Fundamentals (free badge)", "https://www.databricks.com/learn/training/lakehouse-fundamentals"),
   docs("Databricks concepts", "getting-started/concepts")],
  [{"q": "Which layer of the medallion architecture holds raw, unprocessed ingested data?",
    "options": ["Bronze", "Silver", "Gold", "Platinum"], "answer": 0,
    "explain": "Bronze is the raw landing layer; Silver is cleaned/conformed; Gold is business-level aggregates."}])

n("notebooks-workspace", "Workspace & Notebooks", "platform", ["foundations"], "foundational",
  "Lakehouse Fundamentals", 0,
  "Navigate the workspace, run notebooks, attach compute, and use magic commands.",
  [docs("Notebooks", "notebooks/")])

# ================================================== PLATFORM & COMPUTE (DE/DA)
n("platform-architecture", "Data Intelligence Platform Architecture", "platform",
  ["de-assoc", "da-assoc"], "associate", "Databricks Intelligence Platform", 6,
  "Core components — control/data plane, Delta Lake, Unity Catalog — and how they connect.",
  [docs("Architecture", "getting-started/overview")],
  [{"q": "In the Databricks architecture, where does customer data primarily reside?",
    "options": ["The control plane managed by Databricks", "The customer's own cloud account (data plane)",
                "On the driver node only", "In the Hive metastore"], "answer": 1,
    "explain": "Compute and data live in the customer's cloud account (data plane); Databricks runs the control plane."}])

n("compute-selection", "Compute Selection & Cost Models", "platform",
  ["de-assoc"], "associate", "Databricks Intelligence Platform", 6,
  "Choose all-purpose, jobs, serverless, or SQL warehouses by workload; understand DBU cost models.",
  [docs("Compute", "compute/")])

# ======================================================= DELTA LAKE (DE/DA) ==
n("delta-tables", "Create & Manage Delta Tables", "delta",
  ["de-assoc", "da-assoc"], "associate", "Data Transformation and Modeling", 22,
  "Create, read, update, and delete Delta tables; understand ACID and the transaction log.",
  [docs("Delta Lake", "delta/"), acad("Data Engineering with Databricks", AC)],
  [{"q": "What guarantees does Delta Lake add on top of Parquet files?",
    "options": ["Only compression", "ACID transactions and schema enforcement",
                "Automatic GPU acceleration", "A proprietary binary format"], "answer": 1,
    "explain": "Delta adds a transaction log giving ACID guarantees, time travel, and schema enforcement over Parquet."}])

n("managed-vs-external", "Managed vs External Tables", "delta",
  ["de-assoc"], "associate", "Governance and Security", 15,
  "Difference between managed and external tables; create, convert, and choose between them.",
  [docs("Managed vs external tables", "tables/managed-vs-external")],
  [{"q": "When you DROP a managed table in Unity Catalog, what happens to the underlying data?",
    "options": ["It is retained in cloud storage", "It is deleted", "It is archived to Bronze", "Nothing—only external tables store data"],
    "answer": 1,
    "explain": "For managed tables Databricks controls the storage lifecycle, so DROP removes the data files. External tables keep their data."}])

n("delta-merge", "MERGE & Upserts", "delta",
  ["de-assoc", "de-pro"], "associate", "Data Transformation and Modeling", 22,
  "Use MERGE INTO for upserts and change application; deduplicate on merge.",
  [docs("MERGE INTO", "delta/merge")])

n("cdf", "Change Data Feed", "delta",
  ["de-pro"], "professional", "Cost & Performance Optimization", 13,
  "Enable and read Change Data Feed (CDF) to propagate row-level changes downstream.",
  [docs("Change Data Feed", "delta/delta-change-data-feed")])

n("liquid-clustering", "Liquid Clustering & Predictive Optimization", "delta",
  ["de-assoc", "de-pro"], "associate", "Troubleshooting, Monitoring, and Optimization", 10,
  "Use Liquid Clustering instead of partitioning/ZORDER; let predictive optimization maintain tables.",
  [docs("Liquid Clustering", "delta/clustering")],
  [{"q": "Liquid Clustering is generally preferred over Hive-style partitioning because it:",
    "options": ["Requires manual OPTIMIZE after every write", "Avoids over/under-partitioning and adapts clustering keys without rewriting layout",
                "Only works on external tables", "Disables data skipping"], "answer": 1,
    "explain": "Liquid Clustering avoids the small-file / skew problems of fixed partitioning and can evolve keys without a full rewrite."}])

n("delta-optimization", "Data Skipping, Deletion Vectors & File Pruning", "delta",
  ["de-pro"], "professional", "Cost & Performance Optimization", 13,
  "Deletion vectors, data skipping statistics, and file pruning to speed large-table queries.",
  [docs("Optimizations", "delta/optimizations/")])

# ============================================= UNITY CATALOG / GOVERNANCE ====
n("uc-fundamentals", "Unity Catalog Fundamentals", "unity-catalog",
  ["de-assoc", "da-assoc", "genai-assoc", "platform-admin"], "associate", "Governance and Security", 15,
  "The catalog > schema > table hierarchy, the three-level namespace, and the metastore.",
  [docs("Unity Catalog", "data-governance/unity-catalog/"), acad("Get Started with Data Governance", AC)],
  [{"q": "What is the correct three-level namespace for a table in Unity Catalog?",
    "options": ["schema.catalog.table", "catalog.schema.table", "metastore.catalog.table", "workspace.schema.table"],
    "answer": 1, "explain": "Unity Catalog uses catalog.schema.table (three-level namespace)."}])

n("uc-access-controls", "Access Controls: GRANT / REVOKE", "unity-catalog",
  ["de-assoc", "da-assoc", "platform-admin"], "associate", "Governance and Security", 15,
  "Apply GRANT, REVOKE, DENY to users, groups, and service principals across the security hierarchy.",
  [docs("Manage privileges", "data-governance/unity-catalog/manage-privileges/")],
  [{"q": "Privileges granted on a catalog in Unity Catalog by default:",
    "options": ["Apply only to that catalog object itself", "Are inherited by schemas and tables within it",
                "Must be re-granted on every table", "Only work for the metastore admin"], "answer": 1,
    "explain": "Unity Catalog uses a hierarchical inheritance model — a grant on a catalog flows down to its schemas and tables."}])

n("uc-rls-masking", "Row-Level Security & Column Masking", "unity-catalog",
  ["de-assoc", "de-pro"], "associate", "Governance and Security", 15,
  "Restrict rows and mask columns with row filters, column masks, and ABAC policies.",
  [docs("Row filters and column masks", "data-governance/unity-catalog/row-and-column-filters")])

n("uc-lineage-discovery", "Metadata, Lineage & Discovery", "unity-catalog",
  ["de-pro", "da-assoc"], "professional", "Data Governance", 7,
  "Add descriptions/tags for discoverability; read column- and table-level lineage.",
  [docs("Data lineage", "data-governance/unity-catalog/data-lineage")])

n("delta-sharing", "Delta Sharing & Lakehouse Federation", "unity-catalog",
  ["de-pro"], "professional", "Data Sharing and Federation", 5,
  "Share live data D2D and D2O with Delta Sharing; query external systems via Lakehouse Federation.",
  [docs("Delta Sharing", "data-sharing/")])

n("data-privacy", "PII Masking, Anonymization & Purging", "unity-catalog",
  ["de-pro"], "professional", "Ensuring Data Security and Compliance", 10,
  "Hashing, tokenization, suppression, generalization; compliant PII pipelines and data purging.",
  [docs("Data privacy", "security/privacy/"), acad("Databricks Data Privacy", AC)])

# =================================================== INGESTION (DE / DA) =====
n("copy-into", "COPY INTO", "ingestion",
  ["de-assoc"], "associate", "Data Ingestion and Loading", 21,
  "Incrementally load files from cloud object storage into Unity Catalog tables idempotently.",
  [docs("COPY INTO", "ingestion/copy-into/")])

n("auto-loader", "Auto Loader & Schema Evolution", "ingestion",
  ["de-assoc", "de-pro"], "associate", "Data Ingestion and Loading", 21,
  "Incremental file ingestion with schema inference, enforcement, and evolution.",
  [docs("Auto Loader", "ingestion/cloud-object-storage/auto-loader/"), acad("Data Ingestion with Lakeflow Connect", AC)],
  [{"q": "Auto Loader is best suited for:",
    "options": ["One-time bulk migration of a fixed file set", "Incrementally and efficiently processing new files as they land in cloud storage",
                "Replacing Unity Catalog", "Interactive dashboard refreshes"], "answer": 1,
    "explain": "Auto Loader (cloudFiles) incrementally ingests newly arriving files with tracked state, schema inference and evolution."}])

n("lakeflow-connect", "Lakeflow Connect Connectors", "ingestion",
  ["de-assoc"], "associate", "Data Ingestion and Loading", 21,
  "Standard and managed connectors to ingest from enterprise sources into UC-governed tables.",
  [docs("Lakeflow Connect", "ingestion/lakeflow-connect/")])

n("ingestion-strategy", "Choosing an Ingestion Method", "ingestion",
  ["de-assoc"], "associate", "Data Ingestion and Loading", 21,
  "Prioritize Auto Loader vs Lakeflow Connect vs partner connectors by volume, frequency, and governance.",
  [docs("Ingestion overview", "ingestion/")])

n("ingest-formats", "Multi-Format & Semi-Structured Ingestion", "ingestion",
  ["de-assoc", "de-pro"], "associate", "Data Ingestion and Loading", 21,
  "Ingest JSON/nested, Parquet, ORC, AVRO, CSV, XML, text and binary from buses and storage.",
  [docs("Read formats", "query/formats/")])

# =============================================== TRANSFORMATION (DE/DA) ======
n("spark-sql-pyspark", "Spark SQL & PySpark Basics", "transform",
  ["de-assoc"], "associate", "Data Transformation and Modeling", 22,
  "Read tables, select/filter, and write with the DataFrame and SQL APIs.",
  [docs("PySpark", "pyspark/")])

n("data-cleaning", "Cleaning & Standardization (Bronze→Silver)", "transform",
  ["de-assoc"], "associate", "Data Transformation and Modeling", 22,
  "Handle nulls, standardize types, deduplicate, and write conformed Silver tables.",
  [docs("Transform data", "transform/")])

n("joins-aggregations", "Joins & Aggregations", "transform",
  ["de-assoc", "de-pro"], "associate", "Data Transformation and Modeling", 22,
  "Inner/left/broadcast/cross joins, unions, and aggregates on large DataFrames.",
  [docs("Joins", "transform/join")])

n("advanced-transforms", "Window Functions & Advanced Transforms", "transform",
  ["de-pro"], "professional", "Data Transformation, Cleansing, and Quality", 10,
  "Window functions and complex joins for large-scale analysis.",
  [docs("Window functions", "sql/language-manual/functions/window")])

n("udfs", "User-Defined Functions (UDFs)", "transform",
  ["de-pro"], "professional", "Developing Code for Data Processing", 22,
  "Author Python/Pandas UDFs and understand their performance trade-offs.",
  [docs("UDFs", "udf/")])

n("gold-objects", "Gold Objects: Views, MVs & Streaming Tables", "transform",
  ["de-assoc"], "associate", "Data Transformation and Modeling", 22,
  "Build views, materialized views, and streaming tables for BI consumers in Unity Catalog.",
  [docs("Materialized views", "sql/user/materialized-views")])

n("data-quality", "Data Quality & Quarantine", "transform",
  ["de-assoc", "de-pro"], "associate", "Data Transformation, Cleansing, and Quality", 10,
  "Apply expectations/validation and quarantine bad records in pipelines.",
  [docs("Pipeline expectations", "dlt/expectations")])

n("data-modeling", "Dimensional & Analytical Data Modeling", "transform",
  ["de-pro", "da-assoc"], "professional", "Data Modeling", 6,
  "Design dimensional models and choose layouts that optimize analytical queries.",
  [docs("Data modeling", "lakehouse/medallion")])

# ================================================ PIPELINES (DE) ============
n("dlt-basics", "Declarative Pipelines (SDP) Basics", "pipelines",
  ["de-assoc"], "associate", "Data Transformation and Modeling", 22,
  "Build batch/streaming pipelines with Lakeflow Spark Declarative Pipelines (SQL/Python).",
  [docs("Declarative Pipelines", "dlt/"), acad("Build Data Pipelines with Lakeflow SDP", AC)])

n("dlt-advanced", "Advanced SDP: AUTO CDC & Streaming Tables", "pipelines",
  ["de-pro"], "professional", "Developing Code for Data Processing", 22,
  "AUTO CDC APIs, streaming tables vs materialized views, production-grade SDP.",
  [docs("AUTO CDC", "dlt/cdc"), acad("Advanced Techniques with SDP", AC)])

n("structured-streaming", "Spark Structured Streaming", "pipelines",
  ["de-pro"], "professional", "Developing Code for Data Processing", 22,
  "Stateful streaming, watermarks, triggers, and when to choose it over SDP.",
  [docs("Structured Streaming", "structured-streaming/")])

# ================================================ JOBS / ORCHESTRATION ======
n("jobs-tasks", "Lakeflow Jobs: Tasks & DAGs", "jobs",
  ["de-assoc"], "associate", "Working with Lakeflow Jobs", 16,
  "Configure notebook/SQL/pipeline tasks and their dependencies in a task graph.",
  [docs("Lakeflow Jobs", "jobs/"), acad("Deploy Workloads with Lakeflow Jobs", AC)],
  [{"q": "In Lakeflow Jobs, how do you make Task B run only after Task A succeeds?",
    "options": ["Schedule them one minute apart", "Set Task A as a dependency (upstream) of Task B",
                "Put both in the same notebook cell", "Use a materialized view"], "answer": 1,
    "explain": "Tasks form a DAG; declaring A upstream of B enforces ordering and passes run state."}])

n("jobs-control-flow", "Control Flow: Retries, Branching, Loops", "jobs",
  ["de-assoc", "de-pro"], "associate", "Working with Lakeflow Jobs", 16,
  "Retries, conditional (if/else) tasks, and for-each loops for robust orchestration.",
  [docs("Control flow", "jobs/control-flow")])

n("jobs-triggers", "Schedules & Triggers", "jobs",
  ["de-assoc"], "associate", "Working with Lakeflow Jobs", 16,
  "Scheduled, file-arrival, and table-update triggers; time-based vs data-driven choices.",
  [docs("Triggers", "jobs/triggers")])

# ================================================ CI/CD & DABs ==============
n("git-folders", "Databricks Git Folders", "cicd",
  ["de-assoc"], "associate", "Implementing CI/CD", 10,
  "Branch, commit, push, and open PRs from the workspace with Git integration.",
  [docs("Git folders", "repos/"), acad("DevOps Essentials for Data Engineering", AC)])

n("dabs", "Declarative Automation Bundles (DABs)", "cicd",
  ["de-assoc", "de-pro", "genai-assoc"], "associate", "Implementing CI/CD", 10,
  "Package and promote jobs, pipelines, and apps across dev/test/prod with bundle variables.",
  [docs("Asset Bundles", "dev-tools/bundles/"), acad("Automated Deployment with DABs", AC)],
  [{"q": "What problem do Declarative Automation Bundles primarily solve?",
    "options": ["Real-time dashboarding", "Packaging and promoting the same code/assets across environments as code",
                "Replacing Unity Catalog grants", "Training ML models"], "answer": 1,
    "explain": "DABs describe jobs/pipelines/apps as code with per-target overrides, enabling promotion across dev/test/prod."}])

n("databricks-cli", "Databricks CLI", "cicd",
  ["de-assoc", "de-pro"], "associate", "Implementing CI/CD", 10,
  "Validate, deploy, and manage bundles and workspace assets in automated CI/CD.",
  [docs("CLI", "dev-tools/cli/")])

n("testing", "Unit & Integration Testing", "cicd",
  ["de-pro"], "professional", "Developing Code for Data Processing", 22,
  "assertDataFrameEqual / assertSchemaEqual, DataFrame.transform, and pipeline tests.",
  [docs("Testing", "notebooks/test-notebooks")])

n("python-project", "Scalable Python Project Structure", "cicd",
  ["de-pro"], "professional", "Developing Code for Data Processing", 22,
  "Modular Python projects optimized for DABs; manage PyPI/wheel/source dependencies.",
  [docs("Python projects", "dev-tools/bundles/python")])

# ============================================ OBSERVABILITY / OPTIMIZE ======
n("job-monitoring", "Monitoring Jobs & Pipelines", "observability",
  ["de-assoc", "de-pro"], "associate", "Troubleshooting, Monitoring, and Optimization", 10,
  "Read run history, DAG status, run times, and failure rates to spot blockers.",
  [docs("Monitor jobs", "jobs/monitor")])

n("spark-ui", "Spark UI & Query Profiler", "observability",
  ["de-assoc", "de-pro"], "associate", "Troubleshooting, Monitoring, and Optimization", 10,
  "Diagnose skew, shuffle, and spill from stage metrics; find bottlenecks in query profiles.",
  [docs("Spark UI", "compute/troubleshooting/debugging-spark-ui")])

n("system-tables", "System Tables for Observability", "observability",
  ["de-pro", "platform-admin"], "professional", "Monitoring and Alerting", 10,
  "Use system tables for cost, utilization, audit, and workload monitoring.",
  [docs("System tables", "admin/system-tables/")])

n("sql-alerts", "SQL Alerts & Notifications", "observability",
  ["de-pro"], "professional", "Monitoring and Alerting", 10,
  "SQL Alerts for data-quality signals and job notifications for status/perf issues.",
  [docs("Alerts", "sql/user/alerts/")])

n("perf-tuning", "Performance Tuning Parameters", "observability",
  ["de-assoc"], "associate", "Data Transformation and Modeling", 22,
  "Tune shuffle partitions, parallelism, memory, and broadcast-join thresholds.",
  [docs("Performance", "optimizations/")])

n("debugging-repair", "Debugging & Job Repair", "observability",
  ["de-pro"], "professional", "Debugging and Deploying", 10,
  "Diagnose failures from logs/system tables and repair runs with parameter overrides.",
  [docs("Repair runs", "jobs/repair-run")])

# ==================================================== DATABRICKS SQL (DA) ===
n("dbsql-warehouses", "SQL Warehouses & Photon", "dbsql",
  ["da-assoc"], "associate", "Executing Queries Using Databricks SQL", 20,
  "Run queries on SQL warehouses; understand Photon and warehouse sizing.",
  [docs("SQL warehouses", "compute/sql-warehouse/"), acad("Data Analysis with Databricks", AC)],
  [{"q": "What is Photon in Databricks SQL?",
    "options": ["A dashboard theme", "A vectorized C++ query engine that accelerates SQL/DataFrame workloads",
                "A Python package", "A governance feature"], "answer": 1,
    "explain": "Photon is a native vectorized engine that speeds up SQL and DataFrame operations on Databricks."}])

n("sql-queries", "SQL Querying: SELECT, JOIN, GROUP BY", "dbsql",
  ["da-assoc"], "associate", "Executing Queries Using Databricks SQL", 20,
  "SELECT/WHERE/GROUP BY, aggregates, joins, and view creation.",
  [docs("SQL reference", "sql/language-manual/")])

n("query-analysis", "Query Performance & Insights", "dbsql",
  ["da-assoc"], "associate", "Analyzing Queries", 15,
  "Optimize queries with Query Insights, history/audit logs, and liquid clustering signals.",
  [docs("Query history", "sql/user/queries/query-history")])

n("da-importing", "Importing Data for Analysis", "ingestion",
  ["da-assoc"], "associate", "Importing Data", 5,
  "UI uploads, S3 ingestion, Delta Sharing, Marketplace, and Auto Loader for analysts.",
  [docs("Add data", "ingestion/add-data/")])

# =================================================== DASHBOARDS & GENIE (DA)
n("aibi-dashboards", "AI/BI Dashboards & Visualizations", "dashboards",
  ["da-assoc"], "associate", "Creating Dashboards and Visualizations", 16,
  "Build datasets, author KPIs/trends/breakdowns, add filters, publish, and schedule refresh.",
  [docs("AI/BI Dashboards", "dashboards/")],
  [{"q": "In an AI/BI dashboard, what does a dataset define?",
    "options": ["The color palette", "The query/logic that supplies data to one or more visualizations",
                "The warehouse size", "User permissions"], "answer": 1,
    "explain": "A dataset is the reusable query that feeds visualizations on the canvas."}])

n("genie-spaces", "AI/BI Genie Spaces", "genie",
  ["da-assoc"], "associate", "Developing AI/BI Genie Spaces", 12,
  "Create/configure Genie spaces, natural-language querying, and governance through Genie.",
  [docs("Genie", "genie/")],
  [{"q": "What is the main purpose of an AI/BI Genie space?",
    "options": ["To train foundation models", "To let business users ask natural-language questions over curated data",
                "To manage cluster policies", "To replace Unity Catalog"], "answer": 1,
    "explain": "Genie provides a governed natural-language interface to a curated set of tables for self-service analytics."}])

# ======================================================= MLFLOW (ML) ========
n("mlflow-tracking", "MLflow Experiment Tracking", "mlflow",
  ["ml-assoc", "ml-pro", "genai-assoc"], "associate", "Databricks Machine Learning", 38,
  "Log params/metrics/artifacts; compare runs; organize experiments.",
  [docs("MLflow tracking", "mlflow/tracking"), acad("Machine Learning Model Development", AC)],
  [{"q": "What does mlflow.log_metric() record?",
    "options": ["A model artifact file", "A scalar value (e.g. accuracy) tied to a run, often over steps",
                "A cluster policy", "A Unity Catalog grant"], "answer": 1,
    "explain": "log_metric records scalar metrics per run (and optionally per step); artifacts use log_artifact/log_model."}])

n("model-registry-uc", "Model Registry in Unity Catalog", "mlflow",
  ["ml-assoc", "ml-pro"], "associate", "Databricks Machine Learning", 38,
  "Register models in UC, manage versions, and use @prod/@challenger aliases and lineage.",
  [docs("Models in UC", "machine-learning/manage-model-lifecycle/")])

n("automl", "AutoML", "ml-dev",
  ["ml-assoc"], "associate", "Databricks Machine Learning", 38,
  "Automated model selection, hyperparameter search, and editable generated notebooks.",
  [docs("AutoML", "machine-learning/automl/")])

n("ml-runtime", "Databricks Runtime for ML", "ml-dev",
  ["ml-assoc"], "associate", "Databricks Machine Learning", 38,
  "Pre-configured ML runtime with common libraries and GPU support.",
  [docs("ML Runtime", "machine-learning/databricks-runtime-ml")])

# =================================================== MODEL DEVELOPMENT (ML) =
n("data-prep-ml", "Data Prep & Exploration for ML", "ml-dev",
  ["ml-assoc"], "associate", "ML Workflows", 19,
  "Profile data, explore distributions, and prepare features for modeling.",
  [acad("Data Preparation with Machine Learning", AC), docs("Prepare data", "machine-learning/")])

n("model-training", "Model Training & Evaluation", "ml-dev",
  ["ml-assoc", "ml-pro"], "associate", "Model Development", 31,
  "Train supervised/unsupervised models, evaluate, and compare candidates.",
  [docs("Train models", "machine-learning/train-model/")],
  [{"q": "For a binary classifier with heavy class imbalance, which metric is most informative?",
    "options": ["Raw accuracy", "Area under the PR curve / F1", "Number of epochs", "Training time"],
    "answer": 1, "explain": "With imbalance, accuracy is misleading; PR-AUC / F1 better reflect minority-class performance."}])

n("hyperparameter-tuning", "Hyperparameter Tuning", "ml-dev",
  ["ml-assoc", "ml-pro"], "associate", "Model Development", 31,
  "Tune with Optuna/Hyperopt; parallelize search and log trials to MLflow.",
  [docs("Hyperparameter tuning", "machine-learning/automl-hyperparam-tuning/")])

n("distributed-ml", "Distributed Training with SparkML", "ml-dev",
  ["ml-pro"], "professional", "Model Development", 44,
  "Scale training with SparkML and distributed patterns; scalable ML pipelines.",
  [docs("Distributed training", "machine-learning/train-model/distributed-training/")])

# =================================================== FEATURE ENGINEERING ====
n("feature-store", "Feature Engineering & Feature Store", "features",
  ["ml-assoc", "ml-pro"], "associate", "ML Workflows", 19,
  "Create UC feature tables, use FeatureLookup and point-in-time joins.",
  [docs("Feature engineering", "machine-learning/feature-store/")])

n("feature-serving", "Online Features & Feature Serving", "features",
  ["ml-pro"], "professional", "Model Development", 44,
  "Serve features online (Lakebase online store) for low-latency inference.",
  [docs("Feature serving", "machine-learning/feature-store/feature-serving")])

# ======================================================= MODEL SERVING ======
n("model-serving-endpoints", "Model Serving Endpoints", "serving",
  ["ml-assoc", "ml-pro", "genai-assoc"], "associate", "Model Deployment", 12,
  "Deploy models behind REST endpoints; understand serverless serving.",
  [docs("Model Serving", "machine-learning/model-serving/"), acad("Machine Learning Model Deployment", AC)])

n("batch-streaming-inference", "Batch & Streaming Inference", "serving",
  ["ml-assoc"], "associate", "Model Deployment", 12,
  "Score with spark_udf / fe.score_batch for batch and streaming inference.",
  [docs("Batch inference", "machine-learning/model-inference/")])

n("serving-scale", "Serving at Scale & Traffic Routing", "serving",
  ["ml-pro"], "professional", "Model Deployment", 12,
  "A/B and canary traffic routing, autoscaling, and zero-downtime version swaps.",
  [docs("Serving config", "machine-learning/model-serving/manage-serving-endpoints")])

# ============================================================ MLOPS =========
n("mlops-cicd", "MLOps & CI/CD", "mlops",
  ["ml-pro"], "professional", "ML Ops", 44,
  "MLOps patterns, CI/CD for models, testing/validation, and reproducible environments.",
  [docs("MLOps", "machine-learning/mlops/"), acad("Machine Learning Operations", AC)],
  [{"q": "In the @prod / @challenger alias pattern, the 'challenger' model is:",
    "options": ["The model currently serving production traffic", "A candidate evaluated against prod before promotion",
                "A deprecated model", "The training dataset"], "answer": 1,
    "explain": "The challenger is a candidate compared to the incumbent @prod model; if it wins, it is promoted."}])

n("model-monitoring", "Model & Data Drift Monitoring", "mlops",
  ["ml-pro"], "professional", "ML Ops", 44,
  "Lakehouse Monitoring for drift detection and performance degradation.",
  [docs("Lakehouse Monitoring", "lakehouse-monitoring/")])

# ============================================================ GEN AI ========
n("genai-design", "Designing LLM Applications", "genai",
  ["genai-assoc"], "associate", "Design Applications", 14,
  "Decompose problems, navigate the LLM landscape, and select models.",
  [acad("Generative AI Engineering with Databricks", AC), docs("Generative AI", "generative-ai/")])

n("chunking-parsing", "Document Parsing & Chunking", "genai",
  ["genai-assoc"], "associate", "Data Preparation", 14,
  "Parse unstructured docs and chunk them for retrieval.",
  [docs("Prepare data for RAG", "generative-ai/tutorials/ai-cookbook/")])

n("vector-search", "Vector Search & AI Search", "genai",
  ["genai-assoc"], "associate", "Data Preparation", 14,
  "Build vector indexes and use semantic similarity search.",
  [docs("Vector Search", "generative-ai/vector-search")],
  [{"q": "A Vector Search index is used to:",
    "options": ["Store relational foreign keys", "Retrieve semantically similar chunks via embedding similarity",
                "Schedule jobs", "Mask PII"], "answer": 1,
    "explain": "Vector Search indexes embeddings so a query can retrieve the most semantically similar chunks for RAG."}])

n("rag-apps", "Building RAG Applications", "genai",
  ["genai-assoc"], "associate", "Application Development", 30,
  "Assemble RAG with Agent Bricks Knowledge Assistants and LLM chains over a knowledge base.",
  [docs("RAG", "generative-ai/tutorials/ai-cookbook/"), acad("Generative AI Engineering", AC)],
  [{"q": "In a RAG pipeline, retrieval happens:",
    "options": ["After the LLM generates its answer", "Before generation, to ground the prompt with relevant context",
                "Only during training", "Never—RAG has no retrieval"], "answer": 1,
    "explain": "RAG retrieves relevant context first and injects it into the prompt so the LLM answers from grounded data."}])

n("agents-deploy", "Agents, MCP & Deployment", "genai",
  ["genai-assoc"], "associate", "Assembling and Deploying Apps", 22,
  "Single/multi-agent systems, tool use via MCP, and deploying agents as Databricks Apps with DABs.",
  [docs("Agent framework", "generative-ai/agent-framework/")])

n("genai-governance", "Governance for AI Applications", "genai",
  ["genai-assoc"], "associate", "Governance", 8,
  "Unity Catalog governance for AI, governed tools, and safety mechanisms.",
  [docs("AI governance", "generative-ai/")])

n("genai-eval", "Evaluation & Monitoring (MLflow)", "genai",
  ["genai-assoc"], "associate", "Evaluation and Monitoring", 12,
  "MLflow tracing, LLM judges (built-in/guideline/custom), offline eval, and production monitoring.",
  [docs("Agent evaluation", "generative-ai/agent-evaluation/"), acad("GenAI App Evaluation and Governance", AC)],
  [{"q": "MLflow tracing for an agent primarily gives you:",
    "options": ["Faster inference", "Step-by-step observability of the agent's execution for debugging and evaluation",
                "Cheaper storage", "Automatic model training"], "answer": 1,
    "explain": "Tracing records each step/tool call in an agent run so you can debug and score its behavior."}])

# ==================================================== ADMINISTRATION ========
n("admin-iam", "Identity & Access Management", "admin",
  ["platform-admin"], "specialty", "Identity and Access Management", None,
  "SCIM provisioning, users/groups, and service principals at workspace and account level.",
  [docs("Manage identities", "admin/users-groups/")])

n("admin-compute-policies", "Compute Policies & Cluster Management", "admin",
  ["platform-admin"], "specialty", "Compute Management", None,
  "Cluster policies, instance pools, and governing compute across workspaces.",
  [docs("Compute policies", "admin/clusters/policies")])

n("admin-account", "Account, Billing & Quotas", "admin",
  ["platform-admin"], "specialty", "Account Management", None,
  "Account console, workspace provisioning, billing, and quota management.",
  [docs("Account admin", "admin/account-settings/")])

n("admin-audit", "Audit Logging & Compliance", "admin",
  ["platform-admin"], "specialty", "Audit & Compliance", None,
  "Configure audit logs, verifiable diagnostics, and compliance controls.",
  [docs("Audit logs", "admin/account-settings/audit-logs")])

n("admin-uc-setup", "Unity Catalog Administration", "admin",
  ["platform-admin"], "specialty", "Governance", None,
  "Set up the metastore, storage credentials, external locations, and catalog governance.",
  [docs("Set up Unity Catalog", "data-governance/unity-catalog/get-started")])

# ----------------------------------------------------------------- EDGES -----
# Foundations underpin every associate entry point.
for t in ["platform-architecture", "uc-fundamentals", "delta-tables", "spark-sql-pyspark",
          "dbsql-warehouses", "mlflow-tracking", "genai-design", "admin-iam"]:
    e("lakehouse-fundamentals", t, "soft")
e("lakehouse-fundamentals", "notebooks-workspace", "hard")

# Platform / Delta
e("platform-architecture", "compute-selection")
e("delta-tables", "managed-vs-external")
e("delta-tables", "delta-merge")
e("delta-merge", "cdf")
e("delta-tables", "liquid-clustering", "soft")
e("liquid-clustering", "delta-optimization")

# Unity Catalog
e("uc-fundamentals", "uc-access-controls")
e("uc-fundamentals", "managed-vs-external")
e("uc-access-controls", "uc-rls-masking")
e("uc-rls-masking", "data-privacy")
e("uc-fundamentals", "uc-lineage-discovery")
e("uc-fundamentals", "delta-sharing", "soft")
e("uc-fundamentals", "admin-uc-setup", "soft")

# Ingestion
e("delta-tables", "copy-into")
e("delta-tables", "auto-loader")
e("copy-into", "ingestion-strategy", "soft")
e("auto-loader", "ingestion-strategy", "soft")
e("lakeflow-connect", "ingestion-strategy", "soft")
e("auto-loader", "ingest-formats", "soft")
e("uc-fundamentals", "lakeflow-connect", "soft")

# Transformation
e("spark-sql-pyspark", "data-cleaning")
e("spark-sql-pyspark", "joins-aggregations")
e("data-cleaning", "data-quality")
e("joins-aggregations", "advanced-transforms")
e("spark-sql-pyspark", "udfs")
e("data-cleaning", "gold-objects")
e("gold-objects", "data-modeling", "soft")

# Pipelines
e("auto-loader", "dlt-basics", "soft")
e("data-cleaning", "dlt-basics")
e("dlt-basics", "dlt-advanced")
e("dlt-basics", "structured-streaming", "soft")
e("delta-merge", "dlt-advanced", "soft")
e("cdf", "dlt-advanced", "soft")

# Jobs
e("notebooks-workspace", "jobs-tasks", "soft")
e("jobs-tasks", "jobs-control-flow")
e("jobs-tasks", "jobs-triggers")
e("dlt-basics", "jobs-tasks", "cooccur")

# CI/CD
e("notebooks-workspace", "git-folders", "soft")
e("git-folders", "dabs")
e("dabs", "databricks-cli")
e("dabs", "python-project")
e("python-project", "testing")
e("jobs-tasks", "dabs", "cooccur")

# Observability
e("jobs-tasks", "job-monitoring")
e("spark-sql-pyspark", "spark-ui", "soft")
e("spark-ui", "perf-tuning")
e("job-monitoring", "system-tables", "soft")
e("job-monitoring", "sql-alerts", "soft")
e("spark-ui", "debugging-repair")
e("liquid-clustering", "perf-tuning", "cooccur")

# DBSQL / DA
e("dbsql-warehouses", "sql-queries")
e("sql-queries", "query-analysis")
e("delta-tables", "da-importing", "soft")
e("sql-queries", "aibi-dashboards")
e("aibi-dashboards", "genie-spaces", "soft")
e("uc-fundamentals", "genie-spaces", "soft")
e("sql-queries", "data-modeling", "soft")

# ML
e("ml-runtime", "automl", "soft")
e("mlflow-tracking", "model-registry-uc")
e("data-prep-ml", "model-training")
e("automl", "model-training", "soft")
e("model-training", "hyperparameter-tuning")
e("mlflow-tracking", "model-training", "soft")
e("data-prep-ml", "feature-store")
e("feature-store", "model-training", "soft")
e("model-training", "distributed-ml")
e("feature-store", "feature-serving")
e("model-registry-uc", "model-serving-endpoints")
e("model-serving-endpoints", "batch-streaming-inference")
e("model-serving-endpoints", "serving-scale")
e("model-registry-uc", "mlops-cicd")
e("mlops-cicd", "model-monitoring")
e("serving-scale", "model-monitoring", "cooccur")
# ML Assoc -> Pro progression (level bridges)
e("model-training", "mlops-cicd", "soft")
e("hyperparameter-tuning", "distributed-ml", "soft")

# GenAI
e("genai-design", "chunking-parsing")
e("chunking-parsing", "vector-search")
e("vector-search", "rag-apps")
e("rag-apps", "agents-deploy")
e("mlflow-tracking", "genai-eval", "soft")
e("dabs", "agents-deploy", "soft")
e("model-serving-endpoints", "agents-deploy", "soft")
e("uc-fundamentals", "genai-governance", "soft")
e("rag-apps", "genai-eval")

# Admin
e("admin-iam", "admin-compute-policies", "soft")
e("admin-iam", "admin-account", "soft")
e("admin-account", "admin-audit", "soft")
e("admin-uc-setup", "admin-audit", "soft")
e("uc-access-controls", "admin-uc-setup", "soft")
e("system-tables", "admin-audit", "cooccur")

# DE Associate -> Professional level bridges
e("auto-loader", "dlt-advanced", "soft")
e("joins-aggregations", "advanced-transforms", "soft")
e("dabs", "testing", "soft")
e("job-monitoring", "debugging-repair", "soft")

# ============================================ ACADEMY ON-DEMAND COURSES ======
# Verified public Databricks Academy / training-catalog course pages (self-paced,
# on-demand). "free" marks courses whose public page states no cost. Each skill node
# links to the on-demand course that teaches it.
CO = "https://www.databricks.com/training/catalog/"
RL = "https://www.databricks.com/resources/learn/training/"
LT = "https://www.databricks.com/learn/training/"
COURSES = {
    "lakehouse-fund":   ("Lakehouse Fundamentals", RL + "lakehouse-fundamentals", True),
    "dbx-fund":         ("Databricks Fundamentals", CO + "databricks-fundamentals-2206", True),
    "de-databricks":    ("Data Engineering with Databricks", CO + "data-engineering-with-databricks-911", False),
    "ingest-connect":   ("Data Ingestion with Lakeflow Connect", CO + "data-ingestion-with-lakeflow-connect-2963", True),
    "deploy-jobs":      ("Deploy Workloads with Lakeflow Jobs", CO + "deploy-workloads-with-lakeflow-jobs-1365", True),
    "devops":           ("DevOps Essentials for Data Engineering", CO + "devops-essentials-for-data-engineering-3605", False),
    "interop-uc":       ("Data Interoperability with Unity Catalog", CO + "data-interoperability-with-unity-catalog-4556", False),
    "build-sdp":        ("Build Data Pipelines with Lakeflow SDP", CO + "build-data-pipelines-with-apache-spark-declarative-pipelines-2971", True),
    "gov-start":        ("Get Started with Data Governance", CO + "get-started-with-data-governance-on-databricks-4677", True),
    "adv-de":           ("Advanced Data Engineering with Databricks", CO + "advanced-data-engineering-with-databricks-971", False),
    "adv-sdp":          ("Advanced Techniques with Spark Declarative Pipelines", CO + "advanced-techniques-with-apache-spark-declarative-pipelines-1810", False),
    "privacy":          ("Databricks Data Privacy", CO + "databricks-data-privacy-3764", False),
    "perf-opt":         ("Databricks Performance Optimization", CO + "databricks-performance-optimization-1809", False),
    "dabs":             ("Automated Deployment with Declarative Automation Bundles", CO + "automated-deployment-with-declarative-automation-bundles-3489", False),
    "sql-bi":           ("Get Started with SQL Analytics and BI", LT + "sql-analytics-bi", True),
    "data-analysis":    ("Data Analysis with Databricks", LT + "data-analysis-with-databricks", False),
    "aibi-analysts":    ("AI/BI for Data Analysts", CO + "aibi-for-data-analysts-3707", True),
    "mgmt-gov-uc":      ("Data Management and Governance with Unity Catalog", CO + "data-management-and-governance-with-unity-catalog-3145", False),
    "ml-prep":          ("Data Preparation for Machine Learning", CO + "data-preparation-for-machine-learning-2343", True),
    "ml-dev":           ("Machine Learning Model Development", CO + "machine-learning-model-development-2390", False),
    "ml-deploy":        ("Machine Learning Model Deployment", CO + "machine-learning-model-deployment-2395", False),
    "ml-ops":           ("Machine Learning Operations", CO + "machine-learning-operations-2400", False),
    "genai-fund":       ("Generative AI Fundamentals", RL + "generative-ai-fundamentals", True),
    "genai-start":      ("Get Started with Gen AI", RL + "get-started-with-generative-ai", True),
    "genai-eng":        ("Generative AI Engineering with Databricks", CO + "generative-ai-engineering-with-databricks-1980", False),
    "genai-eval":       ("Generative AI Application Evaluation and Governance", "https://customer-academy.databricks.com/learn/courses/2717", False),
    "genai-deploy":     ("Generative AI Application Deployment and Monitoring", "https://customer-academy.databricks.com/learn/courses/2713", False),
    "admin-role":       ("Platform Administrator courses (role catalog)", "https://www.databricks.com/training/catalog?roles=platform-administrator", True),
}
NODE_COURSE = {
    "lakehouse-fundamentals":"lakehouse-fund", "notebooks-workspace":"dbx-fund",
    "platform-architecture":"dbx-fund", "compute-selection":"de-databricks",
    "delta-tables":"de-databricks", "managed-vs-external":"interop-uc", "delta-merge":"de-databricks",
    "cdf":"adv-de", "liquid-clustering":"perf-opt", "delta-optimization":"perf-opt",
    "uc-fundamentals":"gov-start", "uc-access-controls":"gov-start", "uc-rls-masking":"privacy",
    "uc-lineage-discovery":"mgmt-gov-uc", "delta-sharing":"interop-uc", "data-privacy":"privacy",
    "copy-into":"ingest-connect", "auto-loader":"ingest-connect", "lakeflow-connect":"ingest-connect",
    "ingestion-strategy":"ingest-connect", "ingest-formats":"ingest-connect",
    "spark-sql-pyspark":"de-databricks", "data-cleaning":"de-databricks", "joins-aggregations":"de-databricks",
    "advanced-transforms":"adv-de", "udfs":"adv-de", "gold-objects":"de-databricks",
    "data-quality":"build-sdp", "data-modeling":"adv-de",
    "dlt-basics":"build-sdp", "dlt-advanced":"adv-sdp", "structured-streaming":"adv-sdp",
    "jobs-tasks":"deploy-jobs", "jobs-control-flow":"deploy-jobs", "jobs-triggers":"deploy-jobs",
    "git-folders":"devops", "dabs":"dabs", "databricks-cli":"devops", "testing":"devops", "python-project":"dabs",
    "job-monitoring":"deploy-jobs", "spark-ui":"perf-opt", "system-tables":"perf-opt",
    "sql-alerts":"deploy-jobs", "perf-tuning":"perf-opt", "debugging-repair":"perf-opt",
    "dbsql-warehouses":"data-analysis", "sql-queries":"data-analysis", "query-analysis":"data-analysis",
    "da-importing":"data-analysis", "aibi-dashboards":"aibi-analysts", "genie-spaces":"aibi-analysts",
    "mlflow-tracking":"ml-dev", "model-registry-uc":"ml-dev", "automl":"ml-dev", "ml-runtime":"ml-prep",
    "data-prep-ml":"ml-prep", "model-training":"ml-dev", "hyperparameter-tuning":"ml-dev",
    "distributed-ml":"ml-dev", "feature-store":"ml-prep", "feature-serving":"ml-deploy",
    "model-serving-endpoints":"ml-deploy", "batch-streaming-inference":"ml-deploy", "serving-scale":"ml-deploy",
    "mlops-cicd":"ml-ops", "model-monitoring":"ml-ops",
    "genai-design":"genai-eng", "chunking-parsing":"genai-eng", "vector-search":"genai-eng",
    "rag-apps":"genai-eng", "agents-deploy":"genai-deploy", "genai-governance":"genai-eval", "genai-eval":"genai-eval",
    "admin-iam":"admin-role", "admin-compute-policies":"admin-role", "admin-account":"admin-role",
    "admin-audit":"admin-role", "admin-uc-setup":"mgmt-gov-uc",
}
# attach the on-demand Academy course to every node (replacing the earlier generic
# catalog placeholder links), keeping docs links.
_missing = [nd["id"] for nd in NODES if nd["id"] not in NODE_COURSE]
assert not _missing, f"nodes without an Academy course mapping: {_missing}"
for nd in NODES:
    nd["links"] = [l for l in nd["links"] if l["url"] != AC]     # drop placeholder academy links
    title, url, free = COURSES[NODE_COURSE[nd["id"]]]
    nd["links"].insert(0, {"type": "academy", "title": title, "url": url, "free": free, "onDemand": True})

# ---------------------------------------------------------------- assemble ---
graph = {
    "meta": {
        "version": "1.0.0",
        "generated": datetime.date.today().isoformat(),
        "disclaimer": (
            "Community/enablement resource, not an official Databricks product. Nodes are "
            "seeded from PUBLISHED certification exam-guide domains, their percentage "
            "weightings, and Academy learning paths. Exam objectives are referenced; no "
            "confidential exam questions are used. Practice questions are original scenarios "
            "for self-placement only. Verify against the current official exam guides."
        ),
        "xpFormula": "xp = max(50, round(weight% * 10)); nodes without published weights default to 100",
    },
    "tracks": TRACKS,
    "areas": AREAS,
    "nodes": NODES,
    "edges": EDGES,
}

# --------------------------------------------------------------- validation --
ids = [n["id"] for n in NODES]
assert len(ids) == len(set(ids)), "duplicate node id"
idset = set(ids)
for ed in EDGES:
    assert ed["from"] in idset, f"edge from unknown node {ed['from']}"
    assert ed["to"] in idset, f"edge to unknown node {ed['to']}"
areaset = {a["id"] for a in AREAS}
trackset = {t["id"] for t in TRACKS}
for nd in NODES:
    assert nd["area"] in areaset, f"{nd['id']} bad area {nd['area']}"
    for tr in nd["tracks"]:
        assert tr in trackset, f"{nd['id']} bad track {tr}"

# cycle check (edges must form a DAG for topo-based unlocking)
from collections import defaultdict
adj = defaultdict(list)
for ed in EDGES:
    adj[ed["from"]].append(ed["to"])
WHITE, GRAY, BLACK = 0, 1, 2
color = {i: WHITE for i in ids}
def visit(u):
    color[u] = GRAY
    for v in adj[u]:
        if color[v] == GRAY:
            raise AssertionError(f"cycle via {u}->{v}")
        if color[v] == WHITE:
            visit(v)
    color[u] = BLACK
for i in ids:
    if color[i] == WHITE:
        visit(i)

here = os.path.dirname(os.path.abspath(__file__))

# 1) raw data export (kept in the repo for reuse / inspection)
out = os.path.join(here, "data", "graph.json")
with open(out, "w") as f:
    json.dump(graph, f, indent=2)

# 2) single self-contained page: inject the graph inline into the template so
#    index.html is fully portable (no data/ dependency, works by double-click).
tpl_path = os.path.join(here, "index.template.html")
with open(tpl_path) as f:
    tpl = f.read()
inline = "<script>window.GRAPH = " + json.dumps(graph) + ";</script>"
MARK = "<!--__GRAPH_DATA__-->"
assert MARK in tpl, f"template missing {MARK} placeholder"
html = tpl.replace(MARK, inline)
with open(os.path.join(here, "index.html"), "w") as f:
    f.write(html)

print(f"OK  {len(NODES)} nodes, {len(EDGES)} edges, {len(TRACKS)} tracks")
print(f"    -> data/graph.json ({os.path.getsize(out)//1024} KB)")
print(f"    -> index.html      ({os.path.getsize(os.path.join(here,'index.html'))//1024} KB, self-contained)")
