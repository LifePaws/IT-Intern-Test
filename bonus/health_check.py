#!/usr/bin/env python3
"""
WordPress Health Check Script
Comprehensive health check for WordPress, MySQL, and phpMyAdmin services
"""

import subprocess
import sys
import requests
import time
import json
from datetime import datetime

def run_docker_command(command):
    """Execute a docker command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_docker_containers():
    """Check if all required Docker containers are running"""
    print("🐳 Checking Docker containers...")
    
    required_containers = [
        "lifepaws-wordpress",
        "lifepaws-mysql", 
        "lifepaws-phpmyadmin"
    ]
    
    running_containers = []
    
    for container in required_containers:
        cmd = f"docker ps --filter name={container} --format '{{{{.Names}}}}'"
        success, stdout, stderr = run_docker_command(cmd)
        
        if success and container in stdout:
            print(f"  ✅ {container} is running")
            running_containers.append(container)
        else:
            print(f"  ❌ {container} is not running")
    
    return len(running_containers) == len(required_containers), running_containers

def check_wordpress_health():
    """Check WordPress website accessibility"""
    print("🌐 Checking WordPress website...")
    
    try:
        response = requests.get("http://localhost:8080", timeout=10)
        if response.status_code == 200:
            print("  ✅ WordPress website is accessible")
            return True
        else:
            print(f"  ❌ WordPress returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ WordPress website is not accessible: {e}")
        return False

def check_phpmyadmin_health():
    """Check phpMyAdmin accessibility"""
    print("🗄️ Checking phpMyAdmin...")
    
    try:
        response = requests.get("http://localhost:8081", timeout=10)
        if response.status_code == 200:
            print("  ✅ phpMyAdmin is accessible")
            return True
        else:
            print(f"  ❌ phpMyAdmin returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ phpMyAdmin is not accessible: {e}")
        return False

def check_database_connection():
    """Check MySQL database connection"""
    print("💾 Checking database connection...")
    
    cmd = 'docker exec -it lifepaws-mysql mysql -u wordpress -pwordpress_password -e "SELECT 1;"'
    success, stdout, stderr = run_docker_command(cmd)
    
    if success:
        print("  ✅ Database connection successful")
        return True
    else:
        print(f"  ❌ Database connection failed: {stderr}")
        return False

def check_wordpress_database():
    """Check WordPress database structure"""
    print("📊 Checking WordPress database...")
    
    # Check if WordPress tables exist
    cmd = 'docker exec -it lifepaws-mysql mysql -u wordpress -pwordpress_password wordpress -e "SHOW TABLES;"'
    success, stdout, stderr = run_docker_command(cmd)
    
    if success:
        tables = stdout.strip().split('\n')[1:]  # Skip header
        expected_tables = ['wp_users', 'wp_posts', 'wp_options']
        
        found_tables = []
        for table in expected_tables:
            if any(table in line for line in tables):
                found_tables.append(table)
        
        if len(found_tables) == len(expected_tables):
            print(f"  ✅ WordPress database structure is correct ({len(tables)} tables found)")
            return True
        else:
            print(f"  ⚠️ Some WordPress tables are missing. Found: {found_tables}")
            return False
    else:
        print(f"  ❌ Failed to check database structure: {stderr}")
        return False


def check_disk_space():
    """Check available disk space"""
    print("💽 Checking disk space...")
    
    cmd = "docker exec lifepaws-wordpress df -h /var/www/html"
    success, stdout, stderr = run_docker_command(cmd)
    
    if success:
        lines = stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 4:
                used = parts[2]
                available = parts[3]
                print(f"  📊 Disk usage: {used} used, {available} available")
                return True
    
    print("  ⚠️ Could not determine disk space")
    return False

def generate_report(results):
    """Generate a health check report"""
    print("\n" + "=" * 60)
    print("📋 HEALTH CHECK REPORT")
    print("=" * 60)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    
    print(f"📊 Overall Status: {passed_checks}/{total_checks} checks passed")
    print()
    
    for check_name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name}")
    
    print()
    if passed_checks == total_checks:
        print("🎉 All systems are healthy!")
        print("🌐 WordPress: http://localhost:8080")
        print("🗄️ phpMyAdmin: http://localhost:8081")
    else:
        print("⚠️ Some issues detected. Please review the failed checks above.")
    
    print("=" * 60)

def main():
    """Main function"""
    print("🔧 WordPress Health Check Script")
    print("=" * 60)
    
    # Run all health checks
    results = {}
    
    results["Docker Containers"] = check_docker_containers()[0]
    results["WordPress Website"] = check_wordpress_health()
    results["phpMyAdmin"] = check_phpmyadmin_health()
    results["Database Connection"] = check_database_connection()
    results["WordPress Database"] = check_wordpress_database()
    results["Disk Space"] = check_disk_space()
    
    # Generate report
    generate_report(results)
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)  # All checks passed
    else:
        sys.exit(1)  # Some checks failed

if __name__ == "__main__":
    main()
