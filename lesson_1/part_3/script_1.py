import great_expectations as gx

# 1. Configuration Constants
PROJECT_ID = "project-f9d57285-2f9c-4d90-b25"
DATASET_ID = "chicago_taxi"
TABLE_NAME = "gold_table"
CONNECTION_STRING = f"bigquery://{PROJECT_ID}/{DATASET_ID}"

# 2. Initialize a Persistent Context
# Using FileDataContext ensures your "gx" folder is created in your notebook
# which makes finding the HTML Data Docs much easier.
context = gx.get_context()

# 3. Add the BigQuery Datasource
datasource_name = "bq_taxi_datasource"

datasource = context.data_sources.add_sql(
    name=datasource_name, 
    connection_string=CONNECTION_STRING
)

# 4. Add the Table Asset
# We nickname the asset 'gold_taxi_data'
asset_name = "gold_taxi_data"
try:
    table_asset = datasource.add_table_asset(name=asset_name, table_name=TABLE_NAME)
except Exception:
    table_asset = datasource.get_asset(asset_name)

# 5. Create the Suite and Validator
suite_name = "taxi_gold_suite"
try:
    # Try to add it fresh
    suite = context.suites.get(name=suite_name)
    
except Exception:
    # If it already exists, just retrieve the existing one
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

validator = context.get_validator(
    batch_request=table_asset.build_batch_request(),
    expectation_suite_name=suite_name
)

# 6. Define the 8 Expectations (Modern 1.x Syntax)
# Null Checks
validator.expect_column_values_to_not_be_null("label_high_tip")
validator.expect_column_values_to_not_be_null("company")

# Range/Value Checks
validator.expect_column_values_to_be_between("avg_speed_mph", min_value=0, max_value=120)
validator.expect_column_values_to_be_between("pickup_hour", min_value=0, max_value=23)

# Uniqueness
validator.expect_column_values_to_be_unique("unique_key")

# Set Membership
validator.expect_column_values_to_be_in_set("split", value_set=["train", "test"])

# Distributional/Statistical
validator.expect_column_mean_to_be_between("label_high_tip", min_value=0.01, max_value=0.50)
# In GX 1.x, use expect_column_values_to_be_between with no max_value
validator.expect_column_values_to_be_between("trip_miles", min_value=0, strict_min=True)

validation_result = validator.validate()