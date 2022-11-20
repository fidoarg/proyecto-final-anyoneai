
#Import de libraries
import boto3
import os

# Keys AWS
AWS_ACCESS_KEY_ID = 'AKIA2JHUK4EGCLO2FNS4'
AWS_SECRET_ACCESS_KEY = '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'

#Create the service for AWS
s3_resource = boto3.resource('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# create the resource point in the Anyone bucket
bucket = s3_resource.Bucket('anyoneai-datasets')

#Download the files
for object_summary in bucket.objects.filter(Prefix="credit-data-2010/"):
    try:
        with open(os.path.join(
                '..','data', os.path.split(object_summary.key)[-1]
                  ), 'wb') as data:
            bucket.download_fileobj(object_summary.key, data)
    except IsADirectoryError:
        continue