# MantisBT Bug Tracking Experiment --- Complete Setup and Demonstration Guide

This guide documents the MantisBT practical from a fresh Ubuntu setup
through installation, configuration, issue reporting, workflow
demonstration, screenshots, troubleshooting, and viva preparation.

**Lab environment:** Ubuntu 24.04, Apache2, MariaDB, PHP, Composer, Git,
and MantisBT.

> Values below match the lab configuration used during this experiment.
> Replace them consistently if you choose different credentials or
> paths. Do not use the example password on a public or production
> server.

## 1. Experiment objective

Install and demonstrate MantisBT, a free and open-source, web-based bug
and issue tracking system.

The experiment demonstrates: - Creating projects and categories. -
Creating users and assigning roles. - Reporting bugs and feature
requests. - Setting severity, priority, reproducibility, and category. -
Assigning issues to developers. - Adding notes and viewing issue
history. - Changing issue status through its lifecycle. - Searching,
filtering, and reviewing issues.

**Suggested experiment title:** Study and demonstration of an online Bug
Tracking/Issue Tracking tool --- MantisBT.

## 2. Pre-installation checklist

Before starting, verify:

-   [ ] Ubuntu is running and your account can use `sudo`.
-   [ ] Internet access is available.
-   [ ] Sufficient free disk space is available.
-   [ ] You know the installation directory and database credentials.
-   [ ] No other service is unexpectedly occupying port 80.
-   [ ] A browser is available.
-   [ ] You have a folder ready for practical screenshots.

Check the system:

``` bash
lsb_release -a
uname -r
df -h /
```

Check whether the software is already installed:

``` bash
apache2 -v
mariadb --version
php -v
composer --version
```

Check port 80:

``` bash
sudo ss -ltnp | grep ':80'
```

If another service is using port 80, identify it before changing or
stopping anything.

## 3. Install Apache, MariaDB, PHP, and required tools

Update package lists:

``` bash
sudo apt update
```

Install the packages:

``` bash
sudo apt install -y apache2 mariadb-server mariadb-client \
  php libapache2-mod-php php-mysql php-gd php-mbstring \
  php-curl php-xml php-zip php-bcmath php-intl \
  composer git unzip
```

Enable and start services:

``` bash
sudo systemctl enable --now apache2
sudo systemctl enable --now mariadb
```

Verify:

``` bash
sudo systemctl status apache2 --no-pager
sudo systemctl status mariadb --no-pager
php -v
composer --version
php -m
```

Confirm the PHP module list includes the extensions required by your
MantisBT release, including database support (`mysqli`/`mysqlnd`), `gd`,
`mbstring`, `curl`, `xml`, and `zip`.

If you install more PHP extensions later, restart Apache:

``` bash
sudo systemctl restart apache2
```

Open `http://localhost/` in a browser. The Apache default page should
appear.

If Apache does not respond:

``` bash
sudo systemctl status apache2 --no-pager
sudo journalctl -u apache2 -n 50 --no-pager
```

## 4. Create the MantisBT database

Open the MariaDB administrative shell:

``` bash
sudo mariadb
```

Execute:

``` sql
CREATE DATABASE bugtracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'mantisuser'@'localhost'
  IDENTIFIED BY 'MantisLab@2026';

GRANT ALL PRIVILEGES ON bugtracker.*
  TO 'mantisuser'@'localhost';

FLUSH PRIVILEGES;

SHOW GRANTS FOR 'mantisuser'@'localhost';

EXIT;
```

The example database details are:

  Setting         Value
  --------------- ------------------
  Database        `bugtracker`
  Database user   `mantisuser`
  Host            `localhost`
  Lab password    `MantisLab@2026`

**Security:** Choose a unique, strong password for any deployment beyond
an isolated local lab.

Test the account before opening the MantisBT installer:

``` bash
mysql -u mantisuser -p -h localhost bugtracker
```

Enter the password when prompted. If the MariaDB prompt opens, the
account can connect. Exit using:

``` sql
EXIT;
```

If login fails, inspect the database and grants:

``` bash
sudo mariadb -e "SHOW DATABASES;"
sudo mariadb -e "SHOW GRANTS FOR 'mantisuser'@'localhost';"
```

Do not continue until the database login works.

## 5. Download and prepare MantisBT

Apache's document root is `/var/www/html`.

``` bash
cd /var/www/html
```

Check whether the destination already exists:

``` bash
ls -ld /var/www/html/mantisbt
```

If it does not exist, clone MantisBT:

``` bash
sudo git clone https://github.com/mantisbt/mantisbt.git /var/www/html/mantisbt
```

If it already exists, inspect it rather than cloning over it:

``` bash
cd /var/www/html/mantisbt
git status
git remote -v
```

Initialize submodules and install Composer dependencies:

``` bash
sudo git submodule update --init --recursive
sudo composer install --no-interaction
```

Verify the autoloader:

``` bash
ls -l /var/www/html/mantisbt/vendor/autoload.php
```

The file must exist. A missing `vendor/autoload.php` usually means
Composer dependencies have not been installed successfully.

Check the directory:

``` bash
ls -la /var/www/html/mantisbt
```

### Permissions

Apache must be able to read the application and write only to the
directories MantisBT requires. Do not make the whole web directory
world-writable. Follow the installation and permissions instructions for
the exact MantisBT release. Remove installer-related write permissions
after installation where the release documentation requires it.

## 6. Run the web installer

Open:

``` text
http://localhost/mantisbt/
```

The installer should appear. Use these values for the lab database:

  Installer field                         Value
  --------------------------------------- -------------------------
  Database type                           MySQL Improved / MySQLi
  Hostname                                `localhost`
  Database name                           `bugtracker`
  Database username                       `mantisuser`
  Database password                       `MantisLab@2026`
  Database admin username, if requested   `mantisuser`
  Database admin password, if requested   `MantisLab@2026`
  Table prefix                            `mantis`
  Plugin table prefix                     `plugin`
  Table suffix                            `_table`
  Time zone                               `Asia/Kolkata`

The normal database username/password fields identify the account
MantisBT will use. If the installer separately requests an account to
create or modify the database, that account must have the required
privileges. In this lab, `mantisuser` was granted privileges on
`bugtracker`, so it was entered in both places.

After installation, open the login page and sign in using the
administrator account created during installation. The account used in
this lab was `administrator`.

### If the installer reports a database error

1.  Confirm MariaDB is running.
2.  Test the database login using the command in Section 4.
3.  Recheck the database name, host, username, and password.
4.  Confirm the account has privileges on `bugtracker`.
5.  Check the Apache error log if the page itself fails.

Useful checks:

``` bash
sudo systemctl status mariadb --no-pager
sudo tail -n 100 /var/log/apache2/error.log
```

### After installation: security checks

-   Follow the installed release's instructions for disabling/removing
    installer access.
-   Protect `config_inc.php`, which contains database connection
    details.
-   Change weak or default passwords.
-   Do not expose this lab installation to the public Internet.
-   Configure HTTPS and working email/SMTP for a real deployment.

## 7. Log in and create a project

Open:

``` text
http://localhost/mantisbt/
```

Log in as administrator.

Create the demonstration project:

1.  Open **Manage**.
2.  Open **Manage Projects**.
3.  Select **Create New Project**.
4.  Enter the project name: `Open Source Bug Tracking Project`.
5.  Enter a description, for example:
    `Demonstration project for reporting, assigning, tracking, and resolving software issues using MantisBT.`
6.  Save the project.

Create project categories such as:

-   `Search`
-   `User Interface`
-   `Custom Fields`
-   `Feature Request`

Categories group issues by project area. They are not the same as
priority or severity.

## 8. Create users and assign project roles

Go to **Manage → Manage Users → Create New Account**.

Suggested demonstration accounts:

  Username       Suggested global access level   Purpose
  -------------- ------------------------------- --------------------------
  `teamleader`   Manager                         Oversees project issues
  `developer1`   Developer                       Works on assigned bugs
  `developer2`   Developer                       Works on assigned issues
  `tester1`      Reporter                        Reports and tests issues

Use valid email addresses if you expect email activation or
notifications to work.

### Global access and project access are different

-   **Global access level:** the user's general permissions in MantisBT.
-   **Project-level access level:** the user's role in a particular
    project.

Creating a user does not automatically add that user to the project.

To add a user to the project:

1.  Open **Manage → Manage Users**.
2.  Select the user.
3.  Find **Add user to project**.
4.  Select `Open Source Bug Tracking Project`.
5.  Select the required project role, such as `developer`.
6.  Click **Add User**.

Repeat for the other users. Check that the project appears in the user's
assigned-project list.

### Passwords in a local lab

MantisBT normally uses email activation or password-reset flows,
depending on its configuration. A placeholder address such as
`developer1@example.com` cannot receive a real email.

For a real deployment, configure SMTP and use the normal
activation/reset process.

For an isolated local lab, an administrator can use the
version-appropriate password-reset procedure. Some configurations
disable reset emails; in those configurations, the reset action may set
a blank password. If you use that method, sign in locally and
immediately set a non-empty password under **My Account**. Never use
blank passwords on an Internet-accessible server.

Do not assume that a newly created account already has a usable
password. You can also use the administrator's **Impersonate User**
feature to demonstrate permissions, but clearly distinguish
impersonation from a separate user login.

## 9. Report issues

Open **Report Issue**, select the project, and complete the summary,
description, category, reproducibility, severity, priority, and other
enabled fields.

The following are **sample demonstration records**, not confirmed
defects in the current MantisBT release. They illustrate how to enter
different issue types. If the assignment requires three actual bugs in
an open-source codebase, reproduce and verify the defects in that
selected project before presenting them as confirmed bugs.

### Issue 1 --- Functional/search defect (sample)

  -----------------------------------------------------------------------
  Field                               Example
  ----------------------------------- -----------------------------------
  Summary                             Search fails when the query
                                      contains special characters

  Category                            Search

  Type                                Functional bug / search defect

  Severity                            Major

  Priority                            High

  Assigned to                         `developer1`

  Description                         Enter a search term containing
                                      supported special characters and
                                      check whether the expected matching
                                      records are returned. Record the
                                      exact input and actual result.
  -----------------------------------------------------------------------

### Issue 2 --- Regression/data-persistence defect (sample)

  -----------------------------------------------------------------------
  Field                               Example
  ----------------------------------- -----------------------------------
  Summary                             Custom field value disappears after
                                      editing an unrelated field

  Category                            Custom Fields

  Type                                Regression bug / data-persistence
                                      defect

  Severity                            Major

  Priority                            High

  Assigned to                         `developer1`

  Description                         Create an issue with a custom field
                                      value, edit a different field,
                                      save, and check whether the
                                      original custom field value
                                      remains. Record the steps and
                                      actual result.
  -----------------------------------------------------------------------

### Issue 3 --- Feature request (sample)

  -----------------------------------------------------------------------
  Field                               Example
  ----------------------------------- -----------------------------------
  Summary                             Add a description field to project
                                      categories

  Category                            Feature Request

  Type                                Enhancement / feature request

  Severity                            Feature (if available in the
                                      configuration)

  Priority                            Normal

  Assigned to                         `developer2`

  Description                         Request an optional description for
                                      each project category so users
                                      understand when to use it.
  -----------------------------------------------------------------------

A genuine bug report should include:

-   A concise title.
-   Exact steps to reproduce.
-   Expected result.
-   Actual result.
-   Project and version.
-   Operating system/environment.
-   Screenshot or log, if useful.
-   Reproducibility and justified severity.

Do not classify a feature request as a software defect.

## 10. Demonstrate the issue workflow

A typical issue lifecycle is:

1.  **New** --- issue has been reported.
2.  **Assigned** --- issue has been assigned to a developer.
3.  **Acknowledged / Confirmed** --- reviewed or confirmed, depending on
    configuration.
4.  **Resolved** --- developer marks it addressed and selects a
    resolution.
5.  **Closed** --- issue is reviewed and closed.

Exact status names and transitions can vary with MantisBT configuration
and permissions.

### Practical demonstration sequence

1.  Log in as administrator or reporter and report an issue.
2.  Open its details page.
3.  Show issue ID, summary, description, category, severity, priority,
    and status.
4.  Assign the issue to `developer1`.
5.  Add a note describing investigation or the proposed fix.
6.  Log in as the developer, or use **Impersonate User** to demonstrate
    permissions.
7.  Update the issue status as appropriate.
8.  Add resolution/fix information when resolving it.
9.  Return to the tester/administrator account and verify the updated
    status.
10. Close the issue after verification.

For a feature request, demonstrate recording, review, prioritization,
and assignment. Do not claim it is a confirmed defect.

## 11. Demonstrate other MantisBT features

If time permits, demonstrate:

-   **View Issues:** list issues in the selected project.
-   **Filters:** filter by status, reporter, handler, category,
    severity, or priority.
-   **Search:** find issues by ID or search term.
-   **Notes:** record investigation and discussion.
-   **Attachments:** attach screenshots, logs, or evidence.
-   **Change history:** inspect how issue fields and status changed.
-   **Assignment:** transfer responsibility to another developer.
-   **User permissions:** compare reporter, developer, and manager
    access.
-   **Categories:** group issues by functional area.

Available options depend on the installed version and project
configuration.

## 12. Screenshots for the practical journal

Create a screenshot directory:

``` bash
mkdir -p ~/Unix-Operating-System/Open-Source-Software/MantisBT/screenshots
```

Capture genuine screenshots from your installation:

-   [ ] Apache default page (`http://localhost/`).
-   [ ] MantisBT login page.
-   [ ] Administrator dashboard.
-   [ ] Project creation or project list.
-   [ ] Project categories.
-   [ ] Manage Users page showing created accounts.
-   [ ] User edit page showing global access level.
-   [ ] User edit page showing project membership and project access
    level.
-   [ ] Report Issue form.
-   [ ] First issue details.
-   [ ] Second issue details.
-   [ ] Feature request details.
-   [ ] View Issues list showing the records.
-   [ ] Assigned issue showing its handler.
-   [ ] Issue note or change history.
-   [ ] Resolved issue.
-   [ ] Closed issue.

Do not fabricate screenshots or present sample descriptions as verified
defects.

## 13. Troubleshooting and checks before demonstration

### Apache not running

``` bash
sudo systemctl status apache2 --no-pager
sudo systemctl restart apache2
sudo journalctl -u apache2 -n 50 --no-pager
```

### MariaDB not running

``` bash
sudo systemctl status mariadb --no-pager
sudo systemctl restart mariadb
```

### Missing Composer autoloader

``` bash
ls -l /var/www/html/mantisbt/vendor/autoload.php
```

If it is missing:

``` bash
cd /var/www/html/mantisbt
sudo composer install --no-interaction
```

### Database connection failure

``` bash
mysql -u mantisuser -p -h localhost bugtracker
sudo mariadb -e "SHOW GRANTS FOR 'mantisuser'@'localhost';"
```

### Apache/PHP errors

``` bash
sudo tail -n 100 /var/log/apache2/error.log
php -m
```

After installing a missing PHP extension:

``` bash
sudo systemctl restart apache2
```

### Developer cannot see or handle project issues

Check:

-   User account is enabled.
-   User is added to the correct project.
-   Project-level role is appropriate.
-   Issue belongs to that project.
-   Issue handler is set to that user.

### Final pre-demo health check

``` bash
sudo systemctl is-active apache2
sudo systemctl is-active mariadb
test -f /var/www/html/mantisbt/vendor/autoload.php && echo "Composer autoloader: OK"
```

Then open `http://localhost/mantisbt/`, log in, and verify the project,
users, categories, and issues.

## 14. Comparison of FOSS bug-tracking tools

FOSS means **Free and Open Source Software**.

  -----------------------------------------------------------------------
  Tool                    Main purpose            Notable characteristics
  ----------------------- ----------------------- -----------------------
  MantisBT                Dedicated bug/issue     Lightweight web-based
                          tracking                tracker, categories,
                                                  roles, workflow,
                                                  notifications

  Bugzilla                Defect tracking         Mature bug database,
                                                  detailed search and
                                                  workflow

  Redmine                 Project management and  Projects, issues, wiki,
                          issue tracking          time tracking,
                                                  repository integration

  Trac                    Project management and  Issue tracker, wiki,
                          issue tracking          source browser

  GitLab                  DevOps and software     Issues integrated with
                          collaboration           Git repositories, merge
                                                  requests, CI/CD

  Gitea                   Self-hosted Git         Lightweight Git hosting
                          collaboration           with issues and pull
                                                  requests

  OpenProject             Project/work management Work packages, project
                                                  planning,
                                                  collaboration,
                                                  issue/work tracking
  -----------------------------------------------------------------------

**Comparison conclusion:** MantisBT is suitable when the primary
requirement is focused bug tracking. Bugzilla is another dedicated
defect tracker. Redmine and OpenProject provide broader
project-management functionality. GitLab and Gitea combine issue
tracking with source-code collaboration and repository workflows.

## 15. Viva questions and answers

**1. What is MantisBT?**\
MantisBT is a free and open-source, web-based bug and issue tracking
system.

**2. What is bug tracking?**\
It is the process of reporting, recording, assigning, monitoring,
resolving, and closing software defects.

**3. What is an issue?**\
An issue is a tracked item such as a bug, task, or feature request.

**4. What is severity?**\
Severity describes the technical impact of a defect on the software.

**5. What is priority?**\
Priority indicates how urgently an issue should be addressed.

**6. What is reproducibility?**\
It describes how consistently the reported problem can be reproduced.

**7. What is a category?**\
A category groups issues by a project area or functional component.

**8. What is an issue handler?**\
The handler is the user responsible for working on an issue.

**9. Difference between a bug and a feature request?**\
A bug is unexpected or incorrect behavior. A feature request asks for
new or improved functionality.

**10. Difference between global and project access?**\
Global access defines general system permissions; project access defines
a user's role within a particular project.

**11. What are issue notes used for?**\
They record investigation details, discussions, and progress.

**12. Why is issue history useful?**\
It records changes to an issue and helps the team understand progress
and accountability.

**13. What is FOSS?**\
Free and Open Source Software is software distributed under a license
that grants specified rights to use, inspect, modify, and redistribute
it.

**14. Name alternatives to MantisBT.**\
Bugzilla, Redmine, Trac, GitLab, Gitea, and OpenProject.

## 16. Suggested practical conclusion

MantisBT was installed and configured on Ubuntu using Apache, MariaDB,
and PHP. A demonstration project was created, users were configured with
appropriate access levels, and sample issues were reported, assigned,
updated, and tracked through the issue workflow. The experiment
demonstrates how an open-source bug-tracking system supports defect
reporting, team collaboration, responsibility assignment, and issue
lifecycle management.

> **Important for the final record:** Clearly distinguish sample
> demonstration tickets from defects personally reproduced in a selected
> open-source codebase. If the assignment requires three actual bugs,
> include the project/version, reproduction steps, expected result,
> actual result, and evidence for each verified bug.
