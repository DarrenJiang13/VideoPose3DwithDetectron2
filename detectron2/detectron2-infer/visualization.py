import os
import shutil
import numpy as np
import cv2
import subprocess as sp


def load_keypoints_from_npz(path_to_npz, dataset_name='detectron2'):
	data = np.load(path_to_npz, encoding='latin1', allow_pickle=True)
	meta = data['metadata'].item()
	keypoints = data['positions_2d'].item()[dataset_name]['custom'][0]

	return keypoints, meta


def remove_dir(dir):
	try:
		shutil.rmtree(dir)
	except OSError as e:
		print ("Error: %s - %s." % (e.filename, e.strerror))


def frames_to_video(src_path, dst_path, fps=30):
	os.system("ffmpeg -framerate %s -pattern_type glob -f image2 -i '%s/*.jpeg' %s" % (fps, src_path, dst_path))


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
		yield cv2.imread(path), path


def read_video(filename):
	w, h = get_resolution(filename)

	command = ['ffmpeg',
			'-i', filename,
			'-f', 'image2pipe',
			'-pix_fmt', 'bgr24',
			'-vsync', '0',
			'-vcodec', 'rawvideo', '-']

	pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
	i = 0
	while True:
		i += 1
		data = pipe.stdout.read(w*h*3)
		if not data:
			break
		yield np.frombuffer(data, dtype='uint8').reshape((h, w, 3)), str(i-1).zfill(5)


def get_resolution(filename):
	command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
			   '-show_entries', 'stream=width,height', '-of', 'csv=p=0', filename]
	pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=-1)
	for line in pipe.stdout:
		w, h = line.decode().strip().split(',')
		return int(w), int(h)


def draw_body_joints_2d(img_orig, pts2d, bones=None, draw_indices=None):
	img = img_orig.copy()

	for i in range(len(pts2d)):
		x = int(round(pts2d[i][0]))
		y = int(round(pts2d[i][1]))
		img = cv2.circle(img, (x,y), 5, (0,0,255), 5)

		if draw_indices is not None:
				font = cv2.FONT_HERSHEY_SIMPLEX
				bottomLeftCornerOfText = (x,y)
				fontScale = 1
				fontColor = (255,255,255)
				lineType = 2
				cv2.putText(img,str(i), bottomLeftCornerOfText, font, fontScale,fontColor,lineType)

		if bones is not None:
			for bone in bones:
				pt1 = (int(round(pts2d[bone[0]][0])), int(round(pts2d[bone[0]][1])))
				pt2 = (int(round(pts2d[bone[1]][0])), int(round(pts2d[bone[1]][1])))
				img = cv2.line(img,pt1,pt2,(255,0,0),4)

	return img


def visualize_keypoints(img_generator, keypoints, mp4_output_path, fps=30, draw_joint_indices=None):
	'''
	Visualize keypoints (2d body joints) detected by Detectron2:
		img_generator:      Images source (images or video)
		keypoints:          Body keypoints detected by Detectron2
		mp4_output_path:    The path where the result will be saved in .mp4 format
		fps:                FPS of the result video
		draw_joint_indices: Draw body joint indices (in COCO format)
	'''
	body_edges_17 = np.array([[0,1],[1,3],[2,0],[4,2],[5,7],[6,5],[7,9],[8,6],[10,8],
							  [11,5],[12,6],[12,11],[13,11],[14,12],[15,13],[16,14]])

	#Create a temp_dir to save intermediate results:
	temp_dir = './temp'
	if os.path.exists(temp_dir):
		remove_dir(temp_dir)
	os.makedirs(temp_dir)

	#Draw keypoints and save the result:
	for i, (img, img_path) in enumerate(img_generator):
		frame_joint2d = keypoints[i]
		
		img = draw_body_joints_2d(img, frame_joint2d, bones=body_edges_17, draw_indices=draw_joint_indices)

		img_name = img_path.split('/')[-1].split('.')[0]
		out_path = os.path.join(temp_dir,img_name + '.jpeg')
		cv2.imwrite(out_path,img)

		print('{}      '.format(i+1), end='\r')

	#Convert images to video:
	frames_to_video(temp_dir, mp4_output_path, fps=fps)
	remove_dir(temp_dir)

	print ('All done!')


if __name__ == '__main__':
	#Load keypoints from .npz:
	keypoints_npz_path = './pose2d.npz'
	keypoints,_ = load_keypoints_from_npz(keypoints_npz_path, dataset_name='detectron2')

	# img_generator = read_images('./images')    # read images from a directory
	img_generator = read_video('./video.mp4')  # or get them from a video

	#Visualize the keypoints:
	visualize_keypoints(img_generator, keypoints, mp4_output_path='./output.mp4')
