#!/usr/bin/python3
# -*- coding:utf8 -*-

import os
import sys
import shutil
import zipfile
import json
from glob import iglob
import lxml.html as html

TEST_NSX = ''


# helper
def join_path(path1, path2):
	return os.path.join(path1, path2)

def abs_path(relevant_path):
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), relevant_path)

def new_folder(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)

def delete_folder(folder):
	shutil.rmtree(folder, ignore_errors=True)

def copy_files(src_glob, dst_folder):
	for fname in iglob(src_glob):
		shutil.copy(fname, dst_folder)


def get_content(file):
	with open(file, 'r') as f:
		c = f.read()
	return c

def get_nsx_file_name():
	assert len(sys.argv) == 2
	return sys.argv[1]


# process

def unzip_nsx(nsx_file, unzip_folder):
	delete_folder(unzip_folder)
	new_folder(unzip_folder)
	zip_ref = zipfile.ZipFile(nsx_file, 'r')
	zip_ref.extractall(unzip_folder)
	zip_ref.close()


def load_folder_content(folder):
	with open(join_path(folder, 'config.json')) as data_file:
		enter = json.load(data_file)
	# get ids
	ids_list = []
	for key in ['note', 'notebook']:
		ids_list += enter[key]
	for key in ['id', 'stack', 'tag']:
		ids_list += enter['shortcut'][key]
	ids = list(set(ids_list))
	# get content
	contents = {}
	for cid in ids:
		file = join_path(folder, cid)
		if os.path.isfile(file):
			with open(file, encoding='utf8') as data_file:
				contents[cid] = json.load(data_file)
	return contents


def process_content_attachment(tmp_folder, content, attachment_folder):
	for nkey, note in content.items():
		if 'attachment' in note:
			attachments = note['attachment']
			for akey, attach in attachments.items():
				att_src = join_path(tmp_folder, 'file_' + attach['md5'])
				att_dst = join_path(attachment_folder, attach['md5'] + '_' + attach['name'])
				shutil.move(att_src, att_dst)
	return


def render_result(tmp_folder, result_folder):
	content = load_folder_content(tmp_folder)
	attachment_folder = join_path(result_folder, 'attachment')
	delete_folder(result_folder)
	new_folder(result_folder)
	new_folder(attachment_folder)
	# copy templates
	templates_join = lambda file: join_path(abs_path('templates'), file)
	copy_files(templates_join('*.html'), result_folder)
	copy_files(templates_join('*.js'), result_folder)
	# copy attachment
	process_content_attachment(tmp_folder, content, attachment_folder)
	# config.json
	config_file = join_path(result_folder, 'config.json')
	with open(config_file, 'w+') as outputfile:
		outputfile.write('CONFIG = ' + get_content(join_path(tmp_folder, 'config.json')))
	# contents.json
	output = join_path(result_folder, 'contents.json')
	with open(output, 'w+', encoding='utf8') as outfile:
		outfile.write('CONTENTS = ' + json.dumps(content, ensure_ascii=False))


if __name__ == '__main__':
	nsx_file = TEST_NSX if TEST_NSX else get_nsx_file_name()
	tmp_folder = abs_path('tmp')
	result_folder = abs_path('result')

	unzip_nsx(nsx_file, tmp_folder)
	render_result(tmp_folder, result_folder)
	delete_folder(tmp_folder)
	print('Done. Open result folder and browse index.html')