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
		command_name = line[line.index(' ')+1:line.index('=')]
		#when looking at each line, you are looking for the command
		#it will have $ before it, and either ' ', '{', or '}' after
		#it
		command_name = '$' + command_name
		command_dict[command_name] = 0

#return 1 if this command is in the line, 0 otherwise
def command_count(command, line):
	#get the character directly after the command to see that it is
	#ACTUALLY a call, and no just a fake
	index_of_command = line.index(command)
	length_of_command = len(command)
	location_of_command_end = index_of_command + length_of_command
	character_after_command = line[location_of_command_end:location_of_command_end+1]
	#we think that if there is a space, an open curly bracket, or a close
	#curly bracket, then this is a valid calls
	if character_after_command in "\"\n {}`');":
		return 1
	else:
		return 0


#now walk the enitre ZFS project tree and find refernces
for root, dirs, files in os.walk('usr/src/test/zfs-tests'):
	for file_name in files:
		file_path = os.path.join(root, file_name)
		project_file = open(file_path)
		for line in project_file:
			for command in command_dict:
				if command in line:
					count = command_count(command, line)
					command_dict[command] = command_dict[command] + count

print "\n\n"
pad_number = 15
for command in command_dict:
	print command.ljust(pad_number) + str(command_dict[command]).rjust(3)
