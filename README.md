# INTRODUCTION #

This script allows administrators to import a large volume of users automatically into DeployStudio.  DeployStudio does not have this functionality in any version at the moment (v1.7.5), so this is the fastest way to import large numbers of users without having to manually input the required details.

This repo contains custom scripts to work with DeployStudio for Mac.

**IMPORTANT:**  Always remember to backup your DeployStudio repository/files before running this script.  Just in case ;).


# How it works #

The script works by reading in a csv file which contains user information and matching it to existing computers imported to Deploy Studio.  The csv file MUST contain the following fields in the correct order for the script to work correctly.


A template CSV file is provided in the samples/ folder.

```
#!bash
CSV Format:
Serial Number, Name, Short Name, Password 

```

**Serial Number** of the device being assigned to a user.

**Name** is what is displayed to the user.

**Short Name** is what is used for authentication and home directory.

**Password** the default password for this user when the device is given to them.


# How to use #

1. Clone repository
2. Create csv file with users and serial numbers
3. Run script


# Running the script #

You can run the script from any directory, provided you give it the correct DeployStudio repository directory in the command-line arguments.

## Example Usage ##
```

$ python deploystudio_users.py -r /Users/Shared/repository -f ~/Desktop/usernames.csv -H y

```

## Further Usage ##

```

$ python deploystudio_users.py -h

************************************
* Laptop Mass User Creation Script *
*       for DeployStudio           *
*                                  *
* Created by: Cian Byrne 2016 (c)  *
************************************
usage: deploystudio_users.py [-h] -r REPO -f FILE -H HEADER

Insert users into DeployStudio installation.

optional arguments:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  The path to the root of your DeployStudio repository
                        location. E.G. /Users/Shared/repository
  -f FILE, --file FILE  The full path to the CSV file containing usernames.
                        E.G. ~/Desktop/usernames.csv
  -H HEADER, --header HEADER
                        Does the provided file contain headers? (y or n)

```



### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
