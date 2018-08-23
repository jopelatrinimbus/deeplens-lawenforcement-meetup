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
            help='ARN of the role giving rekognition access to Video Stream',
            required=True)


    parser.add_argument(
            '-p',
            '--picture-file',
            help='path to the file containing picture of wanted subject',
            required=True)

    parser.add_argument(
            '-b',
            '--bucket-name',
            help='name of the bucket used to upload wanted subject image',
            required=True)

    DEFAULT_STREAM_PROCESSOR_NAME = 'deepenforcementsp'
    parser.add_argument(
            '-n',
            '--name-stream-processor',
            help='desired name of the stream processor',
            default=DEFAULT_STREAM_PROCESSOR_NAME)

    DEFAULT_THRESHOLD_FACEMATCH = 50
    parser.add_argument(
            '-t',
            '--threshold-facematch',
            help='threshold value to use for the face match (e.g: 70)',
            type=float,
            default=DEFAULT_THRESHOLD_FACEMATCH)


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
    rekognition.delete_stream_processor(Name=args.name_stream_processor)
    stream_processor = rekognition.create_stream_processor(
            Input={
                'KinesisVideoStream': {
                    'Arn': args.video_stream_arn
                    }
                },
            Output={
                'KinesisDataStream': {
                    'Arn': args.data_stream_arn
                    }
                },
            Name=args.name_stream_processor,
            Settings={
                'FaceSearch': {
                    'CollectionId':collection_id,
                    'FaceMatchThreshold':args.threshold_facematch
                    }
                },
            RoleArn=args.role_arn)

    print(stream_processor)
    return

if __name__ == '__main__':
    main()


