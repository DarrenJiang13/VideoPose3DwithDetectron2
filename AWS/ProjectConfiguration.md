# Project Configuration

## 0. Check status of your GPU
run `nvidia-smi` to check the status of your GPU drivers. Just to make sure that you choose the right AWS instance.

## 1. ffmpeg and imagemagick installation
1. install ffmpeg
    
        sudo apt-get install ffmpeg  
        
2. install [imagemagick](https://linuxconfig.org/how-to-install-imagemagick-7-on-ubuntu-18-04-linux)
    
    **ImageMagick Compilation Dependencies**
    
        sudo apt-get update
        sudo apt build-dep imagemagick
        
    **Download ImageMagick Source files**
    
        wget https://www.imagemagick.org/download/ImageMagick.tar.gz
        tar xf ImageMagick.tar.gz
        cd ImageMagick-7.0.9-21/
        
    **ImageMagick Compilation and Installation**
    
        ./configure
        make
        sudo make install
        sudo ldconfig /usr/local/lib/
        
    **Confirm installation and final check**
    
        identify -version
    
## 2. Install pytorch
  1. In this instance we already have python2 python3 and cuda installed. Remember if you want to work with python3, choose `python3` and `pip3`.
  2. Go to [pytorch](https://pytorch.org/) to download pytorch. Here I choose Stable+Linux+pip+python+10.1. So the command line will be:
    
    pip3 install torch torchvision
  Now we can start to do the deep learning project.
  
  
## 3. Detectron2 Configuration([refer](https://github.com/facebookresearch/detectron2))
- **Requirenment:**  
    Make sure you have installed the following items before you install detectron2.
  - Linux or macOS with Python ≥ 3.6 (already done)
  - PyTorch ≥ 1.3(already done)
  - torchvision that matches the PyTorch installation. You can install them together at pytorch.org to make sure of this.(already done)
  - OpenCV, optional, needed by demo and visualization:
  
        pip3 install opencv-python --user
        
  - pycocotools:  
  
        pip3 install cython
        pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
        
- **[Install](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md)**  
    install Pre-Built Detectron2 for cuda 10.1:
        
        # for CUDA 10.1:
        pip3 install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/index.html
