import boto3

# Cloudflare R2 credentials
r2_access_key_id = 'ACCESS-KEY'
r2_secret_access_key = 'SECRET'
import boto3

# Initialize a boto3 client for Cloudflare R2
s3 = boto3.client(
    's3',
    endpoint_url='https://XYZ.r2.cloudflarestorage.com',
    aws_access_key_id=r2_access_key_id,
    aws_secret_access_key=r2_secret_access_key,
    region_name='auto'
)

# Specify your R2 bucket name
bucket_name = 'BUCKET_NAME'

def move_files(src_prefix, dest_prefix):
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=src_prefix)

    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                src_key = obj['Key']
                dest_key = src_key.replace(src_prefix, dest_prefix, 1)

                # Copy the object to the new location
                s3.copy_object(
                    Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': src_key},
                    Key=dest_key
                )

                # Delete the original object
                s3.delete_object(Bucket=bucket_name, Key=src_key)

                print(f'Moved {src_key} to {dest_key}')

if __name__ == '__main__':
    src_path = 'old-path/'
    dest_path = 'new-path/'
    move_files(src_path, dest_path)
