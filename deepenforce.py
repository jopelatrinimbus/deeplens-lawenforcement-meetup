#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import boto3

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-s',
            '--video-stream-arn',
            help='ARN of the Deeplens Kinesis Video Stream. You can get it'\
                    ' from the kinesis console'\
                    ' (https://console.aws.amazon.com/kinesisvideo/streams)',
            required = True)

    parser.add_argument(
            '-d',
            '--data-stream-arn',
            help='ARN of the Kinesis Data stream used for pushing rekognition'\
                    ' results',
            required=True)

    parser.add_argument(
            '-r',
            '--role-arn',
            help='ARN of the role giving rekognition access to '



    parser.add_argument(
            '-p',
            '--picture-file',
            help='path to the file containing picture of wanted subject',
            required=True)

    parser.add_argument(
            '-b',
            '--bucket-name',
            help='name of the bucket used to upload wanted subject image'
            required=True)


    args = parser.parse_args()

    # upload the suspect image to s3
    s3 = boto3.client('s3')

    file_key = args.picture_file.split('/')[0]

    with open(args.picture_file, 'rb') as data:
        s3.upload_fileobj(data, args.bucket, file_key)

    # create a collection from the suspect image
    rekognition = boto3.client('rekognition')

    collection_id = file_key

    rekognition.delete_collection(CollectionId=collection_id)
    collection = rekognition.create_collection(CollectionId=collection_id)

    # index the face
    face_records = rekognition.index_faces(
            CollectionId=collection_id,
            Image={ 'S3Object': { 'Bucket': args.bucket, 'Name':file_key } },
            ExternalImageId=file_key,
            DetectionAttributes=['ALL'])

    # create a Stream processor for the faces
    rekognition.

