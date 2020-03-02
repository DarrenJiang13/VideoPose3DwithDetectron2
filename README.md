# VideoPose3D project with detectron2

This project is about estimating 3D human pose from customized 2D video, 
whose 2D keypoints are provided by detectron2 rather than detectron. 
This project is mainly about how to implement video-pose-3D project of facebook research 
for inference in the wild in your own computer. 
Instead of detectron, we use detectron2 here.

![Alt Text](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/images/example.gif)

Reference: 
- [VideoPose3D Project](https://github.com/facebookresearch/VideoPose3D)
- [VideoPose3D_with_Detectron2](https://github.com/darkAlert/VideoPose3d_with_Detectron2)

## Configure your computer
0. Install ffmpeg imgMagick, see [this](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/documents/VideoProcessConfiguration.md)
1. Install Nvidia Driver,CUDA10.1,cuDNN 7.6.5,pytorch, see [this](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/documents/GPUConfiguration.md)
2. Install detectron2, see [this](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/documents/Detectron2Installation.md)

## Dataset setup
1. download checkpoints
        
        # in the root directory, make a folder called checkpoint 
        mkdir checkpoint
        cd checkpoint
        wget https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin

2. download model for detectron2

        cd detectron2/detectron2-infer
        wget https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x/139686956/model_final_5ad38f.pkl

## Estimate your customized video
- Firstly, you should put the video you want into the `detectron2/detectron2-infer/videos` folder;
- Then:

        cd detectron2/detectron2-infer
- Run the `.sh` file:
        
        sh infer.sh videos/[your-video-name] [output-video-name-you-want]
- You shall see the output video in the `output` folder of the root directory.

## Docker:
For more details about dockerize this project, and run the project in the docker image.
Please go to [docker.md](https://github.com/DarrenJiang13/VideoPose3DwithDetectron2/blob/master/docker/DOCKER.md)

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
