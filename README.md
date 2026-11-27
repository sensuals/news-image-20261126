# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/sensuals/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/sensuals/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for make.fun's news-image-20261126 bounty: sum up the world's news of
Thursday 26 November 2026 in one image. The program copies the image to
`/output/entry.png`.

The image is a one-page broadsheet, "THE WORLD IN ONE DAY": 40 stories, all
of which happened or were first reported on Thursday 26 November 2026, with
13 drawn scenes, a world map with pins, a UTC timeline of the day, and a date
check that keeps older events (the 2008 Mumbai attacks, the 2025 Hong Kong
fire, NASA's 2022 DART impact) out of the day. Lead stories: the nor'easter
that postponed New York's 100th Macy's Thanksgiving parade, India marking 18
years since the 26/11 Mumbai attacks, and Gukesh vs Sindarov Game 3 of the
World Chess Championship ending in a 60-move draw, level at 1.5-1.5.

The image is drawn by `generate_image.py` (Pillow, no network, deterministic:
two runs write identical bytes) from the story list in that file. Sources are
named on every story: AP, Reuters, BBC, Guardian, PTI, FIDE, Al Jazeera, AFP,
NPR, CBC, DW, Euronews, SCMP, UEFA, IBU. Scenes are drawn illustrations, not
photographs.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image from its source data:

```sh
python3 generate_image.py entry.png
```

## Checks

- PNG, 1024 x 1024, 161,698 bytes (limit 1 MiB)
- Two runs of `generate_image.py` write byte-identical output
- `main.ts` copies `entry.png` to `/output/entry.png` unchanged

---

<sub>Entered on [make.fun](https://make.fun/?ref=a2tcya9q&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
