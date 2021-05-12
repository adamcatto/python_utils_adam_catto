import os
from fileinput import FileInput


def list_all_files_in_dir(input_dir, file_types=[]):
	if file_types:
		result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_dir) for f in filenames if os.path.splitext(f)[1] in file_types]
	else:
		result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_dir) for f in filenames]

	return result


def find_and_replace_all_in_dir(input_dir, find_str, replace_str, file_types=[]):
	files = list_all_files_in_dir(input_dir, file_types)
	print(files)
	for filename in files:
		f = open(filename,'r')
		file_data = f.read()
		f.close()

		new_str = file_data.replace(find_str, replace_str)

		f = open(filename,'w')
		f.write(new_str)
		f.close()
