#!/usr/bin/python

import urllib
import urllib2
import json
import sys

# check for proper usage/invocation
if len(sys.argv) < 2:
	usage()

# vars
projects_url='https://todoist.com/API/getProjects'
add_url='https://todoist.com/API/addItem'
token="<your_token_here>"
project_name = sys.argv[1]
task_name = " ".join(sys.argv[2:])

# function to print usage instructions & bail on errcode 1
def usage():
	print "addToProject.py: project_name task_name"
	exit(1)

# function to get all projects and return a hash of project_name:project_id 
def getProjects() :
	# API Call
	values = {'token' : token}
	req = urllib2.Request(projects_url, urllib.urlencode(values))
	resp = urllib2.urlopen(req)

	# parse response from API and decode JSON guff
	page = resp.read()
	decoded = json.loads(page)

	# create a hash of project name:id mappings and return
	project_dict = {}

	for project in decoded:
		project_dict[project['name']] =  str(project['id'])
	
	return project_dict

# function call to add a task to a project
def addTask(id, task):
	# API Call Setup : default priority of 3
	values = {'token' : token, 'project_id' : id, 'priority' : 3, 'content' : task}
	# Encode data and make API call
	req = urllib2.Request(add_url, urllib.urlencode(values))
	resp = urllib2.urlopen(req)
	# Decode API response
	page = resp.read()
	decoded = json.loads(page)
	print "task id: " + str(decoded['id']) + " added on " + str(decoded['date_added'])


my_projects = getProjects()



# check and see if we have a valid project name ie does it exist on todoist  (case sensitive?)
if project_name in my_projects.keys():
	# get the project id for the add API call
	project_id = my_projects[project_name]
	# add the given task to the specified project
	addTask(project_id, task_name)
else:
	# we couldn't find the specified project - let's blow this facist popsicle stand
	print "project_name \"" + project_name + "\" not found!"
	print my_projects.keys()
	exit(1)


exit(0)