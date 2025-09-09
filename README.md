# IT Intern Take-Home Test – WordPress (Local by Flywheel)

## Objective
Using **Local (by Flywheel)** to spin up a local WordPress site, install and activate the **All-in-One WP Migration** plugin **via command/script (WP-CLI)**, then import the provided backup. Finally, locate the target user and **reset the password safely** (no hash cracking). Document your steps and troubleshooting.

---

## What We Provide
- Backup file: [lifepaws-demo.wpress](https://drive.google.com/file/d/1QQpLb5ewIx9_S2anX1hjjvenYQkH9zMw/view?usp=drive_link)  
- Target user: `intern_test` (exists in the backup)

---

## Prerequisites
- **Local (by Flywheel)** installed  
  - Download: https://localwp.com/
- **Git** installed
- A text editor (VS Code, etc.)

> Local includes WP-CLI. Use **“Open Site Shell”** in Local to run commands like `wp plugin install ...`.

---

## Tasks

### 1) Create a Local site
1. Open Local → **Create a new site** → choose any name (e.g., `intern-wp`).
2. Use **Preferred** environment (PHP/MySQL/NGINX versions are fine).
3. After creation, click **Open Site Shell** to access WP-CLI.

### 2) Install All-in-One WP Migration via WP-CLI
In the **Site Shell**:
```bash
wp plugin install all-in-one-wp-migration --activate
wp plugin status all-in-one-wp-migration
```

### 3) Import the backup
- Try importing the provided `.wpress` file using the plugin.
- If you hit **upload size/time limits**, document:
  - The exact error or restriction,
  - Why it happens (PHP upload/post limits, execution time, etc.),
  - How you would resolve or work around it.

### 4) User & password reset (safe method)
- Reset password via WP-CLI (no hash cracking):
```bash
wp user update intern_test --user_pass='NewStrongPass!123'
```
- Confirm login works and capture a screenshot (blur any sensitive info).

### 5) Documentation
Update:
- `docs/troubleshooting.md` – errors seen & how you fixed them
- `scripts/notes.md` – commands you ran (WP-CLI snippets)
- `README.md` – short **“How to Reproduce”** section

---

## Deliverables
- A **Pull Request** to this repository, created from your own fork.
- Your PR should include:
  - Updated `README.md` with your steps and notes
  - `docs/` (troubleshooting notes + screenshots)
  - `scripts/notes.md` with useful commands
  - Clear commit messages

---

## Git Workflow Requirements

- **Do not commit directly to this repository.**
- Please **fork** this repository into your own GitHub account.
- In your fork, create a new branch named:
  ```
  intern/<your-name>
  ```
  Example: `intern/alex-smith`

- Commit your work on that branch.
- Push the branch to your fork.
- When finished, open a **Pull Request** (PR) from your branch into the `main` branch of this repository.

---

## Evaluation (100 pts)
- Setup & Reproducibility (30)
- Scripted Plugin Install (20)
- Import & Troubleshooting clarity (20)
- Secure Password Reset (10)
- Documentation Quality (20)

### Bonus (+25)
- Automate common fixes (upload size, execution time)
- Use WP-CLI for most of the flow
- Basic hardening suggestions
- Health checks

---

## Useful WP-CLI Snippets
```bash
# Check versions
wp core version
wp --info

# Plugins
wp plugin list
wp plugin install all-in-one-wp-migration --activate

# Users
wp user list
wp user get intern_test --field=ID
wp user update intern_test --user_pass='NewStrongPass!123'
```

⚠️ **No cracking of password hashes.** Always use WordPress tools.
