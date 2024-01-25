import boto3

# Cloudflare R2 credentials
r2_access_key_id = 'ACCESS-KEY'
r2_secret_access_key = 'SECRET'

# Initialize a boto3 client for Cloudflare R2 with custom endpoint
s3 = boto3.client(
    's3',
    endpoint_url='https://XYZ.r2.cloudflarestorage.com',  # Replace with your R2 endpoint
    aws_access_key_id=r2_access_key_id,
    aws_secret_access_key=r2_secret_access_key,
    region_name='auto'  # R2 doesn't require a specific region, but 'auto' or a placeholder can be used
)

# Specify your R2 bucket name
bucket_name = 'BUCKET_NAME'

def is_xml_compliant(char):
    """Check if a character is XML 1.0 compliant."""
    code = ord(char)
    # XML 1.0 compliant characters are:
    # Tab (9), Line Feed (10), Carriage Return (13), and valid printable characters (32-126 and 128-255)
    return code == 9 or code == 10 or code == 13 or 32 <= code <= 126 or 128 <= code <= 255

def contains_non_xml_compliant_chars(string):
    """Check if a string contains any non-XML compliant characters."""
    return not all(is_xml_compliant(char) for char in string)

def main():
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name)

    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if contains_non_xml_compliant_chars(key):
                    print(f'Non-XML compliant file name found: {key}')

if __name__ == '__main__':
    main()
