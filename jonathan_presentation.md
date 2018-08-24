# Jonathan presentation notes
Notes and preparation for the AWS meetup about deeplens.

## Presentation onset
Survey the audience for their background.

> by a show of hand, how many of you would consider themselves:
> 1. Machine Learning newbies, meaning you may have heard of it, but have no
     hands on experience.
> 2. Machine Learning amateurs, meaning you have *weekend project* experience
>    in ML.
> 3. Machine Learning practitionner, meaning you are have used done ML 
     and used the techniques in a practical use case for some time now.
> 4. Machine Learning guru's, meaning you have state-of-the-art knowledge of
     the newest ML models and techniques and/or practical experience deploying
     ML models for large scale inferance in products.

1. Explain to the audience that the presenter is a ML amateur, as defined
in the audience survey question.
2. Tell audience that the Goal of the presentation is:
    a. To acquire a feel, as builders, of how to integrate ML in your
       application.
    b. Understand what Deeplens can do and how it integrates in an ML-enabled
       application.
        
## Slides notes

### Page 2
Different ML applications shown:

1. Product suggestions for online shopping.
2. Autonomous Drone Flying (closely related to autonomous driving).
3. Information extraction from Picture.
4. Speach Recognition Application.a

### 1. Machine Learning Overview
> When we go through the Machine Learning Overview, I want you to keep in mind 
> the following scenario:
>> An healthcare company is trying to develop a new expert system that 
>> analysises chest x-ray images. The system should be able to tell when
>> a submitted image is from a patient suffering from penumonia.
> This simple scenario will tie all of the surveyed machine learning concepts
> to something real.

### Overview of Deep Learning
Depiction of steps in ML.

1. Data: Collect, Annotate, Preprocess
   a. Preprocess example: Taking a set of images with RGB channel and
      *collapsing* it to a greyscale image.
   b. Annotate example: Ask an *expert* to classify dataset.
   c. Data Split example: Keeping part of your data for ultimate validation.
2. Model Training: Define Architecture, Run Training Algo with data, Validate
3. Inference: Use your model and deploy it somewhere, Capture and store novel
   data, use the Deployed Model to get new prediction.

### 2. DEEPLENS OVERVIEW

#### DEEPLENS SPECIFICATIONS
1. 100 GFLOPS == 1/10 of the performance of an X-BOX ONE
2. Deeplens Provides you with GPU processing features that will accelerate 
   inference on your trained model.
3. TODO: Try to benchmark the inference step of the model.

#### UNDER THE COVERS
1. The purpose of deeplens is to execute projects.
2. A project is a combination of 2 things: A lambda function and model.
3. Lambda function are run on the Camera and dont have the time limits of the 
   usual lambdas (they me run indefinitely).
4. You implement the application logic in the lambda and are free to respond to 
   inference results in the way you deem satisfactory.
5. You can manipulate the frames through the lambda function and modify the project stream.
    
