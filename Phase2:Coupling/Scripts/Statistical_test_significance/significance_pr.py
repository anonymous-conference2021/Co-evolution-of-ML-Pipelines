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
	p=subprocess.Popen(['git', 'checkout', commit, '--quiet'])
	p_status = p.wait()

#done
def checkout_master ():
	p=subprocess.Popen(['git', 'checkout', 'master', '--quiet'])
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
def get_commits_file (files_dvc):
	#git log --follow --pretty="%H:%cd" -- file
	list_commits = []
	
	for f in files_dvc:
		p1 = subprocess.Popen(['git', 'log', '--follow', '--pretty=%H', '--', f], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		match_f = p1.communicate()[0].splitlines()
		p_status = p1.wait()
		match_f = Encode_list(match_f)
		for i in match_f:
			if i not in  list_commits:
				list_commits.append(i)
				# print (i)
			
				
	return list_commits


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


		else:
			unknown.append(f)

	return files, others, unknown, dvc_suite

###################################################################################
def get_files_type_tool(list):
	dic = {}
	
	for file in list:
		checkout_master()
		commit = get_last_churn(file)

		if not commit:
			continue

		checkout (commit)
		language = languistic(file)
		if language:
			dic[file] = language

	return dic



def write_results (row, out):
	with open(out, "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(row)

def write_list_in_file(list, file):
	with open(file, 'w') as f:
	    for item in list:
	        f.write("%s\n" % item)

def merge_item(issues, da):
	# res = []
	res = []
	for s in da:
		for (k,i) in issues.items():
			if s in i:
				res.extend(i)
			else:
				res.append(s)
				
	res = list(set(res))

	return res


def get_date(commit):
	p1 = subprocess.Popen(['git', 'log', '--pretty=%at', commit, '-1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	match_f = p1.communicate()[0].decode("utf-8").rstrip('\r\n')
	p_status = p1.wait()
	# print (match_f)
	

	return match_f

def filter_first_date(list_commits, date):
	list_return = []
	for c in list_commits:
		date_c  = get_date(c)

		if date_c:
			difference = int (date_c) - date
			if difference > 0:

				list_return.append(c)


	return list_return

def filter_pr (date_prs, timestamp):
	list_pr =  []

	for key, value in date_prs.items():
		times_pr = time.mktime(time.strptime(value,"%Y-%m-%dT%H:%M:%SZ"))

		diff = times_pr - timestamp

		if diff >= 0:
			list_pr.append(key)

	return list_pr


if __name__ == '__main__':
	target = "data_file"
	no_target1 = "pipeline_file"
	no_target2 = "utilities"


	path_sources = '../../Pull_request_projects.csv'


	output = "output/coupling_item"+target+".csv"
	output_significance = "output/significance_item.csv"
	header = ['project','gitignore=>DVC_data','DVC_data=>gitignore', 'data=>DVC_data','DVC_data=>data','Source=>DVC_data','DVC_data=>source','test=>DVC_data',\
	'DVC_data=>test','others=>DVC_data','DVC_data=>others']


	if os.path.exists(output):
		os.remove(output)
	write_results (header, output)


	git_dvc = 0
	dvc_git = 0
	data_dvc = 0
	dvc_data = 0
	source_dvc = 0
	dvc_source = 0
	test_dvc = 0
	dvc_test = 0
	other_dvc = 0
	dvc_other = 0


	path_to_repository = sys.argv[1]

	df = pd.read_csv(path_sources)
	for index, row in df.iterrows():


		proj = str(row['project_name'])
		folder_name = str(row['folder_name'])
		date_first_dvc = str(row['date_F_dvc'])
		pr_commits = ast.literal_eval(row["all_pr_commits"])
		date_prs = ast.literal_eval(row["date_prs"])
		print (proj)
		source = path_to_repository+"/"+folder_name
		os.chdir(source)
		checkout_master()
		import time
		timestamp = time.mktime(time.strptime(date_first_dvc, '%a %b %d %H:%M:%S %Y'))
		path_rep = "../../dataset/"+folder_name+".csv"


		list_pr_commits = filter_pr(date_prs, timestamp)
		pr_finals = {}
		for key, value in pr_commits.items():
			if key in list_pr_commits:
				pr_finals[key] = value


		print (date_prs.keys(), list_pr_commits)


		with open(path_rep, 'r') as read_obj:
			reader = csv.reader(read_obj)
			for row in reader:
				if row[0] == "source_file":
					files_source_ = ast.literal_eval(row[1])
				
				if row[0] == "data_file":
					data_file_ = ast.literal_eval(row[1])

				if row[0] == "test_file":
					test_file_ = ast.literal_eval(row[1])
					
				if row[0] == "dvc_"+target:
					dvc_file_ = ast.literal_eval(row[1])
				if row[0] == "dvc_"+no_target1:
					dvc_file_no_target1 = ast.literal_eval(row[1])
				
				if row[0] == "dvc_"+no_target2:
					dvc_file_no_target2 = ast.literal_eval(row[1])

				if row[0] == "other_file":
					other_file_ = ast.literal_eval(row[1])

				if row[0] == "gitignore_file":
					gitignore_file_ = ast.literal_eval(row[1])


		gitignore_file= merge_item(pr_finals, gitignore_file_)

		files_source= merge_item(pr_finals, files_source_)


		data_file=merge_item(pr_finals, data_file_)
		test_file=merge_item(pr_finals, files_source_)
		dvc_file=merge_item(pr_finals, dvc_file_)
		other_file=merge_item(pr_finals, other_file_)


		n=len(list_pr_commits)
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


		set_dvc = set(dvc_file)
		set_git = set(gitignore_file)
		set_data = set(data_file)
		set_source = set(files_source)
		set_test = set(test_file)
		set_others = set(other_file)
		
		comm_git_dvc = len(list(set_dvc.intersection(gitignore_file)))
		comm_data_dvc = len(list(set_dvc.intersection(data_file)))
		comm_source_dvc = len(list(set_dvc.intersection(files_source)))
		comm_test_dvc = len(list(set_dvc.intersection(test_file)))
		comm_other_dvc = len(list(set_dvc.intersection(other_file)))


		if comm_git_dvc != 0:
			supp_dvc = len (dvc_file) / n
			supp_git = len (gitignore_file) / n
			supp_git_dvc = supp_dvc_git = comm_git_dvc/n
			conf_git_dvc = supp_git_dvc / supp_git
			conf_dvc_git = supp_dvc_git / supp_dvc
			lift_git_dvc = lift_dvc_git = supp_git_dvc / (supp_dvc*supp_git)

			if ((conf_git_dvc-supp_git_dvc)*(lift_git_dvc - conf_git_dvc)) != 0:
				coupl_git_dvc = n * (lift_git_dvc-1)**2 * ((supp_git_dvc * conf_git_dvc)/((conf_git_dvc-supp_git_dvc)*(lift_git_dvc - conf_git_dvc)))
				if coupl_git_dvc > 3.84146:
					git_dvc+=1
			else:
				coupl_git_dvc="-"
			if (conf_dvc_git-supp_dvc_git)*(lift_dvc_git - conf_dvc_git) !=0:
				coupl_dvc_git = n * (lift_dvc_git-1)**2 * ((supp_dvc_git * conf_dvc_git)/((conf_dvc_git-supp_dvc_git)*(lift_dvc_git - conf_dvc_git)))
				if coupl_dvc_git> 3.84146:
					dvc_git+=1
			else:
				coupl_dvc_git="-"
		else:
			coupl_git_dvc=coupl_dvc_git="-"

		if (comm_data_dvc != 0):

			supp_data = len (data_file) / n
			supp_dvc = len (dvc_file) / n
			supp_data_dvc = supp_dvc_data = comm_data_dvc/n
			conf_data_dvc = supp_data_dvc / supp_data
			conf_dvc_data = supp_data_dvc / supp_dvc

			lift_data_dvc = lift_dvc_data = supp_data_dvc / (supp_dvc*supp_data)
			if (conf_data_dvc-supp_data_dvc)*(lift_data_dvc - conf_data_dvc) != 0:
				coupl_data_dvc = n * (lift_data_dvc-1)**2 * ((supp_data_dvc * conf_data_dvc)/((conf_data_dvc-supp_data_dvc)*(lift_data_dvc - conf_data_dvc)))
				if coupl_data_dvc>3.84146:
					data_dvc+=1
			else:
				coupl_data_dvc = "-"
			if (conf_dvc_data-supp_dvc_data)*(lift_dvc_data - conf_dvc_data) != 0:
				coupl_dvc_data = n * (lift_dvc_data-1)**2 * ((supp_dvc_data * conf_dvc_data)/((conf_dvc_data-supp_dvc_data)*(lift_dvc_data - conf_dvc_data)))
				if coupl_dvc_data > 3.84146:
					dvc_data+=1
			else:
				coupl_dvc_data = "-"
		else:
			coupl_dvc_data =coupl_dvc_data ="-"


		if comm_source_dvc != 0:

			supp_source = len (files_source) / n
			supp_dvc = len (dvc_file) / n
			supp_dvc_source = supp_source_dvc = comm_source_dvc/n
			conf_source_dvc = supp_dvc_source / supp_source
			conf_dvc_source = supp_dvc_source / supp_dvc

			lift_source_dvc = lift_dvc_source = supp_source_dvc / (supp_dvc*supp_source)
			if (conf_source_dvc-supp_source_dvc)*(lift_source_dvc - conf_source_dvc) !=0:
				coupl_source_dvc = n * (lift_source_dvc-1)**2 * ((supp_source_dvc * conf_source_dvc)/((conf_source_dvc-supp_source_dvc)*(lift_source_dvc - conf_source_dvc)))
				if coupl_source_dvc>3.84146:
					source_dvc+=1
			else:
				coupl_source_dvc="-"
			if (conf_dvc_source-supp_dvc_source)*(lift_dvc_source - conf_dvc_source) != 0:
				coupl_dvc_source = n * (lift_dvc_source-1)**2 * ((supp_dvc_source * conf_dvc_source)/((conf_dvc_source-supp_dvc_source)*(lift_dvc_source - conf_dvc_source)))
				if coupl_dvc_source>3.84146:
					dvc_source+=1
			else:
				coupl_dvc_source=""
		else:
			coupl_source_dvc=coupl_dvc_source ="-"


		if comm_test_dvc != 0:


			supp_test = len (test_file) / n
			supp_dvc = len (dvc_file) / n
			supp_test_dvc = supp_dvc_test = comm_test_dvc/n
			conf_test_dvc = supp_test_dvc / supp_test
			conf_dvc_test = supp_test_dvc / supp_dvc

			lift_test_dvc = lift_dvc_test = supp_dvc_test / (supp_dvc*supp_test)
			if (conf_test_dvc-supp_test_dvc)*(lift_test_dvc - conf_test_dvc)!=0:
				coupl_test_dvc = n * (lift_test_dvc-1)**2 * ((supp_test_dvc * conf_test_dvc)/((conf_test_dvc-supp_test_dvc)*(lift_test_dvc - conf_test_dvc)))
				if coupl_test_dvc>3.84146:
					test_dvc+=1
			else:
				coupl_test_dvc=""
			if (conf_dvc_test-supp_dvc_test)*(lift_dvc_test - conf_dvc_test) !=0:
				coupl_dvc_test = n * (lift_dvc_test-1)**2 * ((supp_dvc_test * conf_dvc_test)/((conf_dvc_test-supp_dvc_test)*(lift_dvc_test - conf_dvc_test)))
				if coupl_dvc_test>3.84146:
					dvc_test+=1
			else:
				coupl_dvc_test="-"
		else:
			coupl_test_dvc = coupl_dvc_test = "-"


		if comm_other_dvc != 0:


			supp_other = len (other_file) / n
			supp_dvc = len (dvc_file) / n
			supp_other_dvc = supp_dvc_other = comm_other_dvc/n
			conf_other_dvc = supp_other_dvc / supp_other
			conf_dvc_other = supp_other_dvc / supp_dvc

			lift_dvc_other = lift_other_dvc = supp_dvc_other / (supp_dvc*supp_other)
			if (conf_other_dvc-supp_other_dvc)*(lift_other_dvc - conf_other_dvc)!=0:
				coupl_other_dvc = n * (lift_other_dvc-1)**2 * ((supp_other_dvc * conf_other_dvc)/((conf_other_dvc-supp_other_dvc)*(lift_other_dvc - conf_other_dvc)))
				if coupl_other_dvc>3.84146:
					other_dvc+=1
			else:
				coupl_other_dvc="-"
			if (conf_dvc_other-supp_dvc_other)*(lift_dvc_other - conf_dvc_other)!=0:
				coupl_dvc_other = n * (lift_dvc_other-1)**2 * ((supp_dvc_other * conf_dvc_other)/((conf_dvc_other-supp_dvc_other)*(lift_dvc_other - conf_dvc_other)))
				if coupl_dvc_other>3.84146:
					dvc_other+=1
			else:
				coupl_dvc_other="-"
		else:
			coupl_other_dvc=coupl_dvc_other="-"



		res = [folder_name, coupl_git_dvc, coupl_dvc_git, coupl_data_dvc, coupl_dvc_data, coupl_source_dvc, coupl_dvc_source, coupl_test_dvc, coupl_dvc_test, coupl_other_dvc, coupl_dvc_other]
		write_results (res, output)

	res_significance = [target, git_dvc, dvc_git, data_dvc, dvc_data, source_dvc, dvc_source, test_dvc, dvc_test, other_dvc, dvc_other]
	write_results (res_significance, output_significance)