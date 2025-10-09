import csv
import random
import math

# How many rows to generate
N_ROWS = 1500  # set to 1000 if you prefer

HEADER = [
    "Administrative",
    "Administrative_Duration",
    "Informational",
    "Informational_Duration",
    "ProductRelated",
    "ProductRelated_Duration",
    "BounceRates",
    "ExitRates",
    "PageValues",
    "SpecialDay",
    "Month",
    "OperatingSystems",
    "Browser",
    "Region",
    "TrafficType",
    "VisitorType",
    "Weekend",
    "Revenue",
]

MONTHS = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SPECIAL_DAY_VALUES = [0.0, 0.2, 0.4, 0.6, 0.8]
VISITOR_TYPES = ["Returning_Visitor", "New_Visitor", "Other"]

def weighted_int(low, high, bias_low=True):
    """
    Return an int in [low, high] with a bias toward low values if bias_low=True,
    else bias toward high values. Uses a simple power curve for bias.
    """
    u = random.random()
    power = 2.0
    if bias_low:
        v = u ** power
    else:
        v = 1 - (u ** power)
    return low + int(v * (high - low + 1))

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def roundf(x, ndigits):
    return float(f"{x:.{ndigits}f}")

def make_row():
    # Administrative pages: typically small counts
    administrative = weighted_int(0, 27, bias_low=True)

    # Administrative duration: scaled to the count, plus noise
    if administrative == 0:
        admin_dur = 0.0
    else:
        # avg 30–90 sec per page, with noise
        admin_dur = sum(max(0, random.gauss(60, 20)) for _ in range(administrative))

    # Informational pages: often small
    informational = weighted_int(0, 24, bias_low=True)
    if informational == 0:
        info_dur = 0.0
    else:
        info_dur = sum(max(0, random.gauss(45, 15)) for _ in range(informational))

    # Product-related pages: can be large; skewed toward lower but broader
    product_related = weighted_int(1, 300, bias_low=True)
    # Product-related duration: proportional with noise (avg 35–75 sec/page)
    product_dur = sum(max(0, random.gauss(55, 18)) for _ in range(product_related))

    # Rates: bounce and exit — small decimals
    bounce = clamp(random.gauss(0.03, 0.02), 0.0, 0.2)
    exit_rate = clamp(random.gauss(0.07 + bounce * 0.5, 0.04), 0.0, 0.35)

    # Special day (discrete)
    special_day = random.choices(
        SPECIAL_DAY_VALUES, weights=[60, 15, 12, 8, 5], k=1
    )[0]

    # Month
    month = random.choice(MONTHS)

    # OS, Browser, Region, TrafficType
    os_ = random.randint(1, 8)
    browser = random.randint(1, 13)
    region = random.randint(1, 9)
    traffic = random.randint(1, 20)

    # VisitorType
    visitor = random.choices(
        VISITOR_TYPES, weights=[70, 27, 3], k=1
    )[0]

    # Weekend flag (as TRUE/FALSE strings)
    weekend_bool = random.random() < 0.25
    weekend = "TRUE" if weekend_bool else "FALSE"

    # PageValues: often 0 unless some intent; correlate loosely with product pages and lower bounce/exit
    # Start with 0 baseline
    page_values = 0.0
    # Derive a "intent score"
    intent = 0.0
    intent += 0.0008 * product_dur
    intent += (0.12 - bounce) * 2.5
    intent += (0.15 - exit_rate) * 2.0
    if visitor == "Returning_Visitor":
        intent += 0.8
    if special_day >= 0.6:
        intent += 0.5
    if month in ("Nov", "Dec"):
        intent += 0.4
    if not weekend_bool:
        intent += 0.2

    intent = clamp(intent, -1.5, 3.5)
    # If intent is decent, assign nonzero page values
    if intent > 0.5:
        # Skewed distribution: most are small, some large
        base_val = max(0, random.gauss(30 * intent, 20))
        page_values = base_val

    # Purchase probability (Revenue) as a function of features
    p = 0.03
    p += 0.18 if page_values > 0 else 0.0
    p += 0.09 if visitor == "Returning_Visitor" else 0.0
    p += 0.06 if special_day >= 0.6 else 0.0
    p += 0.05 if month in ("Nov", "Dec") else 0.0
    p += 0.03 if not weekend_bool else -0.015
    p -= 0.6 * bounce
    p -= 0.35 * max(0.0, exit_rate - 0.05)

    p = clamp(p, 0.0, 0.9)
    revenue_bool = random.random() < p

    # If marked as purchase but page_values is 0, give it a small positive value
    if revenue_bool and page_values == 0.0:
        page_values = max(0.5, random.gauss(35, 15))

    revenue = "TRUE" if revenue_bool else "FALSE"

    row = [
        administrative,
        roundf(admin_dur, 2),
        informational,
        roundf(info_dur, 2),
        product_related,
        roundf(product_dur, 2),
        roundf(bounce, 5),
        roundf(exit_rate, 5),
        roundf(page_values, 2),
        roundf(special_day, 1),
        month,
        os_,
        browser,
        region,
        traffic,
        visitor,
        weekend,
        revenue,
    ]
    return row

def main():
    out_path = "test.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for _ in range(N_ROWS):
            writer.writerow(make_row())
    print(f"Wrote {N_ROWS} rows to {out_path}")

if __name__ == "__main__":
    random.seed(42)  # for reproducibility; remove if you want different data each run
    main()
