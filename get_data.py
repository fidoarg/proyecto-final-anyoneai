import boto3
import os


#Dataset: s3://anyoneai-datasets/credit-data-2010/
#Key: AKIA2JHUK4EGCLO2FNS4
#Secret: 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
# fetch credentials from env variables
#aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_access_key_id = "AKIA2JHUK4EGCLO2FNS4"
#aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_secret_access_key = "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"

# setup a AWS S3 client/resource
s3 = boto3.resource(
    's3', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )

print(s3)
# point the resource at the existing bucket
bucket = s3.Bucket(name='anyoneai-datasets')

print(bucket.objects.all())
bucket = s3.Bucket(name='anyoneai-datasets')

for object_summary in bucket.objects.filter(Prefix="credit-data-2010/"):
    print(object_summary.key)
    
    #bucket.download_file(objs[i].key, objs[i].key)

# creating data folder
if not os.path.exists('data'):
    os.makedirs('data')

for object_summary in bucket.objects.filter(Prefix="credit-data-2010/"):
    try:
        with open(os.path.join(
                './data', os.path.split(object_summary.key)[-1]
                  ), 'wb') as data:
            bucket.download_fileobj(object_summary.key, data)
    except IsADirectoryError:
        continue



    
# download the dataset labels
#with open('data/car_dataset_labels.csv', 'wb') as data:
#    bucket.download_fileobj('training-datasets/car_dataset_labels.csv', data)

# upload a file
# with open('sample.png', 'rb') as data:
#     bucket.upload_fileobj(data, 'raf/sample.png')