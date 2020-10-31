#!/usr/bin/env python
import os
import pandas as pd
import csv
import ast
import subprocess
from multiprocessing import Pool
from os import path
from csv import reader
from datetime import datetime
import time
import shutil
import sys

import json

def Encode_list(a):
	b = []
	for l in a:
		b.append(l.decode("utf-8"))
	return b # <-- Moved outside the for loop now
	

#done
def write_results (row, out):
	with open(out, "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(row)
		
#done
def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
  

#done
def get_all_files(fileName):
	lineList = [line.rstrip('\n') for line in open(fileName)]

	return lineList

#done
def search_dvc_files(list):

	match_dvc = [k for k in list if '.dvc' in k]
	return match_dvc


def languistic(path):
	lang = ""
	p1 = subprocess.Popen(['github-linguist', path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p2 = subprocess.Popen(['grep', 'language'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	match_f = p2.communicate()[0]
	p_status = p2.wait()
	
	if match_f:
		lang = match_f.decode("utf-8").rstrip('\r\n').split(':')[1].rstrip('\r\n').strip()

	return lang

#done
def checkout (commit):
	p=subprocess.Popen(['git', 'checkout', '-f', commit, '--quiet'])
	p_status = p.wait()

#done
def checkout_master ():
	p=subprocess.Popen(['git', 'checkout', '-f', 'master', '--quiet'])
	p_status = p.wait()


#done
def get_extension(file):
	filename, extension = os.path.splitext(file)
	return extension, filename

#done
def get_all_files_extensions():
	list = get_all_files()
	list_extension = []
	for f in list:

		ext=get_extension(f)
		if ext not in list_extension:
			list_extension.append(ext)
	return list_extension


#from these files search for commits that touches these files

####################################################################################
def get_last_churn(file):
	#git log -n 2 --pretty=format:%H
	
	p1 = subprocess.Popen(['git', 'log', '-n', '2', '--pretty=format:%H', '--', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p2 = subprocess.Popen(['tail', '-1'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	match_f = p2.communicate()[0].decode("utf-8")
	p_status = p2.wait()

	return match_f
#done
def search_files_extension(list, extensions_source, extension_other, DVC_file,programming_name, ignore, ignore_path):
	files = []
	others = []
	unknown = []
	dvc_suite = []
	for f in list:
		ext, source_s=get_extension(f)
		source = source_s.split("/")[-1]

		if ignore_path[0] in source_s:
			others.append(f)
		elif ignore_path[1] in source_s:
			others.append(f)
		

		elif source in programming_name:
			files.append(f)
			# print (source,ext)
		elif source in DVC_file:
			dvc_suite.append(f)
		elif source in ignore:
			# print (source,ext)
			others.append(f)
		elif source in ignore:
			others.append(f)
		elif ext in extensions_source:
			files.append(f)
		elif ext in extension_other:
			others.append(f)

		# elif ext == "":
		# 	if source in DVC_file:
		# 		dvc_suite.append(f)
			# elif source in ignore:
			# 	others.append(f)
			# elif source in programming_name:
			# 	files.append(f)

		else:
			unknown.append(f)

	return files, others, unknown, dvc_suite

###################################################################################
def get_files_type_tool(list):
	dic = {}
	
	for file in list:
		checkout_master()
		commit = get_last_churn(file)
		# print (file, commit)
		if not commit:
			continue
		# ext = get_extension (file)
		# # if ext == '':
		# # 	if 
		checkout (commit)
		language = languistic(file)
		if language:
			dic[file] = language
		# print (file, commit, language)
	# 	dic [file] = language
	return dic

		# if language == '':
		# 	others[file] = ""
		# else:
		# 	others[file] = language


		# if language in source_language:

	# return others


# as requested in comment
def get_date(commit):
	p1 = subprocess.Popen(['git', 'log', '--pretty=%at', commit, '-1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	match_f = p1.communicate()[0].decode("utf-8").rstrip('\r\n')
	p_status = p1.wait()
	# print (match_f)
	return match_f

def write_results (row, out):
	with open(out, "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(row)

def write_list_in_file(list, file):
	with open(file, 'w') as f:
	    for item in list:
	        f.write("%s\n" % item)

def filter_first_date(date, data_file):
	list_return = []
	for c in data_file:
		date_c  = get_date(c)
		print (date_c)
		difference = int (date_c) - int(date)
		if difference >= 0:
			# print (c, date_c)
			list_return.append(c)
		# else:
			# print (c)
		# print (c, date_c)

	return list_return


# l= languistic("/home/amine/Documents/DVC_project/sources/INTRUDE-refactor/.ipynb_checkpoints/INTRUDE-refactor-checkpoint.ipynb")
# print (l)
if __name__ == '__main__':
	target = "pipeline_file"
	path_sources = '/home/amine/Documents/DVC_project/stats/stats_files_classification2.csv'
	investigation_output = "/home/amine/Documents/DVC_project/coupling_result/investigation/coupling_"+target+".csv"

	
	output = "/home/amine/Documents/DVC_project/coupling_result/coupling_"+target+".csv"
	header = ['project','gitignore=>DVC_data','DVC_data=>gitignore', 'data=>DVC_data','DVC_data=>data','Source=>DVC_data','DVC_data=>source','test=>DVC_data',\
	'DVC_data=>test','others=>DVC_data','DVC_data=>others']
	# res = [proj, coupl_data_dvc, coupl_dvc_data, coupl_source_dvc, coupl_dvc_source, coupl_test_dvc, coupl_dvc_test, coupl_other_dvc, coupl_dvc_other]
	if os.path.exists(investigation_output):
		os.remove(investigation_output)
	if os.path.exists(output):
		os.remove(output)
	write_results (header, output)
	write_results (header, investigation_output)
	df = pd.read_csv(path_sources)

	path_to_repository = sys.argv[1]
	for index, row in df.iterrows():


		proj = str(row['project_name'])
		folder_name = str(row['folder_name'])
		print (proj)
		first_dvc = str(row['first_dvc_commit'])
		first_dvc_date = str(row['date_first_dvc'])

		path_rep = "/dataset/"+folder_name+".csv"

		source = path_to_repository+"/"+folder_name
		os.chdir(source)
		checkout_master()

		with open(path_rep, 'r') as read_obj:
			reader = csv.reader(read_obj)
			for row in reader:
				if row[0] == "source_file":
					files_source = ast.literal_eval(row[1])
				
				if row[0] == "data_file":
					data_file = ast.literal_eval(row[1])

				if row[0] == "test_file":
					test_file = ast.literal_eval(row[1])
					
				if row[0] == "dvc_"+target:
					dvc_file = ast.literal_eval(row[1])
					

				if row[0] == "other_file":
					other_file = ast.literal_eval(row[1])

				if row[0] == "gitignore_file":
					gitignore_file = ast.literal_eval(row[1])
					
		#coupling 
		
		# print (data_file)
		#coupling 
		gitignore_file= filter_first_date(first_dvc_date, gitignore_file)

		files_source= filter_first_date(first_dvc_date, files_source)
		# print (files_source)
		data_file=filter_first_date(first_dvc_date, data_file)
		test_file=filter_first_date(first_dvc_date, test_file)
		dvc_file=filter_first_date(first_dvc_date, dvc_file)
		other_file=filter_first_date(first_dvc_date, other_file)

		coupl_git_dvc=0
		coupl_dvc_git=0
		coupl_data_dvc=0
		coupl_dvc_data=0

		coupl_source_dvc=0
		coupl_dvc_source=0
		coupl_test_dvc=0
		coupl_dvc_test=0
		coupl_other_dvc=0
		coupl_dvc_other=0

		coupl_git_dvc_in=[]
		coupl_dvc_git_in=[]
		coupl_data_dvc_in=[]
		
		coupl_dvc_data_in=[]

		coupl_source_dvc_in=[]
		coupl_dvc_source_in=[]
		coupl_test_dvc_in=[]
		coupl_dvc_test_in=[]
		coupl_other_dvc_in=[]
		coupl_dvc_other_in=[]

		if gitignore_file:
			tot = len(gitignore_file)
			coupl=0
			for gitignore in gitignore_file:

				if gitignore in dvc_file:
					coupl_git_dvc_in.append(gitignore)
					coupl+=1
			coupl_git_dvc = (coupl/tot)*100
			######################################
		else:
			coupl_git_dvc = "-"

		if dvc_file:
			tot = len(dvc_file)
			coupl=0
			for dvc in dvc_file:

				if dvc in gitignore_file:
					coupl_dvc_git_in.append(dvc)
					coupl+=1
			coupl_dvc_git = (coupl/tot)*100
			######################################
		else:
			coupl_dvc_git = "-"

		if data_file:
			tot = len(data_file)
			coupl=0
			for data in data_file:

				if data in dvc_file:
					coupl_data_dvc_in.append(data)
					coupl+=1
			coupl_data_dvc = (coupl/tot)*100
			######################################
		else:
			coupl_data_dvc = "-"
		if dvc_file:
			tot = len(dvc_file)
			coupl=0
			for dvc in dvc_file:

				if dvc in data_file:
					coupl_dvc_data_in.append(dvc)
					coupl+=1
			coupl_dvc_data = (coupl/tot)*100
		else:
			
			coupl_dvc_data = "-"



		if files_source:
			tot = len(files_source)
			coupl=0
			for source in files_source:

				if source in dvc_file:
					coupl_source_dvc_in.append(source)
					coupl+=1
			coupl_source_dvc = (coupl/tot)*100
			######################################
		else:
			coupl_source_dvc = "-"
		if dvc_file:
			tot = len(dvc_file)
			coupl=0
			for dvc in dvc_file:

				if dvc in files_source:
					coupl_dvc_source_in.append(dvc)
					coupl+=1
			coupl_dvc_source = (coupl/tot)*100
		else:
			
			coupl_dvc_source = "-"
		######################################
		if test_file:
			tot = len(test_file)
			coupl=0
			for test in test_file:

				if test in dvc_file:
					coupl_test_dvc_in.append(test)
					coupl+=1
			coupl_test_dvc = (coupl/tot)*100
			######################################
		else:
			coupl_test_dvc = "-"
		
		if dvc_file:	
			tot = len(dvc_file)
			coupl=0
			for dvc in dvc_file:

				if dvc in test_file:
					coupl_dvc_test_in.append(dvc)
					coupl+=1
			coupl_dvc_test = (coupl/tot)*100
		else:
			
			coupl_dvc_test = "-"
		######################################
		if other_file:
			tot = len(other_file)
			coupl=0
			for other in other_file:

				if other in dvc_file:
					coupl_other_dvc_in.append(other)
					coupl+=1
			coupl_other_dvc = (coupl/tot)*100
			######################################
		else:
			coupl_other_dvc = "-"
		if dvc_file:
			tot = len(dvc_file)
			coupl=0
			for dvc in dvc_file:

				if dvc in other_file:
					coupl_dvc_other_in.append(dvc)
					coupl+=1
			coupl_dvc_other = (coupl/tot)*100
		else:
			
			coupl_dvc_other = "-"


		res_in =[folder_name, coupl_git_dvc_in, coupl_dvc_git_in, coupl_data_dvc_in, coupl_dvc_data_in, coupl_source_dvc_in, coupl_dvc_source_in, coupl_test_dvc_in, coupl_dvc_test_in, coupl_other_dvc_in, coupl_dvc_other_in]
		
		res = [folder_name, coupl_git_dvc, coupl_dvc_git, coupl_data_dvc, coupl_dvc_data, coupl_source_dvc, coupl_dvc_source, coupl_test_dvc, coupl_dvc_test, coupl_other_dvc, coupl_dvc_other]
		write_results (res, output)
		write_results (res_in, investigation_output)
				# row[0]
			# for cnt, line in enumerate(read_obj):
			# 	newline = line.rstrip('\r\n')
			# 	print (newline)



		# df_data = pd.read_csv(path_rep)
		# df_tr = df_data.T
		# # print (df_tr)
		# # new_header = df_tr.iloc[0] #grab the first row for the header
		# # print (new_header)
		# # df_tr = df_tr[0:] #take the data less the header row
		# # df_tr.columns = new_header
		# df_tr.to_csv(out,index=False)
		# print (df_tr)
		# for index, a in df_tr.iterrows():
			
		# 	files_source = ast.literal_eval(a['source_file'])
		# 	test_file = ast.literal_eval(a['test_file'])
		# 	dvc_file = ast.literal_eval(a['dvc_file'])
		# 	other_file = ast.literal_eval(a['other_file'])

		# 	print (files_source)



		# print (dic)
		# source_files_tool, other_files_tool = get_files_type_tool(list_all_files)


		# source_test_files = search_source_test_files_tool(list_all_files)

		


		# test_files = search_test_files(list_all_files)
		# list_all_files = Diff(list_all_files , test_files)
		
		# source_files_extension = search_source_files_extension(list_all_files)
		# list_all_files = list_all_files - source_files_extension

		# source_files_tool = search_source_files_tool(list_all_files)
		# other_files = list_all_files - source_files_tool





