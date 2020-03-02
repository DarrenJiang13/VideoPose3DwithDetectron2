python3 detectron_pose_predictor.py $1 $2
cd ../..
python3 run.py -d custom -k myvideos -arc 3,3,3,3,3 -c checkpoint --evaluate pretrained_h36m_detectron_coco.bin --render --viz-subject detectron2 --viz-action custom --viz-camera 0 --viz-video ./detectron2/detectron2-infer/$1 --viz-output output/$2.mp4 --viz-size 6
echo "Video Processing Finished. Output video is in the /output folder of the project directory."
