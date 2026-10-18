# WSU-COS 207: The Data & Algorithm Laboratory (course files)

Faculty of Computing, Wellspring University · Version 1.0 (October 2026)

These are the files you need for the WSU-COS 207 practicals. Use them with the Practical Manual.

## Getting the files

Download them as a ZIP (green **Code** button, then **Download ZIP**) or, once you have Git installed:

```bash
git clone <this repository's URL>
```

Then copy the `data` folder into your own `cos207` project folder (Practical 1, Step 1). All paths in the manual assume:

```
cos207/
    data/
        survey_raw.csv    246 rows: raw student survey with deliberate errors (Practical 4)
        survey_clean.csv  219 rows: the cleaned survey, for anyone who could not finish Practical 4
                          (Practicals 5 and 9 to 13)
        lab_power.csv     48 months of laboratory electricity use, 2022-2025 (Practical 12)
        feedback.txt      8 lines of messy free-text feedback (Practical 2)
    p01/ p02/ ... p13/    your own work, one folder per practical
```

## Before Practical 1

Follow the manual's Preliminary section (Setting Up Your Computer), then, inside your virtual environment:

```bash
python -m pip install -r requirements-course.txt
python check_setup.py        # must end with ALL CHECKS PASSED
```

## Other files

- `make_data.py` regenerates every file in `data/` exactly (fixed seed 207): `python make_data.py`
- Appendix D of the manual describes every column.

All data is fictional; no real person is described. Do not post the files elsewhere online.

## Copyright

Copyright © 2026 A. S. Olayinka, T. C. Olayinka, B. E. Akilo and S. A. Oyedotun. All rights reserved. Registered WSU-COS 207 students may use these files for their course work. See `NOTICE.txt`.
