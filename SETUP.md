# LifePaws IT Intern Test - Setup Documentation

## Environment
- Operating System: Windows 11  
- Tool: XAMPP (Apache + MySQL + PHP 8.2.12)  
- Database: MariaDB 10.4  
- WordPress: 6.x (downloaded from wordpress.org)  

---

# Installation & Setup Steps

## 1. Set Up Local Environment
1. Install and start XAMPP, enable Apache and MySQL.  
2. In phpMyAdmin (`http://localhost/phpmyadmin`), create a new database:  
   - Name: `wp_test`  
   - Collation: `utf8mb4_unicode_ci`  
3. Extract the downloaded `wordpress-6.8.2.wpress` into:  
4. Open `http://localhost/wordpress` in a browser and complete the setup:  
- Database Name: `wp_test`  
- Username: `root`  
- Password: (blank )  
- Host: `localhost`  

---

## 2. Install Plugin
1. Log in to the WordPress Admin dashboard → Plugins → Add New.  
2. Search for All-in-One WP Migration, install and activate it.  

---

## 3. Import Backup
1. Download `lifepaws-demo.wpress`.  
2. Go to All-in-One WP Migration → Import → Select `File`.  
3. Issue: Upload limit (40MB) error occurred.  

Solution:  
- Edit the plugin file `wp-content/plugins/all-in-one-wp-migration/constants.php`.  
- Locate:  
php
define( 'AI1WM_MAX_FILE_SIZE', 536870912 );
