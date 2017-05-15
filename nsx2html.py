import os
import sys
import shutil
import zipfile
import json

TEST_NSX = '20170516_005336_10741_xjk.nsx'


def join_path(path1, path2):
	return os.path.join(path1, path2)


def abs_path(relevant_path):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), relevant_path)


def delete_folder(folder):
	shutil.rmtree(folder, ignore_errors=True)


def get_nsx_file_name():
	assert sys.argv == 2
	return sys.argv[1]


def unzip_nsx(nsx_file, unzip_folder):
	delete_folder(unzip_folder)
	os.mkdir(unzip_folder)
	zip_ref = zipfile.ZipFile(nsx_file, 'r')
	zip_ref.extractall(unzip_folder)
	zip_ref.close()


def load_folder_content(folder):
	with open(join_path(folder, 'config.json')) as data_file:
		enter_list = json.load(data_file)
	print(enter_list)
	result = {'note': []}
	return result


if __name__ == '__main__':
	nsx_file = TEST_NSX if TEST_NSX else get_nsx_file_name()
	nsx_file = abs_path(nsx_file)
	tmp_folder = abs_path('tmp')
	result_folder = abs_path('result')

	unzip_nsx(nsx_file, tmp_folder)
	content = load_folder_content(tmp_folder)
	# render_html(content, result_folder)