import os
import sys
import numpy as np
import cv2
import subprocess as sp
import detectron2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg


def get_img_paths(imgs_dir):
	img_paths = []
	for dirpath, dirnames, filenames in os.walk(imgs_dir):
		for filename in [f for f in filenames if f.endswith('.png') or f.endswith('.PNG') or f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.jpeg') or f.endswith('.JPEG')]:
			img_paths.append(os.path.join(dirpath,filename))
	img_paths.sort()

	return img_paths

def read_images(dir_path):
	img_paths = get_img_paths(dir_path)
	for path in img_paths:
		yield cv2.imread(path)


def get_resolution(filename):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
               '-show_entries', 'stream=width,height', '-of', 'csv=p=0', filename]
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
    for line in pipe.stdout:
        w, h = line.decode().strip().split(',')
        return int(w), int(h)


def read_video(filename):
    w, h = get_resolution(filename)

    command = ['ffmpeg',
            '-i', filename,
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vsync', '0',
            '-vcodec', 'rawvideo', '-']

    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
    while True:
        data = pipe.stdout.read(w*h*3)
        if not data:
            break
        yield np.frombuffer(data, dtype='uint8').reshape((h, w, 3))


def init_pose_predictor(config_path, weights_path, cuda=True):
	cfg = get_cfg()
	cfg.merge_from_file(config_path)
	cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
	cfg.MODEL.WEIGHTS = weights_path
	if cuda == False:
		cfg.MODEL.DEVICE='cpu'
	predictor = DefaultPredictor(cfg)

	return predictor


def encode_for_videpose3d(boxes,keypoints,resolution, dataset_name):
	# Generate metadata:
	metadata = {}
	metadata['layout_name'] = 'coco'
	metadata['num_joints'] = 17
	metadata['keypoints_symmetry'] = [[1, 3, 5, 7, 9, 11, 13, 15], [2, 4, 6, 8, 10, 12, 14, 16]]
	metadata['video_metadata'] = {dataset_name: resolution}

	prepared_boxes = []
	prepared_keypoints = []
	for i in range(len(boxes)):
		if len(boxes[i]) == 0 or len(keypoints[i]) == 0:
			# No bbox/keypoints detected for this frame -> will be interpolated
			prepared_boxes.append(np.full(4, np.nan, dtype=np.float32)) # 4 bounding box coordinates
			prepared_keypoints.append(np.full((17, 4), np.nan, dtype=np.float32)) # 17 COCO keypoints
			continue

		prepared_boxes.append(boxes[i])
		prepared_keypoints.append(keypoints[i][:,:2])
		
	boxes = np.array(prepared_boxes, dtype=np.float32)
	keypoints = np.array(prepared_keypoints, dtype=np.float32)
	keypoints = keypoints[:, :, :2] # Extract (x, y)
	
	# Fix missing bboxes/keypoints by linear interpolation
	mask = ~np.isnan(boxes[:, 0])
	indices = np.arange(len(boxes))
	for i in range(4):
		boxes[:, i] = np.interp(indices, indices[mask], boxes[mask, i])
	for i in range(17):
		for j in range(2):
			keypoints[:, i, j] = np.interp(indices, indices[mask], keypoints[mask, i, j])
	
	print('{} total frames processed'.format(len(boxes)))
	print('{} frames were interpolated'.format(np.sum(~mask)))
	print('----------')
	
	return [{
		'start_frame': 0, # Inclusive
		'end_frame': len(keypoints), # Exclusive
		'bounding_boxes': boxes,
		'keypoints': keypoints,
	}], metadata


def predict_pose(pose_predictor, img_generator, output_path, dataset_name='detectron2'):
	'''
		pose_predictor: The detectron's pose predictor
		img_generator:  Images source
		output_path:    The path where the result will be saved in .npz format
	'''
	boxes = []
	keypoints = []
	resolution = None

	# Predict poses:
	for i, img in enumerate(img_generator):
		pose_output = pose_predictor(img)

		if len(pose_output["instances"].pred_boxes.tensor) > 0:
			cls_boxes = pose_output["instances"].pred_boxes.tensor[0].cpu().numpy()
			cls_keyps = pose_output["instances"].pred_keypoints[0].cpu().numpy()
		else:
			cls_boxes = np.full((4,), np.nan, dtype=np.float32)
			cls_keyps = np.full((17,3), np.nan, dtype=np.float32)   # nan for images that do not contain human

		boxes.append(cls_boxes)
		keypoints.append(cls_keyps)

		# Set metadata:
		if resolution is None:
			resolution = {
				'w': img.shape[1],
				'h': img.shape[0],
			}

		print('{}      '.format(i+1), end='\r')

	# Encode data in VidePose3d format and save it as a compressed numpy (.npz):
	data, metadata = encode_for_videpose3d(boxes, keypoints, resolution, dataset_name)
	output = {}
	output[dataset_name] = {}
	output[dataset_name]['custom'] = [data[0]['keypoints'].astype('float32')]
	np.savez_compressed(output_path, positions_2d=output, metadata=metadata)

	print ('All done!')



if __name__ == '__main__':
	# Init pose predictor:
	model_config_path = './keypoint_rcnn_X_101_32x8d_FPN_3x.yaml'
	model_weights_path = './model_final_5ad38f.pkl'	
	pose_predictor = init_pose_predictor(model_config_path, model_weights_path, cuda=True)

	# Predict poses and save the result:
	# img_generator = read_images('./images')    # read images from a directory
	img_generator = read_video(sys.argv[1])  # or get them from a video
	output_path = '../../data/data_2d_custom_myvideos'
	predict_pose(pose_predictor, img_generator, output_path)
