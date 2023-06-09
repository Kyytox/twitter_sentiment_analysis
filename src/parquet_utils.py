import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


# create paquet file with partition
def create_parquet(df, file_path, file_name, partition_cols):
    # create paquet file with partition
    table = pa.Table.from_pandas(df)

    # write table to parquet file
    if partition_cols is None:
        df.to_parquet(file_path + "/" + file_name + ".parquet",
                      engine='pyarrow', compression='snappy')
    else:
        pq.write_to_dataset(table,
                            root_path=file_path,
                            partition_cols=partition_cols,
                            basename_template=file_name + "-{i}.parquet")
