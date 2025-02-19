from transforms.api import transform, Input, Output, incremental, Check
from transforms import expectations as E
from trinetx.pkey_utils import new_duplicate_rows_with_collision_bits


@incremental(snapshot_inputs=['omop_domain'])
@transform(
    lookup_df=Output(
        "/UNITE/Data Ingestion & OMOP Mapping/Source Data Model: TriNetX/raw_trinetx/Site 77/transform/05 - pkey collision lookup tables/drug_exposure",
        checks=Check(E.col('collision_bits').lt(4), 'Fewer than 3 collisions for each 51-bit id', on_error='FAIL')
    ),
    omop_domain=Input(
        "/UNITE/Data Ingestion & OMOP Mapping/Source Data Model: TriNetX/raw_trinetx/Site 77/transform/04 - domain mapping/drug_exposure",
        checks=Check(E.primary_key('hashed_id'), 'hashed_id is unique (failue is likely due to duplicate primary keys)', on_error='FAIL')
    ),
)
def my_compute_function(omop_domain, lookup_df, ctx):

    pk_col = "drug_exposure_id_51_bit"
    full_hash_col = "hashed_id"

    new_rows = new_duplicate_rows_with_collision_bits(omop_domain, lookup_df, ctx, pk_col, full_hash_col)
    lookup_df.write_dataframe(new_rows)
