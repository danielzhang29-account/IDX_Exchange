import pandas as pd

SOLD_INPUT_FILE = "filtered_sold.csv"
LISTINGS_INPUT_FILE = "filtered_listings.csv"

SOLD_OUTPUT_FILE = "combined_sold_residential_with_mortgage_rates.csv"
LISTINGS_OUTPUT_FILE = "combined_listings_residential_with_mortgage_rates.csv"

sold = pd.read_csv(SOLD_INPUT_FILE)
listings = pd.read_csv(LISTINGS_INPUT_FILE)

print(f"Loaded sold dataset: {sold.shape[0]:,} rows, {sold.shape[1]:,} columns")
print(f"Loaded listings dataset: {listings.shape[0]:,} rows, {listings.shape[1]:,} columns")

fred_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

mortgage = pd.read_csv(
    fred_url,
    parse_dates=["observation_date"]
)

mortgage.columns = ["date", "rate_30yr_fixed"]

print(f"Fetched mortgage rate data: {mortgage.shape[0]:,} weekly observations")

mortgage["year_month"] = mortgage["date"].dt.to_period("M")

mortgage_monthly = (
    mortgage
    .groupby("year_month", as_index=False)["rate_30yr_fixed"]
    .mean()
)

print(f"Created monthly mortgage rate data: {mortgage_monthly.shape[0]:,} monthly observations")

sold["CloseDate"] = pd.to_datetime(sold["CloseDate"], errors="coerce")
listings["ListingContractDate"] = pd.to_datetime(
    listings["ListingContractDate"],
    errors="coerce"
)

sold["year_month"] = sold["CloseDate"].dt.to_period("M")
listings["year_month"] = listings["ListingContractDate"].dt.to_period("M")

sold_with_rates = sold.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

listings_with_rates = listings.merge(
    mortgage_monthly,
    on="year_month",
    how="left"
)

sold_null_rates = sold_with_rates["rate_30yr_fixed"].isna().sum()
listings_null_rates = listings_with_rates["rate_30yr_fixed"].isna().sum()

print("\nMortgage rate null check:")
print(f"Sold rows with missing mortgage rate: {sold_null_rates:,}")
print(f"Listings rows with missing mortgage rate: {listings_null_rates:,}")

if sold_null_rates > 0:
    print("\nWarning: Some sold rows did not match to a mortgage rate.")
    print("Sample unmatched sold rows:")
    print(
        sold_with_rates.loc[
            sold_with_rates["rate_30yr_fixed"].isna(),
            ["CloseDate", "year_month"]
        ].head()
    )

if listings_null_rates > 0:
    print("\nWarning: Some listings rows did not match to a mortgage rate.")
    print("Sample unmatched listings rows:")
    print(
        listings_with_rates.loc[
            listings_with_rates["rate_30yr_fixed"].isna(),
            ["ListingContractDate", "year_month"]
        ].head()
    )

if sold_null_rates == 0 and listings_null_rates == 0:
    print("\nValidation passed: No null mortgage rate values after merge.")

print("\nSold preview:")
sold_preview_cols = ["CloseDate", "year_month", "ClosePrice", "rate_30yr_fixed"]
sold_preview_cols = [col for col in sold_preview_cols if col in sold_with_rates.columns]
print(sold_with_rates[sold_preview_cols].head())

print("\nListings preview:")
listings_preview_cols = [
    "ListingContractDate",
    "year_month",
    "ListPrice",
    "rate_30yr_fixed"
]
listings_preview_cols = [
    col for col in listings_preview_cols if col in listings_with_rates.columns
]
print(listings_with_rates[listings_preview_cols].head())

sold_with_rates.to_csv(SOLD_OUTPUT_FILE, index=False)
listings_with_rates.to_csv(LISTINGS_OUTPUT_FILE, index=False)

print("\nSaved enriched datasets:")
print(f"Sold output file: {SOLD_OUTPUT_FILE}")
print(f"Listings output file: {LISTINGS_OUTPUT_FILE}")