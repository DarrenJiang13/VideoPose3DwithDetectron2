FROM nvidia/cuda:10.1-cudnn7-devel
# this docker file is based on the dockerfile of detectron2
# build this docker:
#   sudo docker image build -t video-pose-infer-demo:v1 .


ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev git wget sudo && \
  rm -rf /var/lib/apt/lists/*


# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser
ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py


# install dependencies like pytorch
# See https://pytorch.org/ for other options if you use a different version of CUDA
RUN pip3 install --user torch torchvision tensorboard cython
RUN pip3 install --user 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN pip3 install --user 'git+https://github.com/facebookresearch/fvcore'


# get our repo
RUN git clone https://github.com/DarrenJiang13/VideoPose3DwithDetectron2.git video_pose_repo
# for dataset setup:
RUN wget -P /home/appuser/video_pose_repo/checkpoint https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin
RUN wget -P /home/appuser/video_pose_repo/detectron2/detectron2-infer https://dl.fbaipublicfiles.com/detectron2/COCO-Keypoints/keypoint_rcnn_X_101_32x8d_FPN_3x/139686956/model_final_5ad38f.pkl


# install pre-build detectron2
ENV FORCE_CUDA="1"
# This will build detectron2 for all common cuda architectures and take a lot more time,
# because inside `docker build`, there is no way to tell which architecture will be used.
ENV TORCH_CUDA_ARCH_LIST="Kepler;Kepler+Tesla;Maxwell;Maxwell+Tegra;Pascal;Volta;Turing"
# for CUDA 10.1:
RUN pip3 install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/index.html


# install ffmpeg for video processing
RUN sudo apt-get update && sudo apt-get install -y ffmpeg  

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"
WORKDIR /home/appuser/video_pose_repo
