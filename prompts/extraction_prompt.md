You are transcribing one page of a handwritten wildlife field notebook.
Entries are typically written like:

    W.P. 1102 Date- 2025/7/31
    N.29.03193' E083.10229'
    Ele-4489m Snow Leopard scat.M 1

Each entry is separated by a horizontal line. Not every entry has all
fields — some are just a starting/ending point or a camera trap install
with no species observed. Some notes mix English and Nepali (Devanagari)
in the same line.

Return a JSON array. Each element is one waypoint entry with exactly
these fields:

- "wp": the waypoint label as written, including the "W.P." prefix if
  present. If a waypoint number is crossed out, duplicated, or you
  otherwise can't tell what it should be, transcribe your best reading
  and explain the issue in "flag" — never silently renumber or guess a
  "corrected" number.
- "date": as written (don't reformat/reorder it).
- "latitude", "longitude": the decimal-minutes numbers as written
  (e.g. "29.03193"), digits only, no letter prefix.
- "elevation_m": the number as written, no "m" suffix.
- "species": ONLY the clean species/sign name (e.g. "Blue sheep",
  "Marmot", "Snow Leopard"). Do not include any count or hyphenated
  number here. Leave "" (empty string) if the entry is logistics-only
  (starting point, ending point, camera install, battery swap) with no
  wildlife observed.
- "count": the number that follows the species in the notebook (e.g. the
  "19" in "Blue sheep-19", the "11" in "Marmot-11"). Leave "" if no
  number was written (e.g. "Live Snow Leopard", a scrape/scat sign with
  no headcount given).
- "notes_nepali": any Nepali-language (Devanagari script) text in the
  entry, transcribed EXACTLY as written — verbatim script, no
  translation, no paraphrase. Leave "" if there is no Nepali text in
  this entry. If Nepali text is present but you genuinely cannot read it
  even at full resolution, write "[illegible]" here rather than
  guessing at characters.
- "notes_english": a plain English description of the entry — camera
  name, battery type used, "starting point" / "ending point", etc.
  (most of this is already written in English in the notebook, so this
  is mostly direct transcription, not translation). If notes_nepali is
  non-empty and not "[illegible]", ALSO include a translation of it
  here, clearly prefixed with "DRAFT translation - please correct:" —
  this is a first pass for a Nepali speaker to check, not a final
  answer. Never invent plausible-sounding text you're not confident in;
  say so instead.
- "flag": a short string explaining any reason a human should
  double-check this row (ambiguous digit, illegible word, duplicate/
  crossed-out waypoint number, missing coordinates, unusual count,
  etc.), or null if nothing needs review.

Rules:
- One JSON object per waypoint entry on the page. If the page has no
  entries (e.g. a cover page), return an empty array [].
- Never leave a field out — use "" (or null for "flag") rather than
  omitting a key.
- Do not merge two waypoint entries into one, and do not split one entry
  into two.
- Do not "correct" the notebook's handwriting into what seems more
  plausible — transcribe what's actually written, and flag anything odd
  instead of silently fixing it.
- Output ONLY the JSON array. No prose before or after it.
