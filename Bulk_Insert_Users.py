#!/usr/bin/python
# Author(s): Ian Lawrence <ian@codezon.com>
# License: MIT
# Copyright (C) 2012 Ian Lawrence

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Version 1 - Proof of concept script to input bulk users to NDG. Do not let this anywhere near a live server yet as there is no input
# sanitation or error handling and you will regret it
# Version 2 - Added md5 hashing


import sys
import csv
import MySQLdb
import hashlib


def main():

	if len(sys.argv) < 2:
		print "Usage: Bulk_Insert_Users.py <csv_file>"
		exit(1)

	# Get connection parameters
	mydb = MySQLdb.connect (host = "localhost" ,user = "ndg", passwd = "",db = "")
	cursor = mydb.cursor()

	# Open the CSV file for reading
	reader = csv.reader(open(sys.argv[1]))

	# Add the role the users will have
	ndg_role_role_name = "Operator"

	for row in reader: # Read a single row from the CSV file
		        mylist = []
		        for column in row: # Read a single column
		            mylist.append("%s" % (column,)) # append the individual variables to be inserted
		            
		        print mylist
		            
		        area_code = mylist[0]
		        country_code = mylist[1]
		        email = mylist[2] 
		        email_preferences = mylist[3] 
		        first_name = mylist[4]  
		        has_full_permissions = mylist[5] 
		        last_name = mylist[6] 
		        password = mylist[7] 
		        phone_number = mylist[8] 
		        user_admin = mylist[9] 
		        user_validated = mylist[10] 
		        username = mylist[11] 
		        validation_key = mylist[12] 
		        company_id = mylist[13] 
		        ndg_group_id = mylist[14]
		        
		        hasher = hashlib.md5()
		        hasher.update(username)
		        hasher.update(":NDG:")
		        hasher.update(password)
		        md5hash = hasher.hexdigest()
		
		        sql = "INSERT INTO `ndg_user` (`area_code`, `country_code`, `email`, `email_preferences`, `first_name`, `has_full_permissions`, `last_name`, `password`, `phone_number`, `user_admin`, `user_validated`, `username`, `validation_key`, `company_id`, `ndg_group_id`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (area_code,country_code,email,email_preferences,first_name,has_full_permissions,last_name,md5hash,phone_number,user_admin,user_validated,username,validation_key,company_id,ndg_group_id)
		        sql1 = "INSERT INTO user_role (`ndg_role_role_name`, `username`) VALUES ('%s','%s')" % (ndg_role_role_name,username)
		        try:
		            # Execute the SQL commands
		            cursor.execute(sql)
		            cursor.execute(sql1) 
		                        
		            # Get a beer...we did it \o/
		            mydb.commit()

		        except mydb.Error, e:

		            # damn, what happened
		            print "Error %d: %s" % (e.args[0],e.args[1])

		            # Rollback dude
		            mydb.rollback()
		            sys.exit(1)

	# disconnect from server
	mydb.close()
	exit(0)

if __name__ == "__main__":
    main()
