import os

#This script will discover how many times each command specified in
#comands.cfg are used in the zfs test suite

#a list of all possible command names
command_dict = dict()

#read in the file that has all the CMD ins them
commands_file = open('usr/src/test/zfs-tests/include/commands.cfg')
for line in commands_file:
	if 'export' in line:
		#the lines are formated
		#export NAME="path"
		#so I want the part betwinxt the space and the =
		command_name = line[line.index(' ')+1:line.index('=')]
		#when looking at each line, you are looking for the command
		#it will have $ before it
		command_name = '$' + command_name
		#initialize its count to 0
		command_dict[command_name] = 0

#return 1 if this command is in the line, 0 otherwise
def command_count(command, line):
	#get the character directly after the command to see that it is
	#ACTUALLY a call, and not a false positive. A false positive would
	#be when the script has a variable like $FILEDIST, since one of the
	#commands is $FILE.
	index_of_command = line.index(command)
	length_of_command = len(command)
	location_of_command_end = index_of_command + length_of_command
	character_after_command = line[location_of_command_end:location_of_command_end+1]
	#here we give the set of acceptable characters to come after a command
	#and still consider it an actual command call
	if character_after_command in "\"\n {}`');":
		return 1
	else:
		return 0


#walk the entire zfs-test tree, passing any references that are found to
#command_count
for root, dirs, files in os.walk('usr/src/test/zfs-tests'):
	for file_name in files:
		file_path = os.path.join(root, file_name)
		project_file = open(file_path)
		for line in project_file:
			for command in command_dict:
				if command in line:
					count = command_count(command, line)
					command_dict[command] = command_dict[command] + count

#hooray stack overflow! This sorts the dict by its values
from operator import itemgetter
sorted_dict = sorted(command_dict.items(), key=itemgetter(1))

#go through the now sorted list and print it
for command,count in sorted_dict:
	print command.ljust(15) + str(count).rjust(3)
