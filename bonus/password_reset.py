#!/usr/bin/env python3
"""
Simple WordPress Password Reset Script
Uses MD5 hash for reliable password reset
"""

import subprocess
import sys

def run_docker_command(command):
    """Execute a docker command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def reset_password_md5(username, password):
    """Reset password using MD5 hash (simple and reliable)"""
    # SQL command to update password with MD5 hash
    sql_command = f"UPDATE wp_users SET user_pass = MD5('{password}') WHERE user_login = '{username}';"
    
    # Execute the command
    docker_cmd = f'docker exec -it lifepaws-mysql mysql -u wordpress -pwordpress_password wordpress -e "{sql_command}"'
    
    success, stdout, stderr = run_docker_command(docker_cmd)
    
    if success:
        print(f"✅ Password reset successful for user: {username}")
        return True
    else:
        print(f"❌ Password reset failed for user: {username}")
        print(f"Error: {stderr}")
        return False

def verify_user_exists(username):
    """Check if a user exists in the database"""
    sql_command = f"SELECT user_login FROM wp_users WHERE user_login = '{username}';"
    docker_cmd = f'docker exec -it lifepaws-mysql mysql -u wordpress -pwordpress_password wordpress -e "{sql_command}"'
    
    success, stdout, stderr = run_docker_command(docker_cmd)
    
    if success and username in stdout:
        return True
    return False

def main():
    """Main function"""
    print("🔧 Simple WordPress Password Reset Script")
    print("=" * 50)
    
    # Check if containers are running
    success, stdout, stderr = run_docker_command("docker ps --filter name=lifepaws-mysql --format '{{.Names}}'")
    if not success or "lifepaws-mysql" not in stdout:
        print("❌ MySQL container is not running. Please start Docker containers first.")
        sys.exit(1)
    
    # Get username from command line or use default
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = "intern_test"
    
    print(f"🎯 Target user: {username}")
    
    # Verify user exists
    if not verify_user_exists(username):
        print(f"❌ User '{username}' does not exist in the database.")
        sys.exit(1)
    
    print(f"✅ User '{username}' found in database.")
    
    # Get password from user input
    password = input(f"Enter new password for '{username}': ")
    
    if not password.strip():
        print("❌ Password cannot be empty!")
        sys.exit(1)
    
    # Reset password
    success = reset_password_md5(username, password)
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Password reset completed successfully!")
        print(f"📝 Login details:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Login URL: http://localhost:8080/wp-admin")
        print("=" * 50)
    else:
        print("\n❌ Password reset failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
