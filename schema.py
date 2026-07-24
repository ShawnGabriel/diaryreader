"""
Single source of truth for the record shape the VLM must return.
Keep this in sync with prompts/extraction_prompt.md if you change it.
"""

FIELDS = [
    "wp",              # str  - waypoint number/label as written, e.g. "W.P. 1102"
    "date",            # str  - as written, e.g. "2025/7/31"
    "latitude",        # str  - as written, e.g. "29.03193"
    "longitude",       # str  - as written, e.g. "83.10229"
    "elevation_m",     # str or number - as written
    "species",         # str  - clean species/sign name only, "" if none
    "count",           # str or number - number associated with species, "" if none
    "notes_nepali",    # str  - Nepali text verbatim, "" if none, "[illegible]" if unreadable
    "notes_english",   # str  - English description; draft translation of Nepali labelled as such
    "flag",            # str or null - reason for human review, or null if none
]

XLSX_HEADERS = [
    "W.P.", "Date", "Latitude (N)", "Longitude (E)", "Elevation (m)",
    "Species", "Count", "Notes (Nepali - original)", "Notes (English)",
]
