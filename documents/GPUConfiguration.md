# Nvidia Driver+CUDA10.1+Cudnn+Pytorch+Detectron Installation for ubuntu18.04 with your own computer  
My computer is Lenovo-Legion Y7000  
**GPU**:GTX 1060

## 1 install nvidia driver (from ubuntu apt-repository)  

- Add new repository in local  

        sudo add-apt-repository ppa:graphics-drivers/ppa
    
- Update local repository information 

        sudo apt update && sudo apt upgrade -y 
        
- Show all devices which need drivers, and which packages apply to them.
        
        ubuntu-drivers devices 
        
- Assuming that we install nvidia-driver-435
        
        sudo apt install nvidia-driver-435
        
- Restart the computer and check the nvidia driver
        
        nvidia-smi  
    
## 2 install CUDA 10.1 (using local runfile)
- Download local runfile from [cuda](https://developer.nvidia.com/cuda-10.1-download-archive-update2?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=runfilelocal)

        wget http://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux.run

- run the runfile

        sudo sh cuda_10.1.243_418.87.00_linux.run
**Uncheck the box of the drivers which is nvidia driver 418 during installation**, or your drivers would be replaced by 418.  
You may find a warning like 

        "Incompleted installation！ This installation did not install the CUDA Driver. A driver of version at least ...". 
No worries! That is because you are using your own nvidia driver rather than the nvidia provided one(nvidia 418).

- Configure Environment Variable
        
        sudo gedit ~/.bashrc
  add following 3 lines to the `.bashrc` file:
  
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.1/lib64
        export PATH=$PATH:/usr/local/cuda-10.1/bin
        export CUDA_HOME=$CUDA_HOME:/usr/local/cuda-10.1
  turn off the gedit. Start a new termimal and type:
  
        source ~/.bashrc
- Check the cuda 10.1  
Start a new termimal and type:

        nvcc -V  
You should be able to see the cuda version which is 10.1:

        nvcc: NVIDIA (R) Cuda compiler driver
        Copyright (c) 2005-2019 NVIDIA Corporation
        Built on Sun_Jul_28_19:07:16_PDT_2019
        Cuda compilation tools, release 10.1, V10.1.243

## 3 install cuDNN 7.6.5
- Download essential `.deb` files from [cudnn](https://developer.nvidia.com/rdp/cudnn-download)
as we are using CUDA 10.1, we should download:  
        [cuDNN Library for Linux](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.1_20191031/cudnn-10.1-linux-x64-v7.6.5.32.tgz)  
        [cuDNN Runtime Library for Ubuntu18.04 (Deb)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.1_20191031/Ubuntu18_04-x64/libcudnn7_7.6.5.32-1%2Bcuda10.1_amd64.deb)  
        [cuDNN Developer Library for Ubuntu18.04 (Deb)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.1_20191031/Ubuntu18_04-x64/libcudnn7-dev_7.6.5.32-1%2Bcuda10.1_amd64.deb)  
        [cuDNN Code Samples and User Guide for Ubuntu18.04 (Deb)](https://developer.nvidia.com/compute/machine-learning/cudnn/secure/7.6.5.32/Production/10.1_20191031/Ubuntu18_04-x64/libcudnn7-doc_7.6.5.32-1%2Bcuda10.1_amd64.deb)  
   You may need to register before you download the resources.  
   
- `cd` to where you save the download files(for me it is /Downloads)

        cd Downloads/
        
- install **cuDNN Library for Linux**

        tar -zxvf cudnn-10.1-linux-x64-v7.6.5.32.tgz
        sudo cp cuda/include/cudnn.h /usr/local/cuda-10.1/include
        sudo cp cuda/lib64/libcudnn* /usr/local/cuda-10.1/lib64
        sudo chmod a+r /usr/local/cuda-10.1/include/cudnn.h
        sudo chmod a+r /usr/local/cuda-10.1/lib64/libcudnn*
  you can run `cat /usr/local/cuda-10.1/include/cudnn.h | grep CUDNN_MAJOR -A 2` to check the cudnn version
  
- install **cuDNN Runtime Library,Developer Library and Code Samples** (in the right order!!)

        sudo dpkg -i libcudnn7_7.6.5.32-1+cuda10.1_amd64.deb
        sudo dpkg -i libcudnn7-dev_7.6.5.32-1+cuda10.1_amd64.deb
        sudo dpkg -i libcudnn7-doc_7.6.5.32-1+cuda10.1_amd64.deb
        
 - check cuDNN installation
 
        cp -r /usr/src/cudnn_samples_v7/ $HOME
        cd $HOME/cudnn_samples_v7/mnistCUDNN
        make clean && make
        ./mnistCUDNN
   When you see:
   
        Result of classification: 1 3 5
        Test passed!
   
   Now you finished the installation.
   
## 4 install pytorch
- install pip for python3

        sudo apt-get install python3-pip

- Install [pytorch](https://pytorch.org/get-started/locally/) to download pytorch. Here I choose Stable+Linux+pip+python+10.1. So the command line will be:
    
        pip3 install torch torchvision
    
  As I want to work with python3.
  
  Now we can start to do the deep learning project.
  
- Check pytorch version
  Start a new terminal:
  
        python3
        import torch
        print(torch.__version__)
        
