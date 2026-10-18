"""Generate the fictional WSU-COS 207 datasets (seeded, reproducible)."""
import csv, math, random, os

random.seed(207)
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

PROGS = ["CSC", "SEN", "CYB", "IFT", "DTS"]
FIELDS = ["record_id", "matric_no", "programme", "study_hours", "attendance_pct", "sleep_hours",
          "screen_hours", "commute_mins", "uses_library", "test_score", "final_score"]


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def make_survey(n=240):
    rows = []
    for i in range(1, n + 1):
        prog = random.choices(PROGS, weights=[30, 20, 18, 17, 15])[0]
        study = clamp(random.gauss(12, 4.5), 1, 30)
        att = clamp(random.gauss(80, 11), 35, 100)
        sleep = clamp(random.gauss(6.6, 1.0), 3.5, 9.5)
        screen = clamp(random.gauss(5.5, 2.0) - 0.08 * study, 1, 12)
        commute = int(clamp(random.expovariate(1 / 25), 2, 120))
        lib = "Yes" if random.random() < 0.35 + 0.015 * study else "No"
        bonus = {"CSC": 2, "SEN": 1.5, "CYB": 0, "IFT": -1, "DTS": 1}[prog]
        final = clamp(22 + 1.9 * study + 0.25 * att + 1.6 * (sleep - 6.5) - 0.9 * screen + bonus + random.gauss(0, 8), 5, 99)
        test = clamp(round(final * 0.3 + random.gauss(0, 2.5)), 0, 30)
        rows.append({"record_id": i, "matric_no": f"WSU/2024/{1000 + i:04d}", "programme": prog,
                     "study_hours": round(study, 1), "attendance_pct": round(att), "sleep_hours": round(sleep, 1),
                     "screen_hours": round(screen, 1), "commute_mins": commute, "uses_library": lib,
                     "test_score": int(test), "final_score": round(final)})
    return rows


def dirty(rows):
    """Inject realistic data-entry problems into a copy of the clean rows."""
    out = [dict(r) for r in rows]
    pick = random.sample(range(len(out)), 60)
    it = iter(pick)
    # programme spelling / case / spaces (8)
    for _ in range(8):
        r = out[next(it)]
        r["programme"] = random.choice([" " + r["programme"].lower(), r["programme"].capitalize() + " ", r["programme"].lower()])
    # missing values (10)
    for col in ["study_hours", "sleep_hours", "attendance_pct", "final_score", "screen_hours"] * 2:
        out[next(it)][col] = random.choice(["", "NA", "n/a"])
    # out-of-range numbers (6)
    out[next(it)]["attendance_pct"] = 140
    out[next(it)]["attendance_pct"] = -5
    out[next(it)]["study_hours"] = -3
    out[next(it)]["sleep_hours"] = 26
    out[next(it)]["final_score"] = 105
    out[next(it)]["test_score"] = 45
    # words instead of numbers (3)
    out[next(it)]["study_hours"] = "twelve"
    out[next(it)]["commute_mins"] = "about 20"
    out[next(it)]["sleep_hours"] = "7 hrs"
    # malformed matric numbers (3)
    r = out[next(it)]; r["matric_no"] = r["matric_no"].replace("/", "-")
    r = out[next(it)]; r["matric_no"] = r["matric_no"].lower()
    r = out[next(it)]; r["matric_no"] = "WSU/2024/12"
    # yes/no variants (4)
    for v in ["yes", "Y", "no ", "N"]:
        out[next(it)]["uses_library"] = v
    # exact duplicate rows (6)
    dups = [dict(out[j]) for j in random.sample(range(len(out)), 6)]
    for d in dups:
        out.insert(random.randrange(len(out)), d)
    return out


def write_csv(name, rows):
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def make_power():
    rows = []
    for k in range(48):
        year, month = 2022 + k // 12, k % 12 + 1
        temp = 27.5 + 2.6 * math.cos((month - 3) / 12 * 2 * math.pi) + random.gauss(0, 0.5)
        sem = 1.0 if month in (1, 2, 3, 4, 5, 9, 10, 11) else 0.72
        kwh = (3200 + 28 * k) * sem + 85 * (temp - 27) + random.gauss(0, 120)
        rows.append({"month": f"{year}-{month:02d}", "mean_temp_c": round(temp, 1), "kwh": round(kwh)})
    with open(os.path.join(DATA, "lab_power.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["month", "mean_temp_c", "kwh"])
        w.writeheader()
        w.writerows(rows)


def make_feedback():
    lines = [
        "WSU/2024/1007 ; csc ;  The labs were USEFUL but the room was too hot.  ",
        "WSU/2024/1012;SEN;I liked the testing practical, testing found two bugs in my code!",
        "wsu/2024/1023 ; cyb ; More time for recursion please. Recursion was hard.",
        "WSU/2024/1031 ; IFT ; good",
        "WSU/2024/1044 ; dts ;   Pandas made the statistics practical much faster.",
        "WSU/2024/1050 ; Csc ; The timing experiment surprised me: sorted() was very fast.",
        "WSU/2024/1068 ; SEN ; Please share the datasets earlier.",
        "WSU/2024/1071 ; csc ; Git was confusing at first, but commits saved my work twice.",
    ]
    with open(os.path.join(DATA, "feedback.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    clean = make_survey()
    write_csv("survey_raw.csv", dirty(clean))
    make_power()
    make_feedback()
    print("data written")
