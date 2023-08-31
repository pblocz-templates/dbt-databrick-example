from pyspark.sql.dataframe import DataFrame
import pyspark.sql.functions as F


def model(dbt, session):
    dbt.config(
        submission_method="all_purpose_cluster",
        create_notebook=True,
        unique_key="provider_id",
        materialized="incremental",
        incremental_strategy='merge',
        # post_hook=[
        #         f"OPTIMIZE { dbt.this } ZORDER BY currency_id;",
        #         f"ANALYZE TABLE { dbt.this } COMPUTE STATISTICS FOR ALL COLUMNS;"
        # ]
    )

    source_df = dbt.source('silver_layer', 'transaction_silver')

    if dbt.is_incremental:
        previous_load_time = session.table(str(dbt.this)).select(F.max("load_time")).collect()[0][0]
        source_df = source_df.filter(F.col("loadTime") > previous_load_time)

    items_silver: DataFrame = (
        source_df
        .groupBy("transactionProvider")
        .agg(F.max("loadTime").alias("load_time"))
        .select(F.md5("transactionProvider").alias("provider_id"),
                F.col("transactionProvider").alias("provider"),
                F.col("load_time")
        )
    )

    return items_silver
