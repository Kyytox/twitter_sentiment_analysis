import pandas as pd
import datetime
import sys
from pathlib import Path


# Utils.
from helpers.aws_utils import check_file_aws
from helpers.aws_utils import send_to_aws

PATH_HISTORY_FILE = "plugins/data_history_tech.xlsx"


# Update history_tech after create bronze
def update_history_tech(df_old_history_tech, df_bronze, timestamp):
    # # create DataFrame
    df_new_history_tech = pd.DataFrame()

    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for user in df_bronze['id_user'].unique():

        # get last id_tweet
        last_id_tweet = str(df_bronze[df_bronze['id_user'] == user]['id_tweet'].max())

        # get last date_tweet
        # date_tweet = df_bronze[df_bronze['id_user']
        #                     == user]['date_tweet'].max().strftime("%Y-%m-%d %H:%M:%S")
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
        

        df_new_history_tech = pd.concat([df_new_history_tech, pd.DataFrame(new_row, index=[0])],ignore_index=True)

    # concat old and new DataFrame
    df_new_history_tech = pd.concat([df_old_history_tech, df_new_history_tech], ignore_index=True).reset_index(drop=True)
    df_new_history_tech['id_user'] = df_new_history_tech['id_user'].astype(int)
    df_new_history_tech['last_id_tweet'] = df_new_history_tech['last_id_tweet'].astype(int)
    df_new_history_tech['timestamp_last_update'] = df_new_history_tech['timestamp_last_update'].astype(int)
    print('types: ', df_new_history_tech.last_id_tweet.unique())
    print('types: ', df_new_history_tech.dtypes)

    # Send df to AWS S3
    send_to_aws(df_new_history_tech, "history_tech.parquet")



# create parquet history_tech if not exists
def create_history_tech():

    print("######################################################")
    print("check history_tech.parquet")
    
    # check if file exists
    test = check_file_aws("history_tech.parquet")
    print(test)
    if test == None:
        # extract history Excel file
        df = pd.read_excel(PATH_HISTORY_FILE, engine="openpyxl")

        # Send to AWS S3
        send_to_aws(df, "history_tech.parquet")
