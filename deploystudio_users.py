#!/bin/python
# -*- coding: UTF-8 -*-
# insert users deploy studio
from os.path import join, isdir, exists
from os import path, listdir
import argparse
import sys

new_user_code = "\t<key>dstudio-users</key>\n\
	<array>\n\
		\t<dict>\n\
			\t\t<key>dstudio-user-admin-status</key>\n\
			\t\t<string>YES</string>\n\
			\t\t<key>dstudio-user-hidden-status</key>\n\
			\t\t<string>NO</string>\n\
			\t\t<key>dstudio-user-name</key>\n\
			\t\t<string>{0}</string>\n\
			\t\t<key>dstudio-user-password</key>\n\
			\t\t<string>{2}</string>\n\
			\t\t<key>dstudio-user-shortname</key>\n\
			\t\t<string>{1}</string>\n\
		\t</dict>\n\
	</array>\n"

valid_header_options = ["yes", "y", "no", "n"]


print "************************************"
print "* Laptop Mass User Creation Script *"
print "*       for DeployStudio           *"
print "*                                  *"
print "* Created by: Cian Byrne 2016 (c)  *"
print "************************************"
def main():
    #
    #   Files to Import
    #
    #   Change these here to the file you need.
    #

    parser = argparse.ArgumentParser(description='Insert users into DeployStudio installation.')
    parser.add_argument("-r", "--repo", type=str, nargs=1, required=True,
                   help="The path to the root of your DeployStudio repository location. E.G. /Users/Shared/repository")
    parser.add_argument("-f", "--file", type=str, nargs=1, required=True,
                   help="The full path to the CSV file containing usernames.  E.G. ~/Desktop/usernames.csv")
    parser.add_argument("-H", "--header", type=str, nargs=1, required=True,
                   help="Does the provided file contain headers? (y or n)")

    args = parser.parse_args()

    # file with usernames and serial numbers
    #  FORMAT:  Serial Number, Name, Short Name, Password
    #
    #  NOTE:  'Name'        is what is displayed to the user.
    #         'Short Name'  is what is used for authentication and home directory.
    #
    if args.file:
        user_file_path = args.file[0]
        # check that file exists: 
        if exists(user_file_path):
            pass
        else:
            print "CSV file does not exists.  Please try again."
            sys.exit()

    # change this option if you are running this file other than in the folder
    #  with the .plist files in it.
    if args.repo:
        # check that the repo directory exists and is real
        deploystudio_path = join(args.repo[0], "Databases", "ByHost")
        if isdir(deploystudio_path):
            pass
        else:
            print "Invalid DeployStudio path.  Please try again."
            sys.exit()

    # change this option if your file has headers...
    if args.header:
        user_file_header = args.header[0]
        if user_file_header in valid_header_options:
            if user_file_header == "yes" or "y":
                user_file_header = True
            else:
                user_file_header = False
        else:
            print "Invalid header option.  Please try again."
            sys.exit()

    #
    #   Openning Required Files
    #
    print "Getting file...{0}".format(user_file_path)
    user_file = open(user_file_path, 'r')
    print "Beginning process..."

    # initialise variables...
    usernames = {}
    row = 0

    # load all serial numbers and usernames into dict
    for line in user_file:
        if row == 0 and user_file_header:
            # skip top row
            row += 1
        else:
            # parse line of input... FORMAT:  Serial Number, Name, Short Name, Password
            line = line.split(',')
            usernames[line[0]] = {'name' : line[1], 'shortname' : line[2], 'password' : line[3].strip("\n") }
            row += 1

    row = 0
    # grab the file and unpack it.
    for sn in usernames:
        try:
            # open .plist file...
            plist_file = open(join(deploystudio_path,'{0}.plist'.format(sn)))

            # read .plist file...
            contents = plist_file.readlines()

            # close .plist file...
            plist_file.close()

            # find if a user is already added...
            search_flag = True
            for line in contents:
                # then skip / do nothing...
                if 'dstudio-users' in line:
                    search_flag = False
                    print "{0} already has a user!".format(sn)

            # no user is in file, insert one from the imported file.
            if search_flag:
                # insert settings for users...
                contents.insert(-2, new_user_code.format(usernames[sn]['name'], usernames[sn]['shortname'],
                                                         usernames[sn]['password']))

                # open the .plist file
                plist_file = open(join(deploystudio_path,'{0}.plist'.format(sn)),'w')

                # insert the string (above) with username...
                for line in contents:
                    plist_file.write(line)

                # close the .plist file...
                plist_file.close()

                # report back that a record has been inserted...
                print "RECORD INSERTED!"
                row++

        except IOError:
            # triggered because the file does not exist.
            print "ERROR: {0}.plist cannot be found".format(sn)
            continue
        

    print "There were {0} records modified.".format(row)

    print "PROGRAM COMPLETE SUCCESSFULLY!"




if __name__ == '__main__':
    main()
