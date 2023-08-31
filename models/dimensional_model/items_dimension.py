from pyspark.sql.dataframe import DataFrame
import pyspark.sql.functions as F


def model(dbt, session):
    dbt.config(
        submission_method="all_purpose_cluster",
        create_notebook=True,
        # cluster_id="abcd-1234-wxyz"
        unique_key="item_id",
    )

    items_silver: DataFrame = (
        dbt.source('silver_layer', 'item_silver')
        .select(F.col("itemId").alias("item_id"), "brand", "name")
    )

    return items_silver
