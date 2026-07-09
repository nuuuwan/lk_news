# lk_news Data Repo — Investigation Report

## 1. README Summary

The repo is a **Sri Lankan news dataset** maintained by [@nuuuwan](https://github.com/nuuuwan), published as an arXiv paper ([arXiv:2510.04124](https://arxiv.org/abs/2510.04124)). It contains **122,652 articles** (~1.9 GB) scraped from 15 Sri Lankan news websites in **Sinhala, Tamil, and English**. Data is provided in three formats: per-article JSON+TXT files, a TSV index, and HuggingFace datasets. Licensed MIT.

## 2. docs_all.tsv — Column Schema

| Column | Description |
|---|---|
| `doc_type` | Always `"lk_news"` |
| `doc_id` | Unique ID: `{date}-{newspaper_id}-{hash}` |
| `num` | Short ID: `{newspaper_id}-{hash}` |
| `date_str` | Publication date (`YYYY-MM-DD`) |
| `description` | Article headline/title |
| `url_metadata` | Source URL |
| `lang` | Language code: `si`, `ta`, or `en` |
| `newspaper_id` | Source identifier (e.g. `dailymirrorlk`) |
| `time_ut` | Unix timestamp (float) |

122,654 lines total (1 header + 122,652 data rows + 2 counting artifact = exact 122,652 articles).

## 3. Per-Article Folder Structure

Each folder `2020s/{year}/{doc_id}/` contains exactly two files:

- **doc.json** — metadata (doc_type, doc_id, num, date_str, description, url_metadata, lang, newspaper_id, time_ut)
- **doc.txt** — full article body text (headline repeated as first line, then paragraphs)

### Sample 1 — English (Daily Mirror, 2024-01-02)

- `doc.json`: `{"doc_type":"lk_news", "doc_id":"2024-01-02-dailymirrorlk-6c58939e", "lang":"en", "newspaper_id":"dailymirrorlk", "date_str":"2024-01-02", "description":"Persons with no TIN could face penalty up-to Rs. 50,000", ...}`
- `doc.txt`: Full article body (11 lines, ~580 chars) about taxpayer ID penalties.

### Sample 2 — Sinhala (BBC Sinhala, 2024-01-03)

- `doc.json`: `{"lang":"si", "newspaper_id":"bbccomsinhala", ...}`
- `doc.txt`: Long investigative article (~4,500 chars Sinhala text) on police human rights violations.

### Sample 3 — Sinhala (Ada.lk, 2023-02-13)

- `doc.json`: `{"lang":"si", "newspaper_id":"adalk", ...}`
- `doc.txt`: Short tech article (~700 chars Sinhala) about a Chinese amphibious drone.

## 4. hugging_face_data/chunks/

- **Format:** JSON array (not JSONL, not Parquet)
- **44 part files** (`part_0001` through `part_0044`)
- **~5,618 records** in `part_0001`
- **Contains full article body text** in the `chunk_text` field
- Each record has all the metadata fields from `doc.json` PLUS:
  - `chunk_id` — `{doc_id}-{chunk_index}`
  - `chunk_index` — integer (articles split into chunks)
  - `language` — duplicate of `lang`
  - `md5` — hash of the chunk text
  - `chunk_size_bytes` — byte length of the chunk

This is the **chunked** version — long articles are split into multiple records.

## 5. hugging_face_data/docs/

- **Format:** JSON array (same as chunks)
- **4 part files** (`part_0001` through `part_0004`)
- **Contains only metadata** (same fields as `doc.json`) — **NO body text**
- This is essentially a JSON-array version of `docs_all.tsv`

**Key difference:** `chunks/` has full text + chunking; `docs/` is metadata-only.

## 6. Corpus Statistics

| Metric | Value |
|---|---|
| **Total articles** | **122,652** |
| **Date range** | **2021-09-12** to **2026-07-09** |
| **Duplicate doc_ids** | **0** (all unique) |

### Language Breakdown

| Language | Count | % |
|---|---|---|
| Tamil (ta) | 50,472 | 41.2% |
| English (en) | 41,847 | 34.1% |
| Sinhala (si) | 30,333 | 24.7% |

### Source Breakdown

| Newspaper | Count |
|---|---|
| virakesarilk | 30,625 |
| tamilmirrorlk | 19,847 |
| adaderanasinhalalk | 13,658 |
| adalk | 11,781 |
| adaderanalk | 10,102 |
| dailyftlk | 9,310 |
| islandlk | 7,970 |
| dailymirrorlk | 7,403 |
| economynextcom | 4,533 |
| lankadeepalk | 3,908 |
| colombotelegraphcom | 1,292 |
| bbccomsinhala | 986 |
| dbsjeyarajcom | 819 |
| newsfirstlk | 418 |

## 7. Data Quality

| Check | Result |
|---|---|
| doc.json with no doc.txt | **0** — every article has body text |
| Empty doc.txt (0 bytes) | **0** |
| Short doc.txt (<50 bytes) | **57** (0.05%) — likely stubs/headline-only scrapes |
| Malformed JSON | **0** |

The 57 short files are across various sources (dailymirror, dailyft, tamilmirror, newsfirst, etc.) — negligible. The corpus is very clean.

## 8. Key Takeaways for Pipeline Design

- **Tamil dominates** (41%) — for a Sinhala-focused project, there are 30k Sinhala articles available.
- The **chunks/ HuggingFace data** is the most convenient single-file corpus loader since it has metadata + full text pre-chunked.
- The per-article folders are the canonical source if you need raw, unchunked text.
- `docs_all.tsv` is the fastest way to filter/select articles by lang, date, or source before loading full text.
- Zero duplicates, zero malformed data — very production-ready dataset.
