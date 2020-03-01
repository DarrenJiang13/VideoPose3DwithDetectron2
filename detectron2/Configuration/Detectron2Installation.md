# Detectron2 Configuration([refer](https://github.com/facebookresearch/detectron2))

## 1.Requirenment
  - Linux or macOS with Python ≥ 3.6 (already done)
  - PyTorch ≥ 1.3(already done)
  - torchvision that matches the PyTorch installation. You can install them together at pytorch.org to make sure of this.(already done)
  - OpenCV, optional, needed by demo and visualization:
  
        pip3 install opencv-python --user
        
  - pycocotools:  
  
        pip3 install cython
        pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
        
## 2.[Install](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md)  
- install Pre-Built Detectron2 for cuda 10.1:
        
        # for CUDA 10.1:
        pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/index.html
