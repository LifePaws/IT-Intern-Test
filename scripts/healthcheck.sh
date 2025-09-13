#A quick health check to show the site is running
set -e
curl -sSf http://localhost:8080/wp-login.php >/dev/null && echo "The site is running" || (echo "The site is NOT running" && exit 1)