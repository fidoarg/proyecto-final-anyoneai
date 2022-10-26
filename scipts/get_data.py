import os
import boto3
from zipfile import ZipFile


_AWS_S3_KEY= os.getenv('AWS_S3_KEY')
_AWS_S3_SECRET= os.getenv('AWS_S3_SECRET')

class FileNames:
    ZIP_FILES= {
        'LEADERBOARD_DATA': 'LeaderBoard_Data.zip',
        'MODELING_DATA': 'PAKDD-2010 training data.zip',
        'PREDICTION_DATA': 'Prediction_Data.zip',
        'LEADERBOARD_SUBMISSION_EXAMPLE': 'Leaderboard_Submission_Example.zip'
    }
    VARIABLES_DOC= 'PAKDD2010_VariablesList.XLS'


if _AWS_S3_KEY is None or _AWS_S3_SECRET is None:
    raise SystemError("Couldn't get variable names")

session= boto3.Session(
    aws_access_key_id=_AWS_S3_KEY,
    aws_secret_access_key=_AWS_S3_SECRET,
)
s3_bucket= session\
    .resource("s3")\
    .Bucket("anyoneai-datasets")

def main(data_dir= './data'):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    for object_summary in s3_bucket.objects.filter(Prefix="credit-data-2010/"):
        try:
            filepath= os.path.join(
                data_dir, 
                os.path.split(object_summary.key)[-1]
            )
            if filepath.endswith('.zip') or filepath.endswith('.XLS'):
                with open(filepath, 'wb') as data:
                    s3_bucket.download_fileobj(object_summary.key, data)

        except IsADirectoryError:
            continue
    

    zipfiles= FileNames().ZIP_FILES

    for zipfile_key, zipfile_name in zipfiles.items():
        print(
            f'--- Unzip {zipfile_key} process'
        )
        zipefile_path= os.path.join(
            data_dir,
            zipfile_name
        ) 
        if os.path.isfile(zipefile_path):
            with ZipFile(zipefile_path, 'r') as zip_file:
                zip_file.extractall(data_dir)
            # After unziping, remove unncessary .zip file
            os.remove(zipefile_path)

if __name__ == "__main__":
    main()