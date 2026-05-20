import great_expectations as gx
import great_expectations.expectations as gxe

# 1. Configuration Constants
PROJECT_ID = "project-f9d57285-2f9c-4d90-b25"
DATASET_ID = "chicago_taxi"
TABLE_NAME = "gold_table"
CONNECTION_STRING = f"bigquery://{PROJECT_ID}/{DATASET_ID}"

# 2. Initialize a Persistent Context
context = gx.get_context()

# 3. Add the BigQuery Datasource
datasource_name = "bq_taxi_datasource"

datasource = context.data_sources.add_sql(
    name=datasource_name,
    connection_string=CONNECTION_STRING
)

# =====================================================================
# 4. Add the Table Asset & Create a Batch Definition
# =====================================================================
asset_name = "gold_taxi_data"
try:
    table_asset = datasource.get_asset(asset_name)
except Exception:
    table_asset = datasource.add_table_asset(name=asset_name, table_name=TABLE_NAME)

# In 1.x, you must define a Batch Definition to point to your data targets
batch_def_name = "gold_taxi_batch_def"
try:
    batch_definition = table_asset.get_batch_definition(batch_def_name)
except Exception:
    batch_definition = table_asset.add_batch_definition_whole_table(name=batch_def_name)


# =====================================================================
# 5. Create the Suite and Define Expectations
# =====================================================================
suite_name = "taxi_gold_suite"
try:
    suite = context.suites.get(name=suite_name)
except Exception:
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

# Add expectations cleanly directly to the suite object
suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="label_high_tip"))
suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="company"))
suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column="is_weekend", value_set=[0, 1]))
suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="pickup_hour", min_value=0, max_value=23))
suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column="unique_key"))
suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column="split", value_set=["train", "test"]))
suite.add_expectation(gxe.ExpectColumnMeanToBeBetween(column="label_high_tip", min_value=0.50, max_value=0.85))
suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column="trip_miles", min_value=0, strict_min=True))


# =====================================================================
# 6. Create a Validation Definition
# =====================================================================
validation_def_name = "taxi_gold_validation"
try:
    validation_definition = context.validation_definitions.get(validation_def_name)
except Exception:
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name=validation_def_name,
            data=batch_definition,
            suite=suite
        )
    )


# =====================================================================
# 7. Define and Run the Checkpoint
# =====================================================================
checkpoint_name = "taxi_gold_checkpoint"
try:
    checkpoint = context.checkpoints.get(name=checkpoint_name)
except Exception:
    # Pass the actual ValidationDefinition object inside a list
    checkpoint = context.checkpoints.add(
        gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=[validation_definition]
        )
    )

# Run the validation evaluation
checkpoint_result = checkpoint.run()
context.build_data_docs()
