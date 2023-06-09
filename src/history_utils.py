import pandas as pd
import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aws.aws_utils import get_file_aws
from aws.aws_utils import send_to_aws

def update_history_tech(df_old_history_tech, df_bronze, timestamp):
    # # create DataFrame
    df_new_history_tech = pd.DataFrame()

    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for user in df_bronze['id_user'].unique():

        # get last id_tweet
        last_id_tweet = str(
            df_bronze[df_bronze['id_user'] == user]['id_tweet'].max())

        # get last date_tweet
        date_tweet = df_bronze[df_bronze['id_user']
                            == user]['date_tweet'].max().strftime("%Y-%m-%d %H:%M:%S")

        # get name_user
        name_user = df_bronze[df_bronze['id_user'] == user]['name_user'].max()

        # insert in DataFrame
        new_row = {'date_last_update': today,
                'timestamp_last_update': timestamp,
                'id_user': user,
                'name_user': name_user,
                'last_id_tweet': last_id_tweet,
                'date_tweet': date_tweet}
        df_new_history_tech = pd.concat([df_new_history_tech, pd.DataFrame(new_row, index=[0])],
                                        ignore_index=True)

    # concat old and new DataFrame
    df_new_history_tech = pd.concat(
        [df_old_history_tech, df_new_history_tech], ignore_index=True).reset_index(drop=True)

    # save DataFrame in one parquet file
    df_new_history_tech.to_parquet("./data/df_history_tech.parquet",
                                engine="pyarrow", compression="snappy")

    return df_new_history_tech





# create parquet history_tech if not exists
def create_history_tech_parquet():
    try :
        # get df_history_tech from AWS S3
        df_history_tech = get_file_aws("history_tech.parquet")
    except:
        # extract history Excel file
        df = pd.read_excel("./data_history_tech.xlsx" , engine="openpyxl")

        # Send to AWS S3
        send_to_aws(df, "history_tech.parquet")


create_history_tech_parquet()