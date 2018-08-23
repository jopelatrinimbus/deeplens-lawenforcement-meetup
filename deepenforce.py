#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import boto3
import logging
import numpy as np
import cv2

from io import BytesIO

def main():

    parser = argparse.ArgumentParser()

    DEFAULT_REFERENCE_BUCKET = 'deepenforcement-reference'
    parser.add_argument(
            '-r',
            '--reference-bucket',
            help='name of the bucket containing the reference',
            default=DEFAULT_REFERENCE_BUCKET)

    parser.add_argument(
            '-s',
            '--source-key',
            required=True,
            help='s3 key of the source image to compare against candidates')

    DEFAULT_CANDIDATES_BUCKET = 'deepenforcement-candidates'
    parser.add_argument(
            '-c',
            '--candidates-bucket',
            help='name of the bucket containing the candidate images streamed from Deeplens',
            default=DEFAULT_CANDIDATES_BUCKET)

    DEFAULT_MATCHED_BUCKET = 'deepenforcement-matched'
    parser.add_argument(
            '-m',
            '--matched-bucket',
            help='name of the bucket where to move matched images',
            default=DEFAULT_MATCHED_BUCKET)

    DEFAULT_UbuckeiNMATCHED_BUCKET = 'deepenforcement-unmatched'
    parser.add_argument(
            '-u',
            '--unmatched',
            help='name of the bucket where t move the unmatched argument',
            default=DEFAULT_UNMATCHED_BUCKET)

    parser.add_argument(
            '-p',
            '--profile',
            help='the profile to use with the boto3 API calls',
            default=None)

    parser.add_argument(
            '-R',
            '--region',
            help='region to use with API client',
            default='us-east-1'
            )

    DEFAULT_SIMILARITY_THRESHOLD = 65
    parser.add_argument(
            '-S',
            '--similarity-threshold',
            help='similarity value beyond which faces are considered similar',
            type=float,
            default=DEFAULT_SIMILARITY_THRESHOLD)


    args = parser.parse_args()

    if args.profile:
        boto3.setup_default_session(profile_name=args.profile, region_name=args.region)

    # make sure there is a face in the reference image
    rekognition = boto3.client('rekognition')
    reference_image = {
            'S3Object': {
                'Bucket':args.reference_bucket,
                'Name':args.source_key
                }
            }

    detect_face_reference = rekognition.detect_faces(Image=reference_image, Attributes=['ALL'])
    if not detect_face_reference['FaceDetails']:
        print('according to rekognition, your reference image contains no face. Try again with a new image')
        exit(-1)

    # get a list of all the candidates to compare
    s3 = boto3.client('s3')
    content = s3.list_objects(Bucket=args.candidates_bucket)

    has_content = 'Contents' in content
    if not has_content:
        print('there is no object in the candidate bucket. Please capture more images and try again')
        exit(-2)


    candidate_keys = [ c['Key'] for c in content['Contents'] ]


    for candidate in candidate_keys:

        # make sure there is a face in our image
        face_detection = rekognition.detect_faces(
                Image={
                    'S3Object': {
                        'Bucket':args.candidates_bucket,
                        'Name':candidate}
                    },
                Attributes=['ALL']
                )

        if not face_detection['FaceDetails']:
            # delete the file from the candidate bucket and move on
            s3.delete_object(Bucket=args.candidates_bucket, Key=candidate)
            continue

        # There is a face in our candiate image, compare it to the reference
        comparison = rekognition.compare_faces(
                SourceImage = {
                    'S3Object': {
                        'Bucket':args.reference_bucket,
                        'Name':args.source_key
                        }
                    },
                TargetImage = {
                    'S3Object': {
                        'Bucket': args.candidates_bucket,
                        'Name': candidate
                        }
                    },
                SimilarityThreshold=args.similarity_threshold)

        if comparison['FaceMatches']:
            # Download the image from the bucket
            content = s3.get_object(Bucket=args.candidates_bucket, Key=candidate)

            # transform into something we can play with
            np_img = np.frombuffer(content['Body'].read(), np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            for face in comparison['FaceMatches']:
                # draw the bounding box around the matche
                bb = face['Face']['BoundingBox']

                continue

            # Upload the face to matched
            s3.copy_object(Bucket=args.matched_bucket, Key=candidate, CopySource={'Bucket':args.candidates_bucket, 'Key':candidate})
        else:
            # no match: move to unmatched
            s3.copy_object(Bucket=args.unmatchedbuckei, Key=candidate, CopySource={'Bucket':args.candidates_bucket, 'Key':candidate})


        # remove the image from the candidate bucket
        s3.delete_object(Bucket=args.candidates_bucket, Key=candidate)

    print('analysis done')
    eturn

if __name__ == '__main__':
    main()
    DEFAULT_MATCHED_BUCKET = 'deepenforcement-matched'
    parser.add_argument(
            '-m',
            '--matched-bucket',
            help='name of the bucket where to move matched images',
            default=DEFAULT_MATCHED_BUCKET)


