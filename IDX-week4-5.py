BASE_PATH = "."

SOLD_INPUT_FILE = os.path.join(
    BASE_PATH,
    "combined_sold_residential_with_mortgage_rates.csv"
)

LISTINGS_INPUT_FILE = os.path.join(
    BASE_PATH,
    "combined_listings_residential_with_mortgage_rates.csv"
)

OUTPUT_DIR = os.path.join(BASE_PATH, "weeks_4_5_outputs")

SOLD_OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "cleaned_sold_analysis_ready.csv"
)

LISTINGS_OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "cleaned_listings_analysis_ready.csv"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

DATE_FIELDS = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

NUMERIC_FIELDS = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "BathroomsFull",
    "BathroomsHalf",
    "DaysOnMarket",
    "YearBuilt",
    "Latitude",
    "Longitude",
    "rate_30yr_fixed"
]

CORE_FIELDS_TO_KEEP_EVEN_IF_MISSING = [
    "ListingKey",
    "ListingId",
    "PropertyType",
    "PropertySubType",
    "StandardStatus",
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "CountyOrParish",
    "City",
    "PostalCode",
    "Latitude",
    "Longitude",
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate",
    "year_month",
    "rate_30yr_fixed"
]

UNNECESSARY_COLUMNS = [
    "Media",
    "MediaURL",
    "Photos",
    "PhotosChangeTimestamp",
    "PhotosCount",
    "VirtualTourURLUnbranded",
    "VirtualTourURLBranded",
    "OriginatingSystemID",
    "OriginatingSystemKey",
    "OriginatingSystemName",
    "SourceSystemID",
    "SourceSystemKey",
    "SourceSystemName",
    "ModificationTimestamp",
    "MajorChangeTimestamp",
    "StatusChangeTimestamp",
    "MlsStatus",
    "InternetAddressDisplayYN",
    "InternetEntireListingDisplayYN",
    "PublicRemarks",
    "PrivateRemarks",
    "SyndicationRemarks",
    "ShowingInstructions",
    "Directions",
    "Disclaimer"
]

MIN_CA_LATITUDE = 32.0
MAX_CA_LATITUDE = 42.5
MIN_CA_LONGITUDE = -125.0
MAX_CA_LONGITUDE = -113.0


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def load_dataset(file_path: str, dataset_name: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"{dataset_name} input file was not found: {file_path}"
        )

    df = pd.read_csv(file_path, low_memory=False)

    print(f"{dataset_name} loaded:")
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    return df


def convert_date_fields(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    print_header(f"{dataset_name}: CONVERT DATE FIELDS")

    for col in DATE_FIELDS:
        if col in df.columns:
            before_missing = df[col].isna().sum()

            df[col] = pd.to_datetime(df[col], errors="coerce")

            after_missing = df[col].isna().sum()
            newly_coerced = after_missing - before_missing

            print(f"{col}: converted to datetime")
            print(f"  Missing before conversion: {before_missing:,}")
            print(f"  Missing after conversion:  {after_missing:,}")
            print(f"  Newly coerced to NaT:      {newly_coerced:,}")
        else:
            print(f"{col}: column not found, skipped")

    return df


def convert_numeric_fields(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    print_header(f"{dataset_name}: CONVERT NUMERIC FIELDS")

    for col in NUMERIC_FIELDS:
        if col in df.columns:
            before_missing = df[col].isna().sum()

            df[col] = pd.to_numeric(df[col], errors="coerce")

            after_missing = df[col].isna().sum()
            newly_coerced = after_missing - before_missing

            print(f"{col}: converted to numeric")
            print(f"  Missing before conversion: {before_missing:,}")
            print(f"  Missing after conversion:  {after_missing:,}")
            print(f"  Newly coerced to NaN:      {newly_coerced:,}")
        else:
            print(f"{col}: column not found, skipped")

    return df


def remove_unnecessary_columns(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    print_header(f"{dataset_name}: REMOVE UNNECESSARY COLUMNS")

    before_cols = df.shape[1]

    columns_to_drop = [
        col for col in UNNECESSARY_COLUMNS
        if col in df.columns and col not in CORE_FIELDS_TO_KEEP_EVEN_IF_MISSING
    ]

    df = df.drop(columns=columns_to_drop, errors="ignore")

    after_cols = df.shape[1]

    print(f"Columns before dropping: {before_cols:,}")
    print(f"Columns after dropping:  {after_cols:,}")
    print(f"Columns dropped:         {len(columns_to_drop):,}")

    if columns_to_drop:
        print("\nDropped columns:")
        for col in columns_to_drop:
            print(f"- {col}")
    else:
        print("No configured unnecessary columns were found.")

    return df


def handle_missing_values(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    print_header(f"{dataset_name}: MISSING VALUE HANDLING")

    before_rows = df.shape[0]

    missing_summary = pd.DataFrame({
        "Column": df.columns,
        "MissingCount": df.isna().sum().values,
        "MissingPercent": (df.isna().sum().values / len(df) * 100).round(2)
    }).sort_values("MissingPercent", ascending=False)

    missing_output_file = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_missing_value_summary.csv"
    )

    missing_summary.to_csv(missing_output_file, index=False)

    print(f"Missing value summary saved to: {missing_output_file}")
    print("\nTop 20 columns by missing percentage:")
    print(missing_summary.head(20).to_string(index=False))

    high_missing_cols = missing_summary[
        missing_summary["MissingPercent"] > 90
    ]["Column"].tolist()

    high_missing_non_core = [
        col for col in high_missing_cols
        if col not in CORE_FIELDS_TO_KEEP_EVEN_IF_MISSING
    ]

    if high_missing_non_core:
        df = df.drop(columns=high_missing_non_core, errors="ignore")

    print("\nColumns with more than 90% missing:")
    print(high_missing_cols)

    print("\nDropped high-missing non-core columns:")
    print(high_missing_non_core)

    after_rows = df.shape[0]

    print(f"\nRows before missing-value handling: {before_rows:,}")
    print(f"Rows after missing-value handling:  {after_rows:,}")
    print("Rows were not dropped for missing values unless explicitly flagged later.")

    return df


def create_invalid_numeric_flags(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    print_header(f"{dataset_name}: INVALID NUMERIC VALUE FLAGS")

    if "ClosePrice" in df.columns:
        df["invalid_close_price_flag"] = (
            df["ClosePrice"].notna() &
            (df["ClosePrice"] <= 0)
        )
    else:
        df["invalid_close_price_flag"] = False

    if "LivingArea" in df.columns:
        df["invalid_living_area_flag"] = (
            df["LivingArea"].notna() &
            (df["LivingArea"] <= 0)
        )
    else:
        df["invalid_living_area_flag"] = False

    if "DaysOnMarket" in df.columns:
        df["invalid_days_on_market_flag"] = (
            df["DaysOnMarket"].notna() &
            (df["DaysOnMarket"] < 0)
        )
    else:
        df["invalid_days_on_market_flag"] = False

    if "BedroomsTotal" in df.columns:
        df["invalid_bedrooms_flag"] = (
            df["BedroomsTotal"].notna() &
            (df["BedroomsTotal"] < 0)
        )
    else:
        df["invalid_bedrooms_flag"] = False

    bathroom_cols = [
        col for col in [
            "BathroomsTotalInteger",
            "BathroomsFull",
            "BathroomsHalf"
        ]
        if col in df.columns
    ]

    if bathroom_cols:
        df["invalid_bathrooms_flag"] = False

        for col in bathroom_cols:
            df["invalid_bathrooms_flag"] = (
                df["invalid_bathrooms_flag"] |
                (
                    df[col].notna() &
                    (df[col] < 0)
                )
            )
    else:
        df["invalid_bathrooms_flag"] = False

    numeric_flag_cols = [
        "invalid_close_price_flag",
        "invalid_living_area_flag",
        "invalid_days_on_market_flag",
        "invalid_bedrooms_flag",
        "invalid_bathrooms_flag"
    ]

    df["any_invalid_numeric_flag"] = df[numeric_flag_cols].any(axis=1)

    print("Invalid numeric flag counts:")
    for col in numeric_flag_cols + ["any_invalid_numeric_flag"]:
        print(f"{col}: {df[col].sum():,}")

    invalid_numeric_records = df[df["any_invalid_numeric_flag"]].copy()

    invalid_numeric_output = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_invalid_numeric_records.csv"
    )

    invalid_numeric_records.to_csv(invalid_numeric_output, index=False)

    print(f"\nInvalid numeric records saved to: {invalid_numeric_output}")

    return df


def create_date_consistency_flags(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    print_header(f"{dataset_name}: DATE CONSISTENCY FLAGS")

    if "ListingContractDate" in df.columns and "CloseDate" in df.columns:
        df["listing_after_close_flag"] = (
            df["ListingContractDate"].notna() &
            df["CloseDate"].notna() &
            (df["ListingContractDate"] > df["CloseDate"])
        )
    else:
        df["listing_after_close_flag"] = False

    if "PurchaseContractDate" in df.columns and "CloseDate" in df.columns:
        df["purchase_after_close_flag"] = (
            df["PurchaseContractDate"].notna() &
            df["CloseDate"].notna() &
            (df["PurchaseContractDate"] > df["CloseDate"])
        )
    else:
        df["purchase_after_close_flag"] = False

    if (
        "ListingContractDate" in df.columns and
        "PurchaseContractDate" in df.columns and
        "CloseDate" in df.columns
    ):
        df["negative_timeline_flag"] = (
            df["ListingContractDate"].notna() &
            df["PurchaseContractDate"].notna() &
            df["CloseDate"].notna() &
            (
                (df["ListingContractDate"] > df["PurchaseContractDate"]) |
                (df["PurchaseContractDate"] > df["CloseDate"]) |
                (df["ListingContractDate"] > df["CloseDate"])
            )
        )
    else:
        df["negative_timeline_flag"] = False

    date_flag_cols = [
        "listing_after_close_flag",
        "purchase_after_close_flag",
        "negative_timeline_flag"
    ]

    print("Date consistency flag counts:")
    for col in date_flag_cols:
        print(f"{col}: {df[col].sum():,}")

    date_issue_records = df[df[date_flag_cols].any(axis=1)].copy()

    date_issues_output = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_date_consistency_issues.csv"
    )

    date_issue_records.to_csv(date_issues_output, index=False)

    print(f"\nDate consistency issue records saved to: {date_issues_output}")

    return df


def create_geographic_flags(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    print_header(f"{dataset_name}: GEOGRAPHIC DATA QUALITY FLAGS")

    if "Latitude" not in df.columns or "Longitude" not in df.columns:
        df["missing_coordinates_flag"] = False
        df["zero_coordinates_flag"] = False
        df["positive_longitude_flag"] = False
        df["implausible_coordinates_flag"] = False
        df["any_geo_issue_flag"] = False

        print("Latitude and/or Longitude columns not found. Geo checks skipped.")
        return df

    df["missing_coordinates_flag"] = (
        df["Latitude"].isna() |
        df["Longitude"].isna()
    )

    df["zero_coordinates_flag"] = (
        (df["Latitude"] == 0) |
        (df["Longitude"] == 0)
    )

    df["positive_longitude_flag"] = (
        df["Longitude"].notna() &
        (df["Longitude"] > 0)
    )

    df["implausible_coordinates_flag"] = (
        df["Latitude"].notna() &
        df["Longitude"].notna() &
        (
            (df["Latitude"] < MIN_CA_LATITUDE) |
            (df["Latitude"] > MAX_CA_LATITUDE) |
            (df["Longitude"] < MIN_CA_LONGITUDE) |
            (df["Longitude"] > MAX_CA_LONGITUDE)
        )
    )

    geo_flag_cols = [
        "missing_coordinates_flag",
        "zero_coordinates_flag",
        "positive_longitude_flag",
        "implausible_coordinates_flag"
    ]

    df["any_geo_issue_flag"] = df[geo_flag_cols].any(axis=1)

    print("Geographic flag counts:")
    for col in geo_flag_cols + ["any_geo_issue_flag"]:
        print(f"{col}: {df[col].sum():,}")

    geo_issue_records = df[df["any_geo_issue_flag"]].copy()

    geo_issues_output = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_geographic_quality_issues.csv"
    )

    geo_issue_records.to_csv(geo_issues_output, index=False)

    print(f"\nGeographic issue records saved to: {geo_issues_output}")

    geo_summary = pd.DataFrame({
        "Issue": geo_flag_cols + ["any_geo_issue_flag"],
        "Count": [int(df[col].sum()) for col in geo_flag_cols + ["any_geo_issue_flag"]],
        "PercentOfRows": [
            round(df[col].mean() * 100, 2)
            for col in geo_flag_cols + ["any_geo_issue_flag"]
        ]
    })

    geo_summary_output = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_geographic_quality_summary.csv"
    )

    geo_summary.to_csv(geo_summary_output, index=False)

    print(f"Geographic quality summary saved to: {geo_summary_output}")

    return df


def save_dtype_confirmation(
    df: pd.DataFrame,
    dataset_name: str
) -> None:
    print_header(f"{dataset_name}: DATA TYPE CONFIRMATION")

    dtype_summary = pd.DataFrame({
        "Column": df.columns,
        "Dtype": df.dtypes.astype(str).values
    })

    dtype_output = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_dtype_confirmation.csv"
    )

    dtype_summary.to_csv(dtype_output, index=False)

    print(dtype_summary.to_string(index=False))
    print(f"\nDtype confirmation saved to: {dtype_output}")


def save_flag_summary(
    df: pd.DataFrame,
    dataset_name: str
) -> None:
    print_header(f"{dataset_name}: FLAG SUMMARY")

    flag_cols = [col for col in df.columns if col.endswith("_flag")]

    summary_rows = []

    for col in flag_cols:
        summary_rows.append({
            "FlagColumn": col,
            "FlaggedCount": int(df[col].sum()),
            "FlaggedPercent": round(df[col].mean() * 100, 2)
        })

    flag_summary = pd.DataFrame(summary_rows).sort_values(
        "FlaggedCount",
        ascending=False
    )

    flag_summary_output = os.path.join(
        OUTPUT_DIR,
        f"{dataset_name.lower()}_flag_summary.csv"
    )

    flag_summary.to_csv(flag_summary_output, index=False)

    print(flag_summary.to_string(index=False))
    print(f"\nFlag summary saved to: {flag_summary_output}")


def clean_dataset(
    df: pd.DataFrame,
    dataset_name: str
) -> pd.DataFrame:
    print_header(f"START CLEANING: {dataset_name}")

    starting_rows = df.shape[0]
    starting_cols = df.shape[1]

    df = convert_date_fields(df, dataset_name)
    df = convert_numeric_fields(df, dataset_name)
    df = remove_unnecessary_columns(df, dataset_name)
    df = handle_missing_values(df, dataset_name)
    df = create_invalid_numeric_flags(df, dataset_name)
    df = create_date_consistency_flags(df, dataset_name)
    df = create_geographic_flags(df, dataset_name)

    save_dtype_confirmation(df, dataset_name)
    save_flag_summary(df, dataset_name)

    ending_rows = df.shape[0]
    ending_cols = df.shape[1]

    print_header(f"FINISHED CLEANING: {dataset_name}")

    print(f"Rows before cleaning:    {starting_rows:,}")
    print(f"Rows after cleaning:     {ending_rows:,}")
    print(f"Columns before cleaning: {starting_cols:,}")
    print(f"Columns after cleaning:  {ending_cols:,}")

    return df

print_header("LOAD INPUT DATASETS")

sold = load_dataset(SOLD_INPUT_FILE, "Sold")
listings = load_dataset(LISTINGS_INPUT_FILE, "Listings")


print_header("CLEAN SOLD DATASET")

cleaned_sold = clean_dataset(sold, "Sold")


print_header("CLEAN LISTINGS DATASET")

cleaned_listings = clean_dataset(listings, "Listings")


print_header("SAVE CLEANED DATASETS")

cleaned_sold.to_csv(SOLD_OUTPUT_FILE, index=False)
cleaned_listings.to_csv(LISTINGS_OUTPUT_FILE, index=False)

print(f"Cleaned sold dataset saved to: {SOLD_OUTPUT_FILE}")
print(f"Cleaned listings dataset saved to: {LISTINGS_OUTPUT_FILE}")


print_header("FINAL DELIVERABLE SUMMARY")

print("Weeks 4–5 deliverables created:")
print(f"1. Cleaned sold CSV: {SOLD_OUTPUT_FILE}")
print(f"2. Cleaned listings CSV: {LISTINGS_OUTPUT_FILE}")
print(f"3. Output folder with summaries: {OUTPUT_DIR}")

print("\nMain summary files created inside the output folder:")
print("- sold_missing_value_summary.csv")
print("- listings_missing_value_summary.csv")
print("- sold_dtype_confirmation.csv")
print("- listings_dtype_confirmation.csv")
print("- sold_flag_summary.csv")
print("- listings_flag_summary.csv")
print("- sold_geographic_quality_summary.csv")
print("- listings_geographic_quality_summary.csv")
print("- sold_invalid_numeric_records.csv")
print("- listings_invalid_numeric_records.csv")
print("- sold_date_consistency_issues.csv")
print("- listings_date_consistency_issues.csv")
print("- sold_geographic_quality_issues.csv")
print("- listings_geographic_quality_issues.csv")