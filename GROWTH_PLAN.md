# The 10x Plan: Awesome Entity Extraction

> **Purpose:** turn a useful catalog into the most trusted, practical starting
> point for choosing and evaluating entity-extraction approaches—without
> pretending a star count is a product strategy.
>
> **Current state:** v1 prototype implemented locally. The README selection matrix,
> static chooser, two synthetic task cards, offline fixture validators/scorers,
> and explicit `not_run` report exist. Reader interviews, model/provider execution,
> independent reproduction, and launch/outreach have not been completed.

## 1. The strategic call

### What this repo should become

**The field guide for choosing an entity extractor:** start with the task and
constraints, see a short list of plausible approaches, run one independently,
and inspect what it gets wrong before adopting it.

The repository already has useful breadth: curated catalog sections, ten
standalone examples, an entry-level decision graphic, contribution guidance,
issue forms, and CI for links/list format/example structure. The next leap is
not another taxonomy, 100 more entries, or a web app. It is turning the catalog
into a **decision-and-evidence loop**:

1. **Find:** identify a real task and its constraints.
2. **Choose:** get a transparent shortlist with trade-offs, not an unsupported
   "best model" claim.
3. **Try:** launch an isolated example with clear setup and expected output.
4. **Inspect:** see representative errors, operating requirements, and limits.
5. **Improve:** report a correction, contribute a case, or update a tool entry.

### The missing X

> **A failure-first, constraint-aware Extraction Field Guide, backed by small
> reproducible task cards and a shareable comparison report.**

The reader-facing promise: **"Tell us what you're extracting and what you can't
compromise on. We'll show you where to start—and what can go wrong."**

The distinct shareable unit is a **task card**: one extraction job; its
constraints; candidate approaches; a tiny, versioned example; expected output;
observed failure cases; exact model/tool/runtime metadata; and a reproducible
command. Task cards can be linked, cited, corrected, and added by contributors.
The first report should be static and small. No accounts, hosted inference,
private-text upload, or backend in v1.

This is the highest-potential bet, **not a proven explanation of the current
star count**. A good field guide could generate repeat use, citations, corrections,
and organic shares. It could also fail to attract users. The plan below sets
explicit tests and kill/pivot gates so we learn before building a benchmark
monument to nobody's problem.

## 2. Current evidence and what it does not say

Snapshot read from GitHub during plan revision (2026-10-12 UTC):

- Repository: `shivamnegi92/awesome-entity-extraction`
- Created: 2026-06-25; default branch `main`
- Stars: **1**; forks: **0**
- Topics already include `awesome`, `entity-extraction`, `information-extraction`,
  `knowledge-graph`, `llm`, `named-entity-recognition`, `ner`, `nlp`, and
  `relation-extraction`.
- Current strong surfaces: README/catalog, animated decision/task graphics,
  ten example folders, contribution guide, issue templates, PR template, link
  check, awesome-lint, and example structure/syntax workflow.

This is a single snapshot, not a trend or diagnosis. One star and zero forks
cannot tell us if the blocker is search discovery, the README pitch, stale
content, a weak use case, conversion, timing, or just too little exposure. Do
not interpret them as proof that the repository is bad—or that outreach alone
will fix it. Capture comparable observations over time before claiming success.

## 3. Strategy: start narrow; earn the right to expand

### Target reader, initially

Primary: a developer or technical lead implementing extraction from text or
documents who is deciding between a local model, an LLM/API, a rules-based tool,
or a domain/document-specific pipeline.

Secondary audiences (serve after the first wedge works):

- NLP researchers/practitioners comparing task fit and error behavior.
- Data/document automation engineers choosing PDF/OCR extraction paths.
- Privacy-sensitive teams needing local processing or PII controls.
- Library/model maintainers wanting an accurate, fair reference/example.

Don't write for "everyone interested in AI." Name a concrete job, a concrete
choice, and the evidence the project supplies.

### User jobs to be validated

1. "I need to extract **X** from **this kind of input**. What should I try
   first?"
2. "I cannot send text to a hosted service / I have no GPU / I need another
   language. Which options remain?"
3. "Will this work with abbreviations, Unicode, negation, OCR noise, overlapping
   mentions, missing fields, or ambiguous names?"
4. "Can I run a minimal example and understand the output without installing a
   kitchen-sink environment?"
5. "What evidence supports this recommendation, and what has not been tested?"

### Falsifiable product hypothesis

**H1:** Compared with the current catalog alone, a task card with constraints,
copyable run path, and visible failure cases helps a target reader make a
shortlist faster and gives them a useful next action.

**Disconfirm H1 if:** target users cannot name the decision it improves; users
prefer a plain curated list; they do not use the task card/example; or the
maintenance burden exceeds the value. In that case, improve curation, examples,
and discovery rather than continuing to build the field guide.

## 4. First validate, then build

### Discovery sprint (5 working days; timebox it)

**Do:**

- Talk to 6–8 people who have recently implemented or evaluated entity
  extraction. Include at least two people outside the author's immediate team
  or close network, and represent more than one task family.
- Ask for a recent real decision, not "would you use this?": input type, schema,
  language, privacy/network constraint, hardware, budget, options tried, where
  they got stuck, and what evidence would have changed their choice.
- Give them the current README and one relevant example. Observe where they
  hesitate, what they click, and whether they can run it. Do not pitch the new
  idea until they have described their workflow.
- Capture notes without names, private source text, or sensitive organization
  details. Ask before quoting anyone publicly.
- Record a baseline snapshot: stars/forks, repo views/clones if GitHub exposes
  them, referrers if available, issue/PR activity, and last-30-day commits. Save
  timestamp and source; don't add invasive tracking just to get a dashboard.

**Decision gate:** proceed with a field-guide prototype only if at least 4 of 6
interviewees describe a materially similar selection/evaluation problem, and at
least 3 say they would use a concrete task card or comparison artifact. These
are directional gates for a small qualitative sample, not statistical proof.
If the sample says otherwise, record what was learned and revise the wedge.

## 5. Product definition: task cards, not a universal leaderboard

### A task card includes

- **Task:** one clearly named job (e.g. business NER, support-email PII
  redaction, invoice fields, relation triples).
- **Constraints:** input kind, language, schema flexibility, local/hosted, network,
  credentials/cost, and compute assumptions.
- **Candidate approaches:** a short rationale and explicit exclusions/unknowns.
- **Fixture:** a small, versioned synthetic/public-domain-safe input set with
  expected output annotations and annotation policy.
- **Run path:** command, dependencies, required model/API, expected output, and
  tested environment; one approach per isolated environment.
- **Results:** task-appropriate metric, sample count, exact tool/model versions,
  date, hardware, and run status.
- **Failure gallery:** at least one miss, false positive, ambiguity, invalid
  structured value, or other representative edge case. Explain why it matters.
- **Limitations and sources:** licenses, coverage limits, known caveats, and
  canonical project/model references.
- **Contribution route:** how a reader can propose another case, correction, or
  supported approach without submitting sensitive input.

### Comparison rules (non-negotiable)

- Compare systems only on the **same task, fixture version, and documented
  conditions**. Keep tasks separate; no single blended "accuracy" rank.
- Separate local models, hosted APIs, commercial products, and deterministic
  rules. Identify paid/network requirements before asking users to run them.
- Report hardware, model size/precision, runtime, and batching with performance.
  Do not compare latency measured on different setups as if directly equivalent.
- For hosted systems, report provider/model, API date/configuration, request
  count, and measured cost if available. If cost isn't measured, say so.
- Publish raw machine-readable outputs plus the human-readable summary. Preserve
  failed runs and exclusions; don't quietly discard inconvenient results.
- Freeze test cases before scoring candidates. New cases get a version bump and
  their own changelog entry; no post-hoc cherry-picking.
- Define each metric next to the result. Exact/overlap span F1 is not a general
  structured-extraction score; valid JSON is not factual correctness.
- Use only synthetic or permissively redistributable inputs. Never solicit
  uploads of private/customer/health data. Review model/data license terms before
  redistribution or publication.
- Scores inform a decision; they are not proof of universal quality, safety, or
  regulatory suitability.

### V1 scope (deliberately small)

**Implemented locally:** a six-row editorial selection matrix plus two versioned
synthetic task cards (custom NER and PII redaction), with standard-library fixture
validation/scoring and a static report scaffold. The generated chooser and report
show both card statuses as `not_run`; actual extractor runs and independent review
are still required before making performance claims.

Start with **two task cards**, not all ten examples and every catalog entry:

1. **Custom NER on short text** — tests span/type/offset behavior and label
   flexibility. Candidate set: one classic pretrained NER baseline and one
   zero-shot custom NER option, subject to verified package/model availability.
2. **PII redaction on synthetic contact text** — tests detected types and whether
   known synthetic values remain after redaction. Clearly distinguish residual
   string checks from a privacy guarantee.

These are candidate starting points, not fixed decisions. User discovery,
license review, reproducibility, and environment size can change the first two
tasks. Add structured extraction or invoice fields only after v1 works and there
is user demand.

## 6. Prioritized roadmap and gates

### Phase A — Baseline and reader test (week 1)

**Deliverables**

- Dated repository/discovery snapshot and a one-page interview synthesis.
- Ranked user jobs with evidence and counter-evidence.
- Five short first-time-reader observations: can they state what this is, pick
  the relevant section, run one low-friction example, and find contribution
  instructions?
- Decision at the discovery gate: build task cards, change the wedge, or stop.

**Done when** the evidence and decision are recorded in-repo (a short dated
research note is enough), including what the team decided *not* to build.

### Phase B — Make selection useful (week 2)

**Status: prototype implemented.** `field_guide/decision_matrix.json` is the
machine-readable shortlist; `field_guide/site/index.html` is generated as a
static chooser. Recommendations are editorial, not measured rankings.

**Deliverable:** a concise `Choosing an approach` matrix in the README or a
linked page. Rows should be **reader constraints/use cases**, columns should
recommend starting options and point to local examples and canonical sources.

Initial rows to validate:

- Common English NER; caller-defined labels; low-latency CPU/local inference.
- PII detection/redaction; strict data locality; no hosted API.
- Fixed schema from short messy text; API-key/paid-service acceptable.
- Text PDF versus scanned/layout-heavy document.
- Multilingual text; relations/triples; dates and quantities.

For each row: say why to start there, what to try next, what disqualifies it,
and what is unknown. Include no unsupported winner badges, performance claims,
or inferred licenses. Link to an example where one exists; explicitly mark gaps.

**Done when** 5 readers can use the matrix to select a candidate for 3 common
scenarios without needing the maintainer to explain it live. Keep it as a
maintained reference, not an interactive app yet.

### Phase C — Ship two trustworthy task cards (weeks 3–5)

**Status: fixtures, policies, schemas, validators, metrics, and report-generation
scaffold implemented.** Model/provider runs and independent review are outstanding;
no scores have been published.

**Deliverables**

- A versioned, small fixture and gold annotations for each selected task.
- A short schema/annotation guide with inclusion/exclusion rules and edge cases.
- Two or three adapters maximum, chosen for viable dependencies, licensing,
  and comparable task support.
- A standard run manifest (commit, fixture version, command, package/model/API,
  date, OS/runtime, hardware, network/credentials, success/failure).
- Task-specific evaluator and tests for offsets/normalization/metric behavior.
- Human-readable failure gallery and raw JSON/CSV results generated from runs.
- Clean-environment reproducibility instructions and a small reviewer checklist.

**Done when** an independent reviewer can reproduce one card; raw outputs map to
summary numbers; exact versions and hardware are visible; failure examples are
included; no PII/private or restricted data is used; and a second reviewer
agrees the comparison language is fair or the disagreements are disclosed.

### Phase D — Contribution flywheel (weeks 4–6; overlaps only after format is stable)

**Status: existing contribution docs/forms are in place; Field Guide-specific
contribution and external first-issue work remains.**

**Deliverables**

- A concise contribution contract for proposing a tool, task card, test case,
  correction, or example.
- Three real, scoped first issues based on actual gaps, each with context,
  acceptance criteria, and a way to test it.
- A release note that credits contributors and explains meaningful changes.
- A monthly/quarterly review habit for stale links/claims; don't add metadata that
  no one will maintain.

**Done when** a new contributor can choose one real issue, understand scope,
submit a PR, and see a clear pass/fail path in CI. Treat respectful rejection or
re-scope as part of healthy review, not contributor failure.

### Phase E — Distribution experiment (weeks 6–8, after useful artifact exists)

**Status: not started.** Do not announce model scores until runs are reproduced
and independently reviewed.

**One launch, multiple tailored messages:**

1. Publish a short article: "How to choose an entity extractor under real
   constraints" with a concrete task card and reproducible method.
2. Ask selected library/model maintainers to correct their own entry/card; make
   no endorsement claim and do not mass-tag people.
3. Share in 2–3 relevant practitioner communities, following their norms. Offer
   a useful result (failure examples / decision matrix), not a generic request for
   stars.
4. Give maintainers/contributors a copyable permalink and citation/version.
5. Track only available, privacy-respecting referral/engagement indicators.

**Done when** each source has a dated outreach record, traffic/referrer or
qualitative feedback is captured where available, and the next change follows
observed response—not a predetermined "viral" goal.

## 7. Explicit kill, pivot, and expand criteria

### Kill or pivot the benchmark/field-guide bet if

- Interviews do not reveal a repeated decision problem.
- The shortlisting matrix is useful but comparisons are not—ship the matrix and
  invest in accurate curation/examples instead.
- Fairly comparable test conditions cannot be maintained for a task.
- Licensing, cost, model availability, or compute make reproduction inaccessible
  to the target reader.
- The fixture fails to capture errors users consider consequential.
- There is no independent reproduction after two deliberate recruitment rounds;
  ask why before adding more scope.

### Expand only if

- Readers use/share/cite task cards for real decisions, not just compliment the
  idea.
- At least one independent reproduction/correction improves confidence.
- New tasks are requested by more than one user or contributor, or expose a
  genuine blind spot in the first two cards.
- Maintenance time and CI/repro burden remain bounded and documented.

## 8. Quality and trust system

### What stays always-on in CI

- `awesome-lint` for the main list.
- Link check with clear network-dependent status and sensible failure reporting.
- Offline example structure/syntax checks.
- Fixture/schema validity, evaluator unit tests, deterministic metric fixtures,
  and report-generation consistency once task cards exist.
- Secret/fixture-size checks if implemented with low false positives and clear
  ownership; never add noisy security theater.

### What is scheduled or manual

- Large model downloads and model inference: scheduled/manual only for a tiny,
  stable, free subset. Pin artifacts and cache responsibly.
- Paid API examples: no pull-request secrets; run manually with approved
  credentials and publish spend/configuration. Never block community PRs on paid
  vendor availability.
- Live web/API linking: scheduled/manual, explicit timeout/retry, respect provider
  terms. Failure due to external outage must not masquerade as a code regression.

Every status should distinguish **passed**, **failed**, **skipped**, and
**not run**. A syntax/structure check is not a model-quality test.

### Curation freshness policy

- Keep the compact factual one-line list format unless contributors show why
  per-entry metadata is worth maintaining.
- Use a dated review note for fast-changing or high-impact entries (APIs, model
  access, licenses, renamed projects); do not make every entry carry a stale
  "last checked" timestamp that becomes noise.
- When a link checker fails, distinguish dead URL from host bot-block, TLS/DNS
  outage, or transient timeout before deleting an entry.
- Review claims and links during a quarterly batch or when a contributor flags
  them; remove/replace only with evidence.

## 9. Measurement: learn whether value and discovery improve

### Baseline and cadence

Save one dated snapshot now, then repeat monthly for at least three months using
the same source and definitions. Track:

- GitHub stars/forks (lagging social proof; not the north star).
- Views/clones/referrers if GitHub makes them available to maintainers.
- External unique contributors; useful issues/PRs; accepted corrections; return
  contributors.
- Example-index clicks or feedback if measurable without new intrusive
  telemetry; otherwise use interviews/issues as qualitative evidence.
- Time to first useful action in five-reader tests (scenario selected, example
  attempted, or meaningful correction submitted).
- Reproduction count for task cards, including failures and corrections.

### North-star signal

**Verified reader actions per month:** a reader runs an example, reproduces a
task card, or contributes a substantive correction/issue. GitHub may not expose
all actions; report only observable evidence and identify the source. Do not
claim this as a complete user count.

### Guardrails

- Never make stars a target that encourages exchanges, spam, or quality dilution.
- Avoid trackers/cookies and do not collect submitted user text.
- Do not compare raw views from different time windows or channels without
  labeling dates, source, and methodology.
- Set numeric targets only after baseline and feedback. Report actuals honestly,
  including flat or negative results.

## 10. Failure modes to prevent

- **Building too much before validation:** cap v1 at two task cards, few adapters,
  static output; require a decision gate before expanding.
- **Leaderboard bias:** no global rank, no selective test cases, no hidden
  provider/model updates, no score without fixture/version/context.
- **Maintenance collapse:** avoid broad dependency matrices and daily link churn;
  automate only stable checks with a maintainer to own failures.
- **Contributor overload:** real good-first issues only; clarify accepted scope;
  don't promise response SLAs without capacity.
- **Promotion without value:** each announcement should answer a specific reader
  question and link to a usable task card/example.
- **Scope confusion:** this is a curated list plus reference artifacts, not a
  product/framework or a certification of listed tools.
- **False confidence:** scores/JSON validity are not evidence of factuality,
  privacy compliance, security, or fitness for production.

## 11. Immediate next 10 actions

1. Freeze and record the current GitHub metric snapshot with retrieval time/source.
2. Recruit six practitioners for short interviews; use a consistent question
   guide, but do not collect sensitive work text.
3. Run five first-time-reader tests of the existing README/example funnel.
4. Write the interview synthesis, including evidence against the field-guide idea.
5. Decide whether the wedge is task selection, fair comparison, or hands-on
   reproduction; do not assume all three are equally urgent.
6. Draft the constraint-based selection matrix from current catalog entries.
7. Show the matrix to five readers; observe selections and confusion.
8. Select two task cards only after users and licensing/feasibility review agree.
9. Publish fixture schemas and annotation policy before running candidate models.
10. Build a tiny evaluator/report, obtain independent reproduction, then launch
    a targeted article/community sharing experiment.

## 12. Definition of success

The plan is working if the repository becomes measurably more useful to real
practitioners: they find a starting approach faster, can reproduce the evidence,
notice and correct meaningful failures, and contribute improvements. Stars,
links, and mentions can support that story but cannot substitute for it.

The principle to keep: **be the honest guide that helps people choose and see
trade-offs—not the loudest list, the biggest benchmark, or the boldest claim.**
