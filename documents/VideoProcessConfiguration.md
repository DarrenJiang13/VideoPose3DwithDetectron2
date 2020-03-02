# Project Configuration


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