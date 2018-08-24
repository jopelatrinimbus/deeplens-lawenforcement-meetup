# deeplens-lawenforcement-meetup
Application that demonstrate integration of AWS Deeplens and AWS Rekognition
in a law enforcement scenario


## Introduction
DeepEnforcement is an application that helps law enforcement find suspect 
through their cctv imagery. The workflow is as follow.

1. A face recognition model is uploaded on a cctv camera (DeepLens).
2. Deeplens runs a lambda that upload images to S3 once a face is
recognized by the model.
3. A system user uploads a picture of the wanted person on an S3 bucket.
4. A Rekognition Collection is created from the suspect image and the face
is indexed.
5. A Rekognition Stream processor analyses the Kinesis Video Stream and looks
for the suspect face.
6. Analysis data are pushed to a Kinesis Data stream for further processing.

## Environment Setup
```bash
git clone https://github.com/jopelatrinimbus/deeplens-lawenforcement-meetup.git
cd deeplens-lawenforcement-meetup
virtualenv -p python3 .deepenv
source .deepenv/bin/activate
pip install -r requirements.txt
```

## Deployment
TBD ...

## Author
Jonathan Pelletier (jonathan.pelletier1@gmail.com)
