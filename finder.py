import os

#This script will discover how many times each command specified in
#comands.cfg are used in the test suite

#a list of all possible command names
command_dict = dict()

#read in the file that has all the CMD ins them
commands_file = open('usr/src/test/zfs-tests/include/commands.cfg')
for line in commands_file:
	if 'export' in line:
		#the lines are formated
		#export NAME="path"
		#so I want the part beteinxt the space and the =
		command_name = '$' + line[line.index(' ')+1:line.index('=')]
		command_dict[command_name] = 0

print command_dict

#now walk the enitre ZFS project tree and find refernces
for root, dirs, files in os.walk('usr/src/test/zfs-tests'):
	for file_name in files:
		print "looking at" + file_name
		file_path = os.path.join(root, file_name)
		project_file = open(file_path)
		for line in project_file:
			for command in command_dict:
				if command in line:
					command_dict[command] = command_dict[command] + 1

print command_dict
