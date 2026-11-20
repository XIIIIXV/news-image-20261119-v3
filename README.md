# Thursday 19 November 2026 — The World in One Day (v3)

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/XIIIIXV/news-image-20261119-v3/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/XIIIIXV/news-image-20261119-v3/reward.svg)](https://make.fun/bounty/news-image-20261119)

A 1024×1024 front page for the make.fun **news-image-20261119** bounty
($250, free entry, deadline 2026-11-21T00:00:00Z): all 52 news stories
from a single day — Thursday 19 November 2026 — on one page. Round 2
rebuild of the round-1 entry (98.2873%, rank #753), rebuilt to the
top-10 standard.

## What it is

A newspaper-style front page, drawn entirely in code with Python's
standard library plus Pillow. No photos, no external images, no network:
every illustration is a flat vector-style drawing (rectangles, ellipses,
polygons, lines), and every story comes from `stories.json`.

The page carries:

- A huge serif masthead, **Thursday 19 November 2026**, with a red
  strap line naming the day's three biggest stories.
- A stats strip: 3 presidents at one table, the 9–6 World Court vote,
  the $120bn COP31 aid cut, Anthropic's $81bn IPO, the 109–0 Danish
  Arctic vote, and Australia's 4.9% jobless rate.
- Colour-coded region and field strips covering all 7 regions and
  9 fields.
- A UTC timeline of the day in 8 beats, from the overnight Riyadh
  missile intercept to the late Senate war-powers vote.
- **16 illustrated cards** (4 large, 6 medium, 6 small) with headline,
  deck, source and region/field tag — led by the Trump–Xi–Putin summit,
  the World Court Myanmar ruling, the COP31 draft, the Anthropic IPO,
  the Riyadh missile, Cyclone Akvan, GTA VI, Korea's top court, the
  Arctic pact and the Kerch Bridge strike.
- A world map with 16 numbered pins, one per card.
- **ALSO ON THURSDAY**, stories 17–52 in two columns.
- **THE DAY IN NUMBERS**: 200,000 evacuated, 15.9m GTA VI pre-orders,
  11,000 migrants in the Canaries, the 51–48 Senate vote, 500,000
  Korean exam sitters and 78,000 hit by El Niño in Bolivia.
- A HOW SURE confidence legend (CONFIRMED 2+ outlets / REPORTED one
  outlet / CLAIM one party) and a red DATE CHECK box that names, one
  by one, the stories left out as other days' news.

## What v3 fixes over round 1

- **Date discipline.** Round 1 carried the Van Gogh $190.4m sale as a
  main story — it was first reported on **18 November**, not the 19th.
  v3 removes it from the cards and from the numbers strip, and names it
  in the DATE CHECK as excluded, alongside Voyager 1, the EU €45bn
  Ukraine loan, Iran firing on Kuwait and Bahrain, Nvidia results,
  Jefferies named for US speaker, and Carney on China ties. The
  Anthropic $83 share price was set 18 Nov (trading began 19 Nov), and
  the DATE CHECK says so. Card 15 is now Italian author Corrado Augias,
  who died on 19 November 2026 aged 91 (verified: Wikipedia, LaPresse).
  The DATE CHECK also lists what was not yet due on 19 Nov: COP31's
  scheduled close and Cyclone Akvan's landfall (both 20 Nov).
- **Craft.** Every illustration is one simple, bold, flat icon that
  reads at small size — round 1's motifs smeared and overlapped at card
  height. The world map is a real equirectangular outline of the
  continents; round 1's map was unrecognisable grey blobs.
- **Confidence legend** now reads CONFIRMED (2+ outlets) / REPORTED
  (one outlet) / CLAIM (one party), as the top entries do.

## How to run

```bash
python3 gen_image.py   # renders entry.png in this directory
python3 main.py        # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

Requirements: Python 3 and Pillow (`pip install pillow`). The render is
fully deterministic — running `gen_image.py` twice produces identical
bytes.

## Coverage

52 stories: 16 featured cards + 36 briefs. 7 regions (Americas 12,
Asia 11, Europe 9, Middle East 7, Africa 6, Oceania 4, Global 3) and
9 fields (Diplomacy 11, Politics 10, War 9, Economy 7, Climate 6,
Culture 3, Labour 3, Business 2, Science 1). All stories are 19
November 2026 news.
