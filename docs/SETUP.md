1.Download Local application, and set up a new local WordPress site named lifepaws.

2.Open site in browser, and log in admin account in WP Admin dashboard.

3.Install All in one WP Migration plugin 
3.1 First, I manually placed the .wpress backup file into the wp-content/ai1wm-backups/ directory of the local site. However, the import was blocked due to the file size limit restriction. 
3.2 I attempted to increase the upload limit via wp-config.php and plugin config files(constants.php), but it didn't take effect. Eventually, I found a modified version of the All-in-One WP Migration plugin from GitHub, which successfully enabled me to upload the 300MB wpress file..

4.After successfully importing the .wpress backup, the original admin credentials were no longer valid, likely because the backup overwrote the users table.

5.So I used WordPress CLI via the Site Shell to locate the existing user and reset the password:
wp user list --fields=ID,user_login,user_email,roles  //check current user
wp user update intern_test --user_pass='NewPwd'       //reset password
wp user set-role intern_test administrator            //set intern_test as administrator

6.After logging in, I went to Settings page and clicked Save Changes twice to flush rewrite rules and fix permalink issue.

7.Finally, I reviewed the site content and confirmed that media files and homepage were successfully restored.