# Field Notes Transcriber

Turns photographed/scanned field notebook pages (waypoint logs like the
Hira 2025 Jul-Aug notebook) into a structured Excel workbook — one row per
waypoint, one tab per source PDF. Built so you (or anyone on the team) can
run and tweak this without needing an AI assistant in the loop each time.

## What it does

1. `pdf_to_images.py` — renders each PDF page to a high-res PNG.
2. `extract.py` — sends each page image to a vision-language model (VLM)
   with a strict prompt (see `prompts/extraction_prompt.md`) and gets back
   structured JSON per waypoint.
3. `build_spreadsheet.py` — merges the JSON from every page/PDF into one
   `.xlsx`, with the columns below, low-confidence rows highlighted yellow
   with a review comment, and Nepali text rendered in a font that displays
   Devanagari correctly in Excel.

## Output columns

| Column | Meaning |
|---|---|
| W.P. | Waypoint number as written (kept even if it looks like a typo/duplicate in the notebook — flagged instead of silently fixed) |
| Date | As written |
| Latitude / Longitude | Decimal-minutes as written (`N.29.03193'` etc.) |
| Elevation (m) | As written |
| Species | Clean species/sign name only (e.g. "Blue sheep"), blank for logistics-only entries (starting/ending points, camera installs, battery swaps) |
| Count | The number associated with the species (e.g. the `19` in "Blue sheep-19"), blank if none was written |
| Notes (Nepali - original) | Any Nepali-language text, transcribed **verbatim** — no translation folded in |
| Notes (English) | English description of the entry, plus a clearly labelled **draft** translation of the Nepali note if there is one — meant to be corrected by a Nepali reader, not trusted as final |

Every row that needed a judgment call (ambiguous digit, illegible note,
duplicate waypoint number) is highlighted and gets a comment on the W.P.
cell explaining exactly what to check. **Treat the output as a first draft
that needs a human pass, not final data** — that's true no matter which
model you point this at.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your API key + model choice
```

Drop PDFs into `data/pdfs/`, then:

```bash
python run_pipeline.py
```

Each PDF becomes one tab in `outputs/field_notes.xlsx` (tab name = PDF
filename). Re-running only re-processes new/changed PDFs (see "Caching"
below).

## Which model to use

This was built and tested against Claude Sonnet. For a fully open-source,
self-serve setup, **Qwen3-VL** is the best current fit:

- It's Apache-2.0 licensed, genuinely open-weight, and its OCR/handwriting
  performance on independent evals is competitive with (sometimes ahead
  of) closed frontier models on document/OCR benchmarks.
- It comes in sizes from ~2B up to 235B-A22B (mixture-of-experts), so you
  can scale to your hardware — or skip hardware entirely and call it
  through a hosted API.
- It has explicit multilingual OCR training, which matters here — this
  notebook mixes English and Nepali (Devanagari) in the same handwritten
  line, and this is the kind of case where a model *not* trained on much
  Devanagari OCR data will confidently produce fluent-looking nonsense.

**Recommended default: `qwen/qwen3-vl-235b-a22b-instruct` via [OpenRouter](https://openrouter.ai)**
(no GPU needed, pay-per-token, cheap — a few cents per notebook page).
This is what `.env.example` is pre-configured for.

**If you'd rather self-host** (data never leaves your machine): `Qwen3-VL-32B-Instruct`
or `Qwen3-VL-30B-A3B` run on a single modern GPU (or a quantized build on
a Mac) and get you most of the way to the 235B model's accuracy for a
fraction of the cost. Serve it with `vllm serve Qwen/Qwen3-VL-32B-Instruct`
and point `.env`'s `VLM_BASE_URL` at `http://localhost:8000/v1` — the
client code doesn't change, since it just talks OpenAI-compatible chat
completions either way.

**Swapping models later:** anything that exposes an OpenAI-compatible
`/chat/completions` endpoint with image input works — Gemini, GPT, other
Qwen sizes, a different open model entirely. Change `VLM_BASE_URL`,
`VLM_API_KEY`, and `VLM_MODEL` in `.env`, nothing else.

**Worth re-checking before you rely on this long-term:** which model is
"best" for OCR/handwriting shifts every few months. Before committing,
skim a current comparison (search something like "best open source vision
language model OCR handwriting [current year]") rather than assuming this
README's pick is still the frontier.

## Tuning the extraction

`prompts/extraction_prompt.md` is the entire behavior spec for the model —
edit it directly to change: how confident it needs to be before flagging
a row, what counts as a "species," how it should format dates, etc. No
code changes needed for most tweaks. `schema.py` defines the JSON shape
the model must return; keep the prompt and schema in sync if you change
either.

## Caching

`outputs/.cache/` stores the raw per-page model output keyed by a hash of
the page image, so re-running the pipeline after adding one new PDF
doesn't re-spend money re-transcribing pages you've already done. Delete
that folder to force a full re-run.

## Known limitations

- Handwriting this messy will always need a human review pass — this
  tool gets you a fast, structured first draft with problem rows flagged,
  not a finished dataset.
- Devanagari handwriting recognition is the weakest link. If your team
  has a Nepali reader, prioritize their time on the "Notes (Nepali -
  original)" column, since a wrong transcription there quietly poisons
  the "Notes (English)" draft translation too.
