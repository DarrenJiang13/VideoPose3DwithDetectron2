# VideoPose3D project with detectron2

## Problem Statement
Human Pose Estimation is about estimating 2D and 3D localization of human joints in images or videos.
Generally this process can be divided into 2 parts: 1. 2D keypoint detection from 2D 
videos; 2. 3D Pose estimation from 2D keypoints. Temporal RNN is widely used to solve this problem.
 However, it can not parallelly process multiple frames. Temporal CNN has been proved competitively in some areas 
 like neural machine translation, language modeling and speed generation. So this project use Temporal CNN for 3D Pose estimation. 
 Moreover, with the pre-trainded model, can we estimate human 3D pose from arbitrary 2D video?

In this project,firstly we use the Detectron2 to detect the 2D joint keypoints from an arbitrary 2D video. Then a pre-trained 
model is applied for predicting 3D joint keypoints from 2D keypoints.

*: This project is mainly about how to implement video-pose-3D project of facebook research 
for inference in the wild in your own computer. Instead of detectron, we use detectron2 here.

![Alt Text](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/images/example.gif)

Reference: 
- [VideoPose3D Project](https://github.com/facebookresearch/VideoPose3D)
- [VideoPose3D_with_Detectron2](https://github.com/darkAlert/VideoPose3d_with_Detectron2)

## Input & Output
**Input:**   
An arbitrary `.mp4` video file. Recommend: one person in an empty field.  
**Output:**  
A video combining the original video and 3D human joint keypoints drawn in a 3D coordinate. Like the "girl playing taiji" picture shown above.

## Configure your computer
0. Install ffmpeg imgMagick, see [this](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/documents/VideoProcessConfiguration.md)
1. Install Nvidia Driver,CUDA10.1,cuDNN 7.6.5,pytorch, see [this](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/documents/GPUConfiguration.md)
2. Install detectron2, see [this](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/documents/Detectron2Installation.md)

## Model setup
1. download model for 2D detection(detectron2)

        cd detectron2/detectron2-infer
        wget https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x/139686956/model_final_5ad38f.pkl
        
2. download model for 3D prediction
        
        # in the root directory, make a folder called checkpoint 
        mkdir checkpoint
        cd checkpoint
        wget https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin

## How to train the model
As we use the model provide by [dariopavllo](https://github.com/facebookresearch/VideoPose3D/blob/master/INFERENCE.md),
there is no better way to retrain the model. The input keypoints is in COCO format. And output 3D joint positions in Human3.6M format.
For how to use the pre-trained model, please see the next step. 

## Estimate your arbitrary 2D video
- Firstly, you should put the video you want into the `detectron2/detectron2-infer/videos` folder;
- Then:

        cd detectron2/detectron2-infer
- Run the `.sh` file:
        
        sh infer.sh videos/[your-video-name] [output-video-name-you-want]
- You shall see the output video in the `output` folder of the root directory.

## Docker:
You can directly run the dockerfile as all the files needed in dockerfile can be download online.
For the dockerfile and more details about dockerizing this project.  
Please go to [docker](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/docker)

To pull this docker image from docker hub:

        sudo docker pull yjjiang1996/video_pose_3d_detectron2_test1:latest

In the docker image:
- Copy your video to the `videos` folder
    
        cd detectron2/detectron2-infer/videos
        [download your videos here]
        # you can also use the videos we provided: taiji.mp4, taiji2.mp4, video.mp4
- Go back the the `detectron2/detectron2-infer` folder and run the `.sh` file.

        cd ..
        sh infer.sh videos/[your-video-name] [output-video-name-you-want]
        # for example: sh infer.sh videos/taiji.mp4 taiji
        
- You shall see the output video in the `output` folder of the root directory.
- As you cannot see the video in the docker, you can copy the videos out to your current directory.
 Now turn on a new terminal and input:
        
        sudo docker cp [container_id]:/home/appuser/video_pose_repo/output/[you_video_name].mp4 .
   
## AWS instance:
1. Build a Amazon EC2 instance, see [AWSConfiguration](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/AWS/AWSConfiguration.md)
2. Implement your project on your instance , see [ProjectConfiguration](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/AWS/ProjectConfiguration.md)
