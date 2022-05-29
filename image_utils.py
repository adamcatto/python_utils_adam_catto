import os

import numpy as np
import skimage


config = {}
# add key-value pairs to config corresponding to argument names/values in `make_video_ffmpeg()`
# e.g.
#config['ffmpeg_path'] = '/path/to/ffmpeg_executable_on_your_system'


def make_video_ffmpeg(ffmpeg_path, frame_rate=30, format_type=None, resolution=(1920,1080),
			start_number=None, image_dir='', filename_prefix='', image_type='jpg', padding_type=None, num_frames=None,
			vcodec_type='libx264', constant_rate_factor=20, pixel_format='yuv420p', video_out_file='', execute_cmd=True, verbose=True):

	cmd_str = ffmpeg_path
	# path/to/ffmpeg
	
	cmd_str += ' -r ' + str(frame_rate)
	# path/to/ffmpeg -r frame_rate

	if format_type:
		cmd_str += ' -f ' + format_type
	# path/to/ffmpeg -r frame_rate -f format_type

	cmd_str += ' -s ' + str(resolution[0]) + 'x' + str(resolution[1])
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2

	if start_number:
		cmd_str += ' -start_number ' + str(start_number)
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number

	cmd_str += ' -i ' + os.path.join(image_dir, filename_prefix) + '%'
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%

	if padding_type:
		if isinstance(padding_type, int):
			cmd_str += '0'
			cmd_str += str(padding_type)
		elif isinstance(padding_type, str) and padding_type[0] != '0':
			cmd_str += '0'
			cmd_str += padding_type
		elif isinstance(padding_type, str) and padding_type[0] == '0':
			cmd_str += padding_type
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}

	cmd_str += 'd'
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d
	
	if image_type[0] != '.':
		image_type = '.' + image_type

	cmd_str += image_type
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d.image_type
	
	if not num_frames:
		num_frames = len([f for f in os.listdir(image_dir) if f[-4:] == image_type])

	cmd_str += ' -vframes ' + str(num_frames)
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d.image_type -vframes num_frames

	cmd_str += ' -vcodec ' + vcodec_type
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d.image_type -vcodec vcodec_type

	cmd_str += ' -crf ' + str(constant_rate_factor)
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d.image_type -vcodec vcodec_type -crf constant_rate_factor

	cmd_str += ' -pix_fmt ' + pixel_format
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d.image_type -vcodec vcodec_type -crf constant_rate_factor -pix_fmt pixel_format

	cmd_str += ' ' + video_out_file
	# path/to/ffmpeg -r frame_rate -f format_type -s res1xres2 -start_number start_number -i path/to/imgs/prefix%{padding_type}d.image_type -vcodec vcodec_type -crf constant_rate_factor -pix_fmt pixel_format video_out_file

	if verbose:
		print(cmd_str)

	if execute_cmd:
		os.system(cmd_str)

	return cmd_str


def pad_to_size(img, new_shape, fill_cval=0):
    img_shape = img.shape
    vertical_is_odd = img.shape[0] % 2 == 1
    horizontal_is_odd = img.shape[1] % 2 == 1
    vertical_pad = (new_shape[0] - img.shape[0]) // 2
    horizontal_pad = (new_shape[1] - img.shape[1]) // 2
    new_img = np.ones(new_shape) * fill_cval
    print(new_img.shape)
    new_img[
        vertical_pad: vertical_pad + img.shape[0],
        horizontal_pad: horizontal_pad + img.shape[1],
        :
    ] = img
    return new_img


def make_2d_gaussian_kernel_matrix(size: int, normalize: bool) -> np.ndarray:
	# == from scipy docs
	t = np.linspace(-10, 10, size)
	bump = np.exp(-0.1*t**2)
	bump /= np.trapz(bump) # normalize the integral to 1

	# make a 2-D kernel out of it
	kernel = bump[:, np.newaxis] * bump[np.newaxis, :]
	if normalize:
		kernel /= np.max(kernel)
	return kernel


def dynamic_alpha_blend_with_kernel(
	background_img: np.ndarray, 
	foreground_img: np.ndarray, 
	kernel: np.ndarray
) -> np.ndarray:
	assert background_img.shape == foreground_img.shape
	assert background_img.shape[0] == kernel.shape[0] 
	assert background_img.shape[1] == kernel.shape[1]

	if len(background_img.shape) == 3:
		if len(kernel.shape) == 2:
			kernel = np.dstack([kernel]*background_img.shape[2])

	foreground = ((kernel*foreground_img)).astype(int)
	background = ((1-kernel)*background_img).astype(int)
	blended = foreground + background
	return blended


if __name__ == '__main__':
	config['ffmpeg_path'] = '/Users/adamcatto/downloads/ffmpeg'
	config['frame_rate'] = 2
	config['format_type'] = 'image2'
	config['start_number'] = 0
	config['image_dir'] = '/Users/adamcatto/src/dippy/input_data/gray_tunnel_sequence'
	config['video_out_file'] = '/Users/adamcatto/desktop/bpu.mp4'
	config['num_frames'] = 140
	config['resolution'] = (704, 480)
	config['image_type'] = 'png'
	config['padding_type'] = 4


	def main(config):
		# -- system_1 montage
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_1/montages/'
		config['num_frames'] = 150
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_1/montage.mp4'
		cmd_str = make_video_ffmpeg(**config)

		# -- system_2 montage
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_2/montages/'
		config['num_frames'] = 140
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_2/montage.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_2 background
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_2/backgrounds/'
		config['num_frames'] = 140
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_2/backgrounds.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_3 montage
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3/montages/'
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3/montage.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_3 background
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3/backgrounds/'
		config['num_frames'] = 140
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3/backgrounds.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_3a montage
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3a/montages/'
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3a/montage.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_3a background
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3a/backgrounds/'
		config['num_frames'] = 140
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_3a/backgrounds.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_4 montage
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_4/montages/'
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_4/montage.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)

		# -- system_4 background
		config['image_dir'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_4/backgrounds/'
		config['num_frames'] = 140
		config['video_out_file'] = '/Users/adamcatto/src/dippy/output_data/segmentation/system_4/backgrounds.mp4'
		config['start_number'] = 10
		cmd_str = make_video_ffmpeg(**config)





