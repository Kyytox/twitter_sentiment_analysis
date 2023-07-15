import pandas as pd
import datetime
from pathlib import Path


# Utils.
from helpers.aws_utils import check_file_aws
from helpers.aws_utils import send_to_aws

PLUGINS_DIR = Path(__file__).parent.parent


# Update history_tech after create bronze
def update_history_tech(df_old_history, df_bronze, timestamp):
    # # create DataFrame
    df_new_history = pd.DataFrame()

    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for user in df_bronze['id_user'].unique():

        # get last id_tweet
        last_id_tweet = str(df_bronze[df_bronze['id_user'] == user]['id_tweet'].max())

        # get last date_tweet
        date_tweet = df_bronze[df_bronze['id_user']== user]['date_tweet'].max()

        # get name_user
        name_user = df_bronze[df_bronze['id_user'] == user]['name_user'].max()

        # insert in DataFrame
        new_row = {'date_last_update': today,
                'timestamp_last_update': timestamp,
                'id_user': user,
                'name_user': name_user,
                'last_id_tweet': last_id_tweet,
                'date_tweet': date_tweet}
        

        df_new_history = pd.concat([df_new_history, pd.DataFrame(new_row, index=[0])],ignore_index=True)

    # concat old and new DataFrame
    df_new_history = pd.concat([df_old_history, df_new_history], ignore_index=True).reset_index(drop=True)
    df_new_history['id_user'] = df_new_history['id_user'].astype(int)
    df_new_history['last_id_tweet'] = df_new_history['last_id_tweet'].astype(int)
    df_new_history['timestamp_last_update'] = df_new_history['timestamp_last_update'].astype(int)

    # Send df to AWS S3
    send_to_aws(df_new_history, "data_history.parquet")



# create parquet history_tech if not exists
def create_history_tech():

    if check_file_aws("data_history.parquet") == False:
        
        # extract history Excel file
        file_path = "ressources/data/data_history.xlsx"
        df = pd.read_excel(file_path, engine="openpyxl")

        # Send to AWS S3
        send_to_aws(df, "data_history.parquet")
