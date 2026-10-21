"""
Retail Sales Performance Analysis
---------------------------------
Analyze a retail (Superstore) sales dataset using pandas and matplotlib.
Cleans the data, answers key business questions, saves charts to a
"charts" folder, and writes a plain-text summary of the findings.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. SETTINGS

CSV_FILE = "train.csv"
CHART_FOLDER = "charts"            # charts will be saved here
os.makedirs(CHART_FOLDER, exist_ok=True)

def save_chart(filename, title, xlabel="", ylabel=""):
    """ Add labels to the current chart, save it as an image, then close it. """
    plt.title(title, fontsize=13, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_FOLDER, filename), dpi=150)
    plt.close()

# 2. LOAD THE DATA
df = pd.read_csv(CSV_FILE)          # read CSV file into a DataFrame
print(f"Loaded {len(df):,} rows and {df.shape[1]} columns.")

# 3. CLEAN THE DATA
# Dates are written day-first (eg.16/06/2017), so we tell pandas that.
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# Remove duplicate orders (ignoring Row ID, which is always unique).
duplicates = df.drop(columns="Row ID").duplicated()
print(f"Duplicate rows removed: {duplicates.sum()}")
df = df[~duplicates]

# Report missing values (leave Postal Code alone)
missing = df.isna().sum()
print("Missing values:", missing[missing > 0].to_dict() or "none")

# Create new helpful columns
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["YearMonth"] = df["Order Date"].dt.to_period("M")
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# 4. ANALYZE: group the data to answer business questions
total_sales = df["Sales"].sum()
num_orders = df["Order ID"].nunique()
num_customers = df["Customer ID"].nunique()

yearly = df.groupby("Year")["Sales"].sum()
yearly_growth = yearly.pct_change() * 100                       # year-over-year % change

monthly = df.groupby("YearMonth")["Sales"].sum()                # every month separately

by_calendar_month = df.groupby("Month")["Sales"].sum()          # merge all Januaries

by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
by_subcat = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
by_state = df.groupby("State")["Sales"].sum().sort_values(ascending=False)
by_segment = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
ship_days = df.groupby("Ship Mode")["Ship Days"].mean().sort_values()

# 5.CHARTS
# Chart 1: Sales per year
yearly.plot(kind="bar", color="#2a6fdb", rot=0)
save_chart("1_sales_by_year.png", "Total Sales by Year", "Year", "Sales ($)")

#Chart 2: Monthly sales trend
plt.figure(figsize=(10, 4.5))
plt.plot(monthly.index.to_timestamp(), monthly.values, marker="o", color="#2a6fdb")
plt.grid(alpha=0.3)
save_chart("2_monthly_sales_trend.png", "Monthly Sales Trend", "Month", "Sales ($)")

#Chart 3: Sales by category
by_category.plot(kind="bar", color="#2a6fdb", rot=0)
save_chart("3_sales_by_category.png", "Sales by Category", "", "Sales ($)")

# Chart 4: Top 10 sub-categories (horizontal bars, biggest on top)
plt.figure(figsize=(9, 5))
by_subcat.head(10).sort_values().plot(kind="barh", color="#2a6fdb")
save_chart("4_top_subcategories.png", "Top 10 Sub-Categories by Sales", "Sales ($)", "")
 
# Chart 5: Sales by region
by_region.plot(kind="bar", color="#2a6fdb", rot=0)
save_chart("5_sales_by_region.png", "Sales by Region", "", "Sales ($)")
 
# Chart 6: Top 10 states
plt.figure(figsize=(9, 5))
by_state.head(10).sort_values().plot(kind="barh", color="#2a6fdb")
save_chart("6_top_states.png", "Top 10 States by Sales", "Sales ($)", "")

print(f"Saved 6 charts to the '{CHART_FOLDER}' folder.")

# 6. SUMMARY OF FINDINGS
best_year = yearly.idxmax()
best_month_num = by_calendar_month.idxmax()
month_name = pd.Timestamp(2000, best_month_num, 1).strftime("%B")

top_cat = by_category.index[0]
top_cat_share = by_category.iloc[0] / total_sales * 100

top_region = by_region.index[0]
top_region_share = by_region.iloc[0] / total_sales * 100
top_state_share = by_state.head(3).sum() / total_sales * 100

last_growth = yearly_growth.dropna().iloc[-1]
last_year = yearly.index[-1]

lines = [
    "RETAIL SALES PERFORMANCE ANALYSIS - KEY FINDINGS",
    "-" * 50,
    f"Total sales: ${total_sales:,.0f} across {num_orders:,} orders "
    f"from {num_customers:,} customers.",
    f"Average order value: ${total_sales / num_orders:,.2f}",
    "",
    "Sales by year:",
]
for year, value in yearly.items():
    growth = yearly_growth[year]
    note = "" if pd.isna(growth) else f" ({growth:+.1f}% vs previous year)"
    lines.append(f" {year}: ${value:,.0f}{note}")

lines += [
    "",
    f"Best year: {best_year}. Sales in {last_year} changed {last_growth:+.1f}% "
    "compared with the year before.",
    f"Strongest calendar month overall: {month_name}.",
    f"Top category: {top_cat} ({top_cat_share:.1f}% of sales).",
    f"Top sub-category: {by_subcat.index[0]} (${by_subcat.iloc[0]:,.0f}).",
    f"Top region: {top_region} ({top_region_share:.1f}% of sales).",
    f"Top 3 states ({', '.join(by_state.index[:3])}) account for "
    f"{top_state_share:.1f}% of sales.",
    f"Top customer segment: {by_segment.index[0]} "
    f"({by_segment.iloc[0] / total_sales * 100:.1f}% of sales).",
    "",
    "Average shipping time (days) by ship mode:",
]
for mode, days in ship_days.items():
    lines.append(f"  {mode}: {days:.1f}")
 
summary = "\n".join(lines)
print("\n" + summary)
 
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
print("\nSummary saved to summary.txt")

