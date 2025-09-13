set -e

wpcli() { docker compose run --rm wpcli "$@"; }

# Install plugin
wpcli plugin install all-in-one-wp-migration --activate \
  || wpcli plugin activate all-in-one-wp-migration

echo "Plugin has been installed."

# Find the user intern_test
wpcli user get intern_test >/dev/null 2>&1 \
  || { echo "User does not exist."; exit 1; }

echo "User has found."

# Reset the password
wpcli user update intern_test --user_pass="InternTestPw123"

echo "User password has been updated."


