# Repo Context & Conventions

This is a Russian-language, from-zero-to-middle AI/LLM engineering **course**,
not a reference manual — the critical distinction from the sibling
`5_devops_sre_knowledgebase` repo in this series. Lessons build on each other
sequentially (each assumes only what earlier lessons taught); a reader is
meant to go through them in order, not jump in at an arbitrary topic.

The authoritative recipe for how to WRITE a lesson is `.agents/PROJECT_TASK.md`
(section "Как писать теорию"; moved out of the repo root on 2026-10-13 so the
root holds only what a learner needs) — read it before authoring any
new lesson. This file (`AGENTS.md`) captures structural/maintenance
conventions and lessons learned from auditing the repo; it does not replace
`PROJECT_TASK.md`'s content rules, it enforces them.

All new content — lesson prose, code comments in examples, exercise text —
is written in Russian, matching the rest of the repo.

## Universal Line Length Rule (70–80 characters, `.md` AND code)

Same rule as the sibling devops repo: hard-wrap prose at ~70-80 characters
(max 80) with explicit line breaks, not reliance on a renderer's soft-wrap —
applies to lesson `.md` files same as any other text in the repo. Files
touched during the 2026-10-13 restructure are compliant: any line over 80
chars in them is only an allowed exception (a markdown link that can't be
broken mid-URL, or a formula), never unwrapped prose. Untouched pre-existing
files are the real Phase 2 debt and run wider — up to 105 chars seen in
sampled files — treat that as a known gap, not a precedent (as of
2026-10-14 most lesson files are compliant; remaining debt is mainly in
section READMEs, `data/README.md`, `0_lab_setup/` reference pages and dense
example `.py` files).
Allowed exceptions: unbreakable URLs/links, code blocks where wrapping
breaks syntax, tables.

**Phased fix (explicit user decision, recorded here):**
- **Phase 1 (now, ongoing):** every file newly written, or edited for any
  other reason (including a rename/split done for a different purpose, like
  extracting lesson content out of a README.md), must be wrapped at 70-80
  chars as part of that same edit.
- **Phase 2 — done 2026-11-04** at the owner's request: every `.md` was
  reflowed paragraph-by-paragraph (whole paragraph re-wrapped, never a
  single long line cut in two — that leaves orphan words). Remaining lines
  over 80 are only unbreakable links, tables and code. Keep it that way.

## Directory & Structural Conventions

- Top-level sections: `<N>_<name>/` with a sequential integer prefix
  (`0_lab_setup`, `1_math_and_data`, ... `12_capstones`), matching the
  numbering in `.agents/PROJECT_TASK.md`'s "Программа" table and the root
  `README.md`'s "Разделы" list. Keep both in sync with what's on disk.
- Standard leaf template per section: `README.md`, `01_theory/`,
  `02_examples/`, `03_exercises/`, `04_exercises_answers/` — see
  `PROJECT_TASK.md` → "Структура репозитория".
- `README.md` at the section's own root (`N_section/README.md`) is pure
  navigation: intro, reading order of that section's lessons, link to
  labs/exercises, "when to move on" criterion. Do not put lesson content
  there — this file must stay scannable as a table of contents.
- **Lesson files inside `01_theory/` get a numeric reading-order prefix**
  (`01_`, `02_`, ...) matching the section's own README "Порядок чтения" list
  — e.g. `1_math_and_data/01_theory/01_vectors_and_linear_model.md`, `02_
  gradients.md`, `03_probability_and_data.md`. Real bug found and fixed
  2026-10-13: every section had 2+ lesson files sitting unprefixed, so their
  alphabetical order on disk (what GitHub/a file browser shows with no
  README open) did NOT match actual reading order — a reader browsing the
  raw directory had zero signal which file to open first. The one exception:
  `12_capstones/01_theory/review_questions.md` stays unprefixed and un-
  numbered on purpose — it is explicitly NOT part of the sequential lesson
  order (see "Consolidated Review Block" below). When adding a new lesson to
  an existing section, insert it at the right position and renumber
  everything after it (both the files and the README's list) rather than
  appending out of order at the end.
  Exception (2026-11-04): `1_math_and_data/01_theory/00_why_math.md` is an
  orientation lesson placed before `01_` without renumbering; sections 5,
  6, 7, 9, 10 got new lessons appended at the end (see below).

## README.md Is Navigation-Only, Never Lesson Content

Superseded decision, corrected after checking the sibling devops repo in detail:
`README.md` **never** holds lesson content anywhere in this repo, matching the
devops repo exactly (there, `README.md` only exists at a section's own root and
inside `03_exercises/`, never inside `01_theory/`). Every section used to have
its first lesson living in `01_theory/README.md` — this was fixed: that content
was extracted into a properly named file sitting alongside the section's other
lessons (`0_lab_setup` → `01_theory/01_rules_and_learning.md`, `1_math_and_data`
→ `01_theory/01_vectors_and_linear_model.md`, `2_classical_ml` →
`01_theory/01_classification_basics.md`, `3_neural_networks` →
`01_theory/01_neurons_and_backprop.md`, `4_nlp_and_transformers` →
`01_theory/02_attention.md`, `5_llm_applications` →
`01_theory/01_structured_output.md`, `6_retrieval_and_rag` →
`01_theory/01_rag_basics.md`, `7_evaluation_and_safety` →
`01_theory/01_free_text_evaluation.md`, `8_fine_tuning` →
`01_theory/01_sft_basics.md`, `9_agents_and_tools` →
`01_theory/01_tool_calling.md`, `10_serving_and_operations` →
`01_theory/01_serving_basics.md`, `11_multimodal_and_cv` →
`01_theory/01_convolutions_basics.md`, `12_capstones` →
`01_theory/01_project_workflow.md`), and `01_theory/README.md` was deleted in
every section — there is no index file at that level, same as devops. When
adding a new lesson: it always gets its own descriptively-named file in
`01_theory/`, including the first lesson of a section — never put lesson content
in a file named `README.md`, at any depth.

## Granularity Principle — One Lesson, One Concept-Cluster

`PROJECT_TASK.md` already states this explicitly ("Не пытайся вместить
несколько сложных тем в одну краткую заметку") — this section exists because
an audit found it wasn't being followed uniformly. `PROJECT_TASK.md`'s own
"Программа" table lists, per section, the distinct concepts that section must
cover (comma-separated). Rule of thumb: if that list has more than ~3-4
genuinely distinct concepts for one section, split them across multiple
lesson files instead of one dense file — each split-out lesson still follows
the full 8-step structure (problem → prior-lesson link → explanation →
worked-by-hand example → formula/code → typical mistake → self-check
questions → next step) on its OWN concept-cluster, not a compressed version
of all of them. A single ~100-120 line file trying to cover 6-9 concepts at
once is the failure mode to avoid — it under-serves every concept crammed
into it and structurally can't fit a worked-by-hand example for each one.

## Self-Check Questions — Scale the Block to the Lesson's Density

Every lesson ends with self-check question(s) in collapsible form:

```markdown
<details>
<summary>Разбор</summary>

Развёрнутый разбор ответа объясняющим текстом...

</details>
```

**This is a different genre from the devops repo's "Interview Q&A" section**
(bold question + italic `*Ответ:*`, ~10 exam-style questions) — do not import
that format here. This repo's questions are self-check prompts for a learner
mid-lesson, phrased to invite the reader to answer in their own words before
revealing the breakdown (see root README "Как читать материал").

That said: **one question per lesson is a floor, not a fixed count.** Scale
the number of `<details>` blocks to how many genuinely distinct ideas the
lesson introduces — a short, single-concept lesson can have one question; a
lesson covering several ideas (even after applying the Granularity Principle
above) should end with a real block of 2-5 self-check questions, each
targeting a different idea from that lesson, not one question covering
everything at once. Place them together under one `## Проверить понимание...`
heading (matching the existing heading style), not scattered through the body.

## Cross-Reference & Validation Discipline

Sections and lessons link to each other and to labs via relative Markdown links
(`[text](../other_section/README.md)`, `[next lesson](01_tokenization.md)`).
After any structural change (new/renamed/moved lesson, split file, section
reorg), re-verify repo-wide, not just the touched files:

1. **Relative links resolve** — glob `*.md` (excluding `.venv`/`__pycache__`),
   regex `\]\(([^)]+)\)`, skip `http(s)://`/`mailto:`, resolve each with
   `os.path.normpath(os.path.join(dirname, link))`, assert `os.path.exists`.
   Links into sibling repos are NOT relative: use canonical GitHub URLs,
   same as the sibling repos (decided 2026-11-04):
   `https://github.com/krasnosvar/<repo>/tree/main/<dir>/` for directories,
   `.../blob/main/<file>` for files. Relative `../4_python_...` links break
   on GitHub because each repo is published separately. Verify the target
   still exists in the local sibling checkout (strip the URL prefix and
   check the path under `../<repo>/`); numbering drifts there
   independently of this repo.
2. **Fence balance** — `grep -c '^```'` even in every touched `.md`.
3. **`<details>`/`<summary>`/`</details>` balance** — counts of all three
   match in every touched lesson file.
4. **No trailing whitespace / stray mixed-script glyphs** — same checks as
   the sibling devops repo: `grep -rnE ' +$'`,
   `grep -nP '[\x{4e00}-\x{9fff}]'`.
5. **Self-reporting hygiene** — the root `README.md` intro states exact
   counts (lessons, examples, exercises, questions). If a structural change
   alters any of these counts (splitting a lesson, adding a self-check
   question block, adding a new review section), update it in the SAME
   change. A stale "78 вопросов" claim after splitting two answers (real
   case, 2026-10-13) is worse than no claim — only assert numbers you can
   back up, and keep calculation vs measurement, syntax-check vs executed
   experiment distinct.

## No Cheat-Sheets (decided 2026-11-04)

Do NOT create `CHEATSHEET.md` cheat-sheets (per section or anywhere else)
in this repo; the earlier per-section cheat-sheets were removed at the
owner's request. Reference material stays in the lessons themselves and in
`other/glossary.md` (the single "term → home lesson" table).

## No Checker/CI/Test Harness — Repo Root Matches the Sibling Repos

On 2026-10-13, at the user's request ("удали чекер и остальное — как в
других репах"), the repo-level tooling was removed: `scripts/check.py`,
`tests/`, `.github/` CI, `Makefile`, `labs.json`, `VALIDATION.md`, and the
shared `coursekit.py` module. Reason: a learner opening the repo root saw a
pile of files with no idea what they were for, and the sibling repos keep
only `README.md`, `.gitignore`, `.agents/`, `other/` at the root. What was
learner-facing was moved, not deleted:
- `scripts/doctor.py` → `0_lab_setup/02_examples/01_doctor.py`;
- `models.json` (pinned model SHAs) → `data/models.json`;
- `PROJECT_TASK.md` → `.agents/PROJECT_TASK.md`;
- `coursekit.py` (paths to `data/` and the model) → inlined into each of the
  10 examples that used it (a `ROOT`, `data()`, `require_model()` block), so
  every example is self-contained and no longer hacks `sys.path`.
Kept at the root on purpose: `pyproject.toml`, `uv.lock`, `.python-version`
(every `uv run` command in the course depends on them), `data/`, `artifacts/`
(local-only, gitignored: model weights and the learner's results).

Consequences for maintenance: do NOT re-add a checker, CI, tests or a
validation report without being asked. Verification is done at edit time by
hand — run the examples you touched (`uv run python <path>`), run
`03_exercises/check.py` (fails with `NotImplementedError`) and
`03_exercises/check.py --answers` (passes) in each touched section, smoke-test
`12_capstones/02_examples/01_ticket_service.py` with curl (health, classify,
404) if you touch it, and run the link/fence/details checks above. The
per-section `03_exercises/check.py` files are the exercises' own self-check,
not repo tooling — they stay. The `02_examples/`, `03_exercises/` and
`04_exercises_answers/` READMEs stay too: they carry content (run commands +
experiments to try; the exercise statement itself; the solution walkthrough),
unlike the removed `01_theory/README.md` index files.

## Lessons From the Sibling Python Repo's Full Audit (2026-10-13)

A repo-wide beginner-clarity audit of `4_python_my_knowledgebase` found
problems that structural checks (links, numbering, fences) never catch.
They apply here just as much — this repo is a from-zero course too:

- **Every section README answers "зачем"** — what concrete problem the
  section solves and what the reader can do afterwards, not only a reading
  list. A README that is just a topic list made readers ask "why does this
  section exist at all" about a section with perfectly good content.
- **Each prerequisite concept has exactly one home lesson.** If a concept
  (a math notion, a Python construct, an ML term) is used across many
  lessons, find the one lesson that teaches it from zero; every other lesson
  gives a one-line gloss + link there. In the Python repo exceptions,
  `import`, type hints, classes, HTTP and basic SQL were used everywhere but
  taught nowhere — check this repo for the same class of gap (e.g. NumPy
  basics, Python features used in examples, probability terms, tensors).
- **Reordering can move the bug instead of fixing it.** Moving a lesson
  earlier to satisfy one dependency made it use terms that were now defined
  only *after* it. After any reorder, re-audit the lesson that moved earlier.
- **Audit full files, not the first file per section.** A first pass that
  spot-checked one file per section missed an ordering bug that a full read
  found immediately. Parallel read-only forks, one per group of sections,
  each reading every lesson in full, worked well.
- **Run code blocks you add or change — reading is not verification.** Real
  bugs found only by running: a missing import, a framework parameter read
  from the wrong place, an example that didn't demonstrate what the prose
  claimed (a coverage example — fixed and verified with the real tool).
- **Links into sibling repos must not be the only explanation of a
  prerequisite.** A reader may not have that repo; two such pointers in the
  Python repo were dead ends. Explain inline (even briefly) and treat the
  sibling link as "подробнее".
- **Mixed Latin+Cyrillic words** are a recurring artifact ("коммit",
  "formы", "corutina", "momент"). Scan in addition to the CJK scan:
  `grep -rnoP '\b\w*(?:[а-яё][a-z]|[a-z][а-яё])\w*\b' --include='*.md'
  --include='*.py' .` — review hits by hand (escapes like `\nчисло` inside a
  string are legit).
  The only expected hits are the examples in this paragraph itself.
- Internals that only a curious reader needs go into a `<details>` block
  labelled "Для любопытных" so the main path stays readable.

## What the 2026-10-14 Full Audit Fixed Here (homes to link, not re-explain)

A full read of every lesson + running every script found the same gap class
as in the Python repo: concepts used everywhere, taught nowhere. Each now has
one home — later lessons give a one-line gloss and link there:
- minimal Python (functions, collections, `zip`/`enumerate`, `lambda`,
  `raise`/`try`, `class`/`self`, `with open`, `import`) →
  `0_lab_setup/python_minimum.md` (reference page, not a numbered lesson;
  the entry diagnostic now also checks exceptions and classes);
- NumPy shapes/axes, broadcasting, matrix×matrix, standardization, (B,T,D) →
  `1_math_and_data/01_theory/04_arrays_and_axes.md`;
- `exp`/`ln`, sigmoid, `-ln(p)` → `1_math_and_data/01_theory/05_exp_and_log.md`;
- PyTorch basics (tensor, autograd, `nn.Linear`, `nn.Module`, optimizer,
  DataLoader) → `3_neural_networks/01_theory/02_pytorch_basics.md`
  (old 02–04 shifted to 03–05);
- stable softmax (subtract max) →
  `3_neural_networks/01_theory/01_neurons_and_backprop.md`;
- conv output size, kernel/padding/stride, out_channels →
  `11_multimodal_and_cv/01_theory/01_convolutions_basics.md`.
Structure: the over-packed attention lesson was split into
`4_nlp_and_transformers/01_theory/02_attention.md`, `03_transformer_block.md`,
`04_architectures_and_lm_training.md` (lifecycle → `05_`); section 4 examples
renamed to reading order (`01_bpe`, `02_attention`, `03_tiny_transformer`);
every self-check block now answers exactly one question.
Examples fixed because they didn't show what the lesson claimed (found only by
running them): group leakage in `2_classical_ml/02_examples/02_leakage.py`,
deep-tree overfitting in `03_trees.py`, per-epoch loss in
`3_neural_networks/02_examples/02_overfit.py`. Factual fix: "always says
не знаю" has zero false claims and undefined precision (0/0), not "perfect"
precision and not accuracy (7/01; corrected again 2026-10-14). Example and
solution code was rewritten from `;`-joined one-liners into commented blocks
— keep it that way: a from-zero learner reads this code (all
`03_exercises/check.py` files followed on 2026-10-14).
Inventory after the audit (root README): 43 lessons, 119 lesson self-check
questions + 5 review questions, 28 CPU examples verified by running, 6 that
need local weights, 11 exercise blocks.

## What the 2026-10-14 Review Pass Changed (keep consistent)

- **Self-check format is uniform repo-wide:** under `## Проверить
  понимание...` a numbered list of questions, then one
  `<summary>Разбор вопроса N</summary>` block per question, same order (the
  section 10/11 format). Never several questions in one paragraph followed
  by unlabelled "Разбор" blocks. Where one answer covered two sub-questions,
  they were merged into one numbered item. Quick detector: no file may match
  `</details>\s*<details>` together with an unlabelled
  `<summary>Разбор</summary>`.
- **Glossary:** the "term → lesson" table lives in `other/glossary.md`
  (linked from root README), not in `other/sources.md`. When a new concept
  gets a home lesson, add a row there.
- New homes: «граф вычислений» →
  `3_neural_networks/01_theory/02_pytorch_basics.md`;
  grounding → `6_retrieval_and_rag/01_theory/01_rag_basics.md`; structured
  output (provider JSON Schema) →
  `5_llm_applications/01_theory/01_structured_output.md`;
  hosted APIs (key in env var, per-token billing, rate limits) →
  `5_llm_applications/01_theory/02_runtime_contract.md`; native function
  calling / `tool` role → `9_agents_and_tools/01_theory/01_tool_calling.md`.
- Section 10 got a new lesson `02_inference_optimizations.md` (vLLM/
  PagedAttention, prefix caching, inference quantization, speculative
  decoding) instead of cramming those into `01_serving_basics.md`
  (Granularity Principle); release/drift renumbered to `03_`. TPOT is
  defined in `01_serving_basics.md`.
- `apply_chat_template(..., return_tensors='pt')` calls whose result is used
  as a tensor pass `return_dict=False` explicitly (default may change in
  future Transformers). Exception still pending: the dense
  `8_fine_tuning/02_examples/02_train_adapter.py` (not yet rewritten).
- Capstone timing (one statement everywhere): classifier CPU-baseline after
  section 2, document assistant after 7, classifier model parts after 8,
  diagnostic agent after 9–10.
- Profiles in root README: CPU, MODEL, EMBEDDING, GPU extension.
- Inventory now: 44 lessons, 125 lesson self-check questions + 5 review
  questions; example/exercise counts unchanged.

## What the 2026-11-04 Expansion Added (keep consistent)

Owner asked why the math is needed and to fill 2026 LLM-engineering gaps.
- Math: `00_why_math.md` (concept → where an LLM engineer meets it → what
  breaks); every math lesson ends with `## Где это встретится` (forward
  links); LLM bridges: cosine search (01), standard error of a proportion
  for prompt A/B (03), logits→softmax→temperature→logprobs→perplexity (05);
  optional parts marked «можно вернуться позже» / «Для любопытных».
- New homes: prompt/context engineering → `5/.../03_prompting_and_context`;
  tokens, cost, prompt caching in APIs, batch → `5/.../04_api_tokens_cost_
  caching`; llama.cpp/Ollama/LM Studio → `5/.../05_local_runtimes`; ANN,
  FAISS, pgvector, vector DBs → `6/.../04_vector_stores`; LLM-as-judge
  biases/calibration → `7/.../04_llm_as_judge` (kappa stays in 03); prompt
  injection & guardrails → `7/.../05_guardrails_and_injection`; MCP →
  `9/.../03_mcp` (01_tool_calling keeps a gloss); multi-agent & memory →
  `9/.../04_multi_agent_and_memory`; LLM observability, traces, OTel →
  `10/.../04_llm_observability`. All rows are in `other/glossary.md`.
- New offline examples: `9_agents_and_tools/02_examples/04_mcp_toy.py`,
  `10_serving_and_operations/02_examples/04_trace.py`.
- Facts not re-checked against live docs: default local ports (llama-server
  8080, Ollama 11434, LM Studio 1234, vLLM 8000), "Q4 ≈ 4.5–5 bits/weight".
- Inventory now: 54 lessons, 174 lesson self-check questions + 5 review
  questions, 30 CPU examples, 6 that need local weights, 11 exercise blocks.
- Known leftover: lessons in sections 3–4 still use unlabelled
  `<summary>Разбор</summary>`; math 04/05 interleave question/answer —
  normalize in a separate pass.

## Consolidated Review Block

The per-lesson self-check questions above are formative (mid-lesson,
collapsible, one learner at a time). A separate cross-topic review block
exists at `12_capstones/01_theory/review_questions.md`: 5 questions, each
deliberately spanning two sections instead of one, for self-test before the
capstone project. Keep it out of the sequential lesson order (it is NOT
"lesson 39") and linked separately from the section's own reading-order list
— see `12_capstones/README.md`'s own separate bullet for the exact pattern.
If another cross-topic review block is ever added elsewhere, follow this
same pattern: own file, explicitly excluded from lesson count, linked
outside the numbered reading order.

## Git & Workspace Discipline

- Treat this repo with the same default caution as any other: confirm scope
  before broad multi-file restructuring (splitting many lessons, renumbering
  sections), the same way plans get confirmed in the sibling devops repo's
  sessions, unless the user has explicitly said otherwise for a given task.
- Never create git worktrees for routine edits here.
- Do not commit without explicit instruction.
