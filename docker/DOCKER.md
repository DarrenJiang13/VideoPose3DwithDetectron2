# Docker your project

## 1. Install [docker engine](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- uninstall old versions

        sudo apt-get remove docker docker-engine docker.io containerd runc
- setup the repo   
    1. install update

            sudo apt-get update

    2. Install packages to allow apt to use a repository over HTTPS:
    
            sudo apt-get install \
            apt-transport-https \
            ca-certificates \
            curl \
            gnupg-agent \
            software-properties-common
        
    3. Add Docker’s official GPG key:

            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
            # verify
            sudo apt-key fingerprint 0EBFCD88
            
    4. set the stable repo
    
           sudo add-apt-repository \
           "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
           $(lsb_release -cs) \
           stable"
- install docker engine-community(latest)

        sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io
        
- check installation correctly

        sudo docker run hello-world
  or you can use `docker version` to check the version of your docker.
  
  
## 2. Install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
This is for those docker working with GPUs.  
Make sure you have installed the NVIDIA driver and Docker 19.03 for your Linux distribution.  
Note that you do not need to install the CUDA toolkit on the host, but the driver needs to be installed.  
  
for **Ubuntu 18.04** 
  
        # Add the package repositories
        distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
        curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
        curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
        
        sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
        sudo systemctl restart docker
  
check your docker:
  
        #### Test nvidia-smi with the latest official CUDA image
        sudo docker run --gpus all nvidia/cuda:10.0-base nvidia-smi
  you should see a output of your gpu conditions.
  
## 3. Build docker image for this project 
**This docker image is created with Nvidia driver 435, Cuda10.1**
Download this repo, from the root diretory, go to `docker` folder.
        
        cd docker
        sudo docker image build -t video-pose-infer-demo:v1 .
        
## 4. Check your images

use `sudo docker images` or `sudo docker image ls`
you can see the ouput like this:
  
  | REPOSITORY            | TAG               | IMAGE ID     | CREATED        | SIZE   |
  |-----------------------|-------------------|--------------|----------------|--------|
  | video-pose-infer-demo | v1                | f8eca520702b | 6 minutes ago  | 7.47GB |
  | nvidia/cuda           | 10.1-cudnn7-devel | b4879c167fc1 | 2 months ago   | 3.67GB |

## 5. Run the docker image
we can use the **first 3 members of IMAGE ID** to run the image. like for "video-pose-infer-demo":
    
    sudo docker run --gpus all -it f8e
or 

    sudo docker run --gpus all -it video-pose-infer-demo:v1

Congratulations! now you are in the docker image.
    
## 6. Run the project
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

  ## Some useful commands:
  - image 
  
     1. check the image information
            
            sudo docker image ls
     2. remove the image (you can fully remove the image only when you kill and remove all the containers referring to that image)
            
            sudo docker image rm [IMAGE_ID]
     3. run the image
     
            sudo docker run -it [IMAGE]
     4. run the image with GPU enabled
     
            sudo docker run --gpus all -it [IMAGE]
     5. build an image
            
            sudo docker image build -t [image_name] .
  
  - container
  
    1. check the containers information
    
            sudo docker container ls --all
    2. kill the containers information
    
            sudo docker container kill [container_id]
    3. remove the containers information
            
            sudo docker container rm [container_id]
    4. copy files from docker to your host computer
            
            sudo docker cp [container_id]:path/to/your/file/in/docker output/path/in/your/computer 
  
