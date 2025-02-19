from pyspark.sql import types as T
from pyspark.sql.functions import col, when
from transforms.api import transform, Input, Output, Check
from transforms import expectations as E
from trinetx.utils import blanks_as_nulls
from trinetx.trinetx_schemas import complete_domain_schema_dict_string_type, schema_dict_all_string_type

domain = "medication"
required_schema = complete_domain_schema_dict_string_type[domain]
required_schema_lowercase = schema_dict_all_string_type(required_schema, all_lowercase=True)
required_schema_uppercase = schema_dict_all_string_type(required_schema)
schema_expectation = E.any(
    E.schema().contains(required_schema_lowercase),
    E.schema().contains(required_schema_uppercase)
)


@transform(
    processed=Output('/UNITE/Data Ingestion & OMOP Mapping/Source Data Model: TriNetX/raw_trinetx/Site 77/transform/02 - clean/medication'),
    my_input=Input(
        '/UNITE/Data Ingestion & OMOP Mapping/Source Data Model: TriNetX/raw_trinetx/Site 77/transform/01 - parsed/medication',
        checks=[
            # Check(E.count().gt(0), 'Required TriNetX table is not empty', on_error='FAIL'),
            Check(schema_expectation, 'Dataset from site includes all expected columns', on_error='WARN')
        ]
    ),
)
def compute_function(my_input, processed):
    processed_df = my_input.dataframe()

    # Replace empty strings with nulls
    processed_df = blanks_as_nulls(processed_df)

    # Drop "orphan" columns referring to patients not in the Patient table
    processed_df = processed_df.filter(col("ORPHAN_FLAG") != "t")

    # Cast non-string columns to proper type
    processed_df = (
        processed_df
        .withColumn("START_DATE", processed_df["START_DATE"].cast(T.DateType()))
        .withColumn(
            "UNITS_PER_ADMINISTRATION",
            processed_df["UNITS_PER_ADMINISTRATION"].cast(T.DoubleType()),
        )
        .withColumn("DURATION", processed_df["DURATION"].cast(T.DoubleType()))
        .withColumn("REFILLS", processed_df["REFILLS"].cast(T.DoubleType()))
        .withColumn("END_DATE", processed_df["END_DATE"].cast(T.TimestampType()))
        .withColumn("QTY_DISPENSED", processed_df["QTY_DISPENSED"].cast(T.DoubleType()))
        .withColumn("DOSE_AMOUNT", processed_df["DOSE_AMOUNT"].cast(T.DoubleType()))
        .withColumn("ORPHAN_FLAG", when(col("ORPHAN_FLAG") == 'f', False).cast(T.BooleanType()))
    )

    processed.write_dataframe(processed_df)
