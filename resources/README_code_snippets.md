# Code Snippets
Collection of code snippets, development hacks, useful tips and tricks

# Contents

* [Python](#python)
	* [AWS S3](#aws-s3)
		* [Init S3 Client](#init-s3-client)
		* [Get parquet file](#get-parquet-file)
		* [Send file to S3 ](#send-file-to-s3 )
		* [Send Partitionned Parquet file to S3](#send-partitionned-parquet-file-to-s3)
	* [Databricks](#databricks)
		* [Secrets Scope](#secrets-scope)
		* [Get parquet file from AWS S3](#get-parquet-file-from-aws-s3)

***
# Python 
&nbsp;


## AWS S3 
### Init S3 Client 
```python 
import boto3

s3 = boto3.client('s3', aws_access_key_id="AWS_ACCESS_KEY",
				  aws_secret_access_key="AWS_SECRET_KEY",
				  region_name="AWS_REGION")
```
&nbsp;

### Get parquet file 
```python
import pandas as pd

# get parquet from S3
parquet_object = s3.get_object(Bucket="AWS_BUCKET_NAME", Key=key_file)['Body'].read()
parquet_buffer = io.BytesIO(parquet_object)

# read parquet buffer
df = pd.read_parquet(parquet_buffer)
```
&nbsp;

### Send file to S3 
```python
# upload file to S3
s3.upload_file(file_path, "AWS_BUCKET_NAME", file_name)
```
&nbsp;

### Send Partitionned Parquet file to S3 
```python
# pip install awswrangler
import awswrangler as wr

bucket = "AWS_BUCKET_NAME"
path_file = f"s3://{bucket}/xxxx/parquet_file.parquet"

wr.s3.to_parquet(df,
		 path_file,
		 partition_cols=['column_name'], 
		 dataset=True,
		 mode="append", 
		 compression='snappy')
```
***
\
&nbsp;
\
&nbsp;

## Databricks
### Secrets Scope

Create Personal Acces Token 
  1. In your Databricks workspace, click your Databricks username in the top bar, and then select **User Settings** from the drop down.
  2.  On the **Access tokens** tab, click **Generate new token**.
  3.  (Optional) Enter a comment that helps you to identify this token in the future, and change the token’s default lifetime of 90 days. To create a token with no lifetime (not recommended),   leave the **Lifetime (days)** box empty (blank).
  4.  Click **Generate**.    
  5.  Copy the displayed token, and then click **Done**.
\
&nbsp;

Install Databricks CLI 
```bash 
pip install databricks-cli
```

configure Databricks CLI 
```bash 
databricks configure --token
```

in console fill
```console 
Databricks Host (should begin with https://): <workspace URL>

Token: <Personal Acces Token>
```

Create Secrets Scope 
```bash 
databricks secrets create-scope --scope <scope-name>
```

Create Secrets in Scope
```bash 
databricks secrets put --scope <scope-name> --key <key> --string-value <value> 
```

List Secrets 
```bash 
databricks secrets list --scope <scope-name>
```

Read Secrets in Notebooks 
```python 
AWS_ACCESS_KEY_ID = dbutils.secrets.get(scope = <scope-name>, key = <key>)
AWS_SECRET_ACCESS_KEY = dbutils.secrets.get(scope = <scope-name>, key = <key>)
```

&nbsp;
\
&nbsp;


### Get parquet file from AWS S3 
Create a Notebook 

```python 
import boto3
import io
import pandas as pd
```

Get secrets, for AWS credentials
```python 
# get Secrets in secrets scope
AWS_ACCESS_KEY_ID = dbutils.secrets.get(scope = "name_scope", key = "ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = dbutils.secrets.get(scope = "name_scope", key = "SECRET_KEY")
```

Init Bucket parameter and client S3 
```python
# Bucket infos 
AWS_BUCKET_NAME = 'bucket_name'
AWS_REGION = 'region'
KEY_FILE = 'parquet_file.parquet'

# init session S3 
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
		region_name=AWS_REGION)
```

Get parquet file 
```python
# get parquet file from S3
parquet_object = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=KEY_FILE)['Body'].read()
parquet_buffer = io.BytesIO(parquet_object)

# Read parquet buffer 
df = pd.read_parquet(parquet_buffer)
```

