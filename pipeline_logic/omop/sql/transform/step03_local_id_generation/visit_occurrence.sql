CREATE TABLE `/UNITE/Data Ingestion & OMOP Mapping/Source Data Model: OMOP/Site 25/transform/03 - local id generation/visit_occurrence` AS
    
    SELECT 
          * 
        , cast(conv(substr(hashed_id, 1, 15), 16, 10) as bigint) & 2251799813685247 as visit_occurrence_id_51_bit
    FROM (
        SELECT
              visit_occurrence_id as site_visit_occurrence_id
            , md5(CAST(visit_occurrence_id as string)) as hashed_id
            , person_id as site_person_id
            , visit_concept_id
            , visit_start_date
            , visit_start_datetime
            , visit_end_date
            , visit_end_datetime
            , visit_type_concept_id
            , provider_id as site_provider_id
            , care_site_id as site_care_site_id
            , visit_source_value
            , visit_source_concept_id
            , admitting_source_concept_id
            , admitting_source_value
            , discharge_to_concept_id
            , discharge_to_source_value
            , preceding_visit_occurrence_id
            , data_partner_id
            , payload
        FROM `/UNITE/Data Ingestion & OMOP Mapping/Source Data Model: OMOP/Site 25/transform/02 - clean/visit_occurrence`
        WHERE visit_occurrence_id IS NOT NULL
    )   
