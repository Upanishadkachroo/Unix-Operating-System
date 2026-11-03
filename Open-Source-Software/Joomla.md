# Experiment: Demonstration of CMS Software – Joomla

A complete practical guide to installing, configuring, and demonstrating **Joomla**, an open-source Content Management System (**CMS**), including user management with **ACL**, core feature implementation, and comparison with Moodle and Schoology.

---

## Table of Contents

1. [Aim](#1-aim)
2. [Objectives](#2-objectives)
3. [Introduction to **CMS**](#3-introduction-to-cms)
4. [Introduction to Joomla](#4-introduction-to-joomla)
5. [Joomla Architecture](#5-joomla-architecture)
6. [Installation of Joomla on Ubuntu](#6-installation-of-joomla-on-ubuntu)
7. [Creating Users and Managing Access](#7-creating-users-and-managing-access)
8. [Managing a Website for a Client](#8-managing-a-website-for-a-client)
9. [Implementing Joomla Core Features](#9-implementing-joomla-core-features)
10. [Comparison: Joomla vs Moodle vs Schoology](#10-comparison-joomla-vs-moodle-vs-schoology)
11. [Observations](#11-observations)
12. [Result](#12-result)
13. [Screenshots to Attach](#13-screenshots-to-attach)
14. [Viva Questions and Answers](#14-viva-questions-and-answers)
15. [Final Practical Checklist](#15-final-practical-checklist)

---

## 1. Aim

To study and demonstrate the features of **Joomla Content Management System (**CMS**)**, create different users with different access permissions, demonstrate how Joomla helps a web developer manage websites for clients, implement its core features, and compare Joomla with other **CMS**/Learning Management Systems such as Moodle and Schoology.

---

## 2. Objectives

## Understand the concept and architecture of a Content Management System.

## Study the installation and configuration of Joomla. ## Create users with different roles and permissions. ## Create and manage a website for a client. ## Implement Joomla's core features, including articles, categories, menus, modules, templates, and media management. ## Understand Joomla's Access Control List (ACL). ## Compare Joomla with Moodle and Schoology. ## Understand the advantages of using a CMS for website development and maintenance.

---

## 3. Introduction to CMS

A **Content Management System (**CMS**)** is software that allows users to create, edit, organize, publish, and manage digital content without requiring extensive programming knowledge.

A **CMS** generally provides two interfaces:

- **Frontend:** The public-facing website that visitors can access.
- **Backend:** The administration interface used by administrators and content managers.

### How a CMS works

```
Website Administrator / Client
        ↓
Creates and manages website content
        ↓
**CMS** Administration Panel
    (Articles · Users · Menus · Media · Settings)
    ↓
Application and Database
        ↓
### Published Website
   (Displays dynamic web pages to visitors)
```

A **CMS** **separates content from presentation**. Therefore, the client can update the content while the website's developer maintains the design and technical configuration.

---

## 4. Introduction to Joomla

**Joomla** is an open-source **CMS** used to develop and manage dynamic websites and web applications. It is based on **PHP** and uses a database to store website content and configuration.

It is suitable for:

- College and university websites
- Business and corporate websites
- News portals and blogs
- Government websites
- Community websites
- Personal websites
- Intranet and organizational portals

### Main Features of Joomla

| Feature | Purpose |
|---------|---------|
| User Management | Create and manage different users |
| Article Management | Create, edit, and publish content |
| Category Management | Organize articles into categories |
| Menu Management | Create website navigation |
| Module Management | Display content in different website positions |
| Template Management | Customize website appearance |
| Media Management | Upload and organize images and files |
| ACL | Control user permissions |
| Extensions | Add additional functionality |
| Multilingual Support | Create websites in multiple languages |
| SEO | Configure search-friendly URLs and metadata |
| Publishing Workflow | Control the article approval process |

---

## 5. Joomla Architecture

Joomla has two major interfaces:

- **Frontend:** Public website visible to visitors.
- **Backend:** Administrative interface for managing the website.

### Major Architectural Elements

| Element | Description |
|---------|-------------|
| Components | Main application functionality, such as articles and contacts |
| Modules | Small blocks displayed around the main content |
| Plugins | Event-based functionality that extends Joomla |
| Templates | Control the visual appearance and layout |
| Database | Stores articles, users, menus, and configuration |
| Libraries | Reusable code used by Joomla and extensions |

### Example

Suppose a college website has a navigation bar, login form, announcement section, and contact page:

- **Articles component** displays the college information
- **Menu module** displays navigation links
- **Login module** provides a login form
- **Template** controls the appearance
- **Database** stores all relevant content and user details

---

## 6. Installation of Joomla on Ubuntu

For this experiment, we create a sample college website named ****ABC** College Website**.

### 6.1 System Requirements

| Requirement | Purpose |
|-------------|---------|
| Ubuntu 24.04 | Operating system |
| Apache | Web server |
| PHP | Server-side programming language |
| MariaDB/MySQL | Database |
| Joomla | CMS software |
| Web browser | Access frontend and backend |

You can use either a native Apache/**PHP**/MariaDB installation or Docker.

### 6.2 Joomla 6.2 Compatibility

We use **Joomla 6.2.0** in this experiment.

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| PHP | 8.3 | 8.4 |
| MariaDB | 10.4 | 12.0 |
| Apache | 2.4 | 2.4 |
| PHP memory limit | 256 MB | 256 MB or more |

MariaDB 10.11 (default on Ubuntu 24.04) is compatible with Joomla 6.2.0.

### 6.3 Create the Project Directory

```bash mkdir -p ~/Unix-Operating-System/Open-Source-Software/Joomla cd ~/Unix-Operating-System/Open-Source-Software/Joomla ```

### 6.4 Download Joomla

Visit the official download portal and download the current stable release as a **ZIP** archive:

``` [https://downloads.joomla.org/](https://downloads.joomla.org/) ```

Extract the archive:

```bash mkdir joomla unzip Joomla_6.2.0-Stable-Full_Package.zip -d joomla ```

### 6.5 Install PHP and Required Extensions

First check your **PHP** version:

```bash php -v ```

Check installed modules:

```bash php -m ```

Install the necessary **PHP** packages if missing:

```bash
sudo apt update
sudo apt install -y \
    php \
    libapache2-mod-php \
    php-mysql \
    php-xml \
    php-gd \
    php-curl \
    php-mbstring \
    php-intl \
    php-zip
```

Verify extensions:

```bash php -m | grep -Ei \ 'mysqli|mysqlnd|pdo_mysql|json|simplexml|dom|zlib|gd|mbstring' ```

You should see the required **PHP** extensions listed.

### 6.6 Start the Web Server and Database

```bash sudo systemctl start apache2 sudo systemctl start mariadb sudo systemctl status apache2 sudo systemctl status mariadb ```

> **Note:** If Apache shows a warning like `DocumentRoot [/var/www/bugzilla] does not exist`, this is from an earlier Bugzilla configuration and does not affect Joomla. It can be inspected later without disturbing your existing setup.

### 6.7 Create the Database

Open MariaDB:

```bash sudo mariadb ```

Execute:

```sql
**CREATE** **DATABASE** joomla_db
    **CHARACTER** **SET** utf8mb4
    **COLLATE** utf8mb4_unicode_ci;

**CREATE** **USER** 'joomla_user'@'localhost' **IDENTIFIED** BY 'ChangeThisStrongPassword!';

**GRANT** **ALL** **PRIVILEGES** ON joomla_db.* TO 'joomla_user'@'localhost';

**FLUSH** **PRIVILEGES**; **EXIT**; ```

Verify the connection:

```bash mariadb -u joomla_user -p -h localhost joomla_db ```

Enter the password. On success you should see:

``` Welcome to the MariaDB monitor. MariaDB [joomla_db]> ```

Exit with `**EXIT**;`.

> **Security note:** Rotate the password if it was shared in any transcript. Use: > ```sql > **ALTER** **USER** 'joomla_user'@'localhost' **IDENTIFIED** BY 'NewStrongPassword'; > **FLUSH** **PRIVILEGES**; > ```

### 6.8 Deploy Joomla into Apache

Copy Joomla into Apache's web root:

```bash cd ~/Unix-Operating-System/Open-Source-Software/Joomla/Joomla_6.2.0-Stable-Full_Package sudo mkdir -p /var/www/html/joomla sudo cp -a . /var/www/html/joomla/ ```

Set ownership and permissions:

```bash sudo chown -R www-data:www-data /var/www/html/joomla sudo find /var/www/html/joomla -type d -exec chmod **755** {} \; sudo find /var/www/html/joomla -type f -exec chmod **644** {} \; ```

Restart Apache:

```bash sudo systemctl restart apache2 ```

Verify the entry point exists:

```bash ls -l /var/www/html/joomla/index.php ```

### 6.9 Verify Apache Modules

```bash apache2ctl -M | grep -E 'php|rewrite' ```

Ensure `php` (or `php8.x`) and `rewrite` are listed.

### 6.10 Open the Installation Wizard

Open your browser and visit:

``` [http://localhost/joomla](http://localhost/joomla) ```

You should see the Joomla installation screen.

#### Main Configuration

| Field | Example |
|-------|---------|
| Site Name | ABC College |
| Administrator Name | College Administrator |
| Administrator Username | collegeadmin |
| Administrator Password | Your strong password |
| Administrator Email | Your test email |

#### Database Configuration

| Field | Value |
|-------|-------|
| Database Type | MySQLi |
| Host Name | localhost |
| Username | joomla_user |
| Password | Your database password |
| Database Name | joomla_db |
| Table Prefix | Automatically generated |

#### Finalize Installation

- Review the configuration
- Verify that the database connection succeeds
- Complete installation
- Allow Joomla to remove or secure its installation directory when prompted

### 6.11 Verify the Installation

| Interface | URL |
|-----------|-----|
| Public website | `[http://localhost/joomla`](http://localhost/joomla`) |
| Administrator dashboard | `[http://localhost/joomla/administrator`](http://localhost/joomla/administrator`) |

Log in using the administrator credentials. You should now have access to:

- Content management
- User management
- Menus
- Modules
- Templates
- Media
- System configuration

### Installation Checkpoint

- [x] Joomla administrator dashboard opens
- [x] Login with administrator credentials succeeds
- [x] Frontend website opens
- [x] Database connection is working
- [x] Installation directory is secured or removed

---

## 7. Creating Users and Managing Access

One of the most important Joomla features is **User Management with Access Control List (**ACL**)**. **ACL** allows a website administrator to control what different users can view, create, edit, publish, and administer.

### 7.1 Understanding Joomla User Groups

| User Group | Permissions / Responsibilities |
|------------|-------------------------------|
| Public | Can access publicly available website content |
| Guest | Visitors who are not logged in |
| Registered | Can access content restricted to logged-in users |
| Author | Can create and manage their own articles |
| Editor | Can edit articles, including those created by other authors |
| Publisher | Can publish and manage articles |
| Manager | Can manage many website operations through the backend |
| Administrator | Has administrative permissions for most backend functions |
| Super Users | Have full administrative access |

### 7.2 Create Different Users

Navigate to: **Users → Manage → Users → New**

Fill in:

1. Name
## Username
## Email address
## Password
## User group
6. Save

### 7.3 Example User Creation

| User | Username | Group | Responsibility |
|------|----------|-------|----------------|
| College Admin | collegeadmin | Administrator | Manage website configuration |
| Content Manager | contentmanager | Manager | Manage website content |
| Faculty Member | faculty | Author | Create announcements and articles |
| Editor | editor1 | Editor | Review and edit articles |
| Student | student1 | Registered | Access restricted content |

Use different passwords for each account. Create corresponding accounts with your own test email addresses.

### 7.4 Demonstrate Permissions

| User | Group | Demonstration |
|------|-------|---------------|
| College Administrator | Administrator | Access backend dashboard, manage users, configure settings, manage articles, menus, and modules |
| Faculty Member | Author | Create an article, save an article, manage own articles, cannot publish unless explicitly permitted |
| Editor | Editor | Review articles, edit articles created by other users, correct content before publication |
| Student | Registered | Log in through the frontend, view restricted content, cannot access the backend by default |

> **Important:** Joomla permissions are configurable. Effective permissions depend on group inheritance, assigned access levels, and permission settings.

### 7.5 Demonstrate Frontend and Backend Access

Open two browser sessions:

- **Session 1:** Log in as `collegeadmin`
- **Session 2:** Log in as `faculty` or `student1`

Observe:

## The administrator can access the backend

## The author can create articles according to assigned permissions ## The registered user can access restricted frontend content ## The student cannot modify administrative settings

This demonstrates how a developer can provide a client with website-management access without giving everyone full administrative privileges.

---

## 8. Managing a Website for a Client

Assume a college has approached a web development company to create its official website.

### Proposed Website Structure

- Home
- About Us
- Departments
- Courses
- Admissions
- Notices and Announcements
- Contact Us

### Role of Developer and Client

| Developer / Web Agency | College Client |
|------------------------|----------------|
| Installs Joomla | Logs in to the website |
| Configures database | Updates college information |
| Selects and customizes template | Publishes announcements |
| Creates menus and categories | Uploads photographs and notices |
| Configures user accounts | Creates and edits permitted content |
| Configures security and backups | Reviews website content |
| Provides training | Maintains day-to-day content |

### Website Management Workflow

```
Developer creates the website
        ↓
Configure users, permissions and website design
        ↓
Handover website access to the college
        ↓
College staff manage articles and announcements
        ↓
Updated information appears on the public website
```

The key advantage is that college staff do not need to write **HTML**, **CSS**, or **PHP** whenever they want to update a notice or announcement.

---

## 9. Implementing Joomla Core Features

### Experiment 1: Article Management

An article is the basic unit of content in Joomla.

**Steps:**

## Navigate to **Content → Articles**

## Click **New** ## Enter title: `Welcome to ABC College` ## Enter the article content ## Select a category ## Add an image if required ## Set status to **Published** ## Click **Save**

**Observation:** The article is stored in the Joomla database and displayed on the frontend when published and made accessible through an appropriate menu or module.

### Experiment 2: Category Management

| Category | Articles |
|----------|----------|
| About Us | College introduction |
| Admissions | Admission notices |
| Departments | Department information |
| Announcements | General notices |
| Events | College events |

**Steps:**

## Navigate to **Content → Categories**

## Click **New**
## Enter the category title
## Add a description
5. Save
## Repeat for remaining categories

**Observation:** Articles can be grouped and filtered by category, making website content easier to manage.

### Experiment 3: Menu Management

**Steps:**

## Navigate to **Menus → Manage**

## Create a menu named `Main Menu` if not present
## Open the menu
## Click **New**
## Enter menu title (e.g., `About Us`)
## Select a menu item type
## Choose the appropriate article or category
8. Save

Create menu items:

- Home
- About Us
- Admissions
- Departments
- Announcements
- Contact Us

**Observation:** The frontend navigation menu provides access to the different website sections.

### Experiment 4: Module Management

Modules are small blocks of content displayed in predefined positions of the website template.

**Steps:**

## Navigate to **Content → Site Modules** (or **System → Manage → Site Modules**)

## Click **New** ## Select a module type ## Enter its title ## Configure its position ## Select pages on which it should appear ## Save and close

**Example:** Create a module named `College Announcements` configured to display latest published articles.

**Observation:** Modules help display reusable website elements without changing the main article content.

### Experiment 5: Template Management

Joomla includes the **Cassiopeia** frontend template and **Atum** administrator template.

**Steps:**

## Navigate to **System → Site Templates**

## View installed frontend templates
## Select **Cassiopeia** as the default site template
## Open its template options
## Customize colors, branding, and layout
6. Save
## Open frontend and observe updated appearance

**Observation:** Templates control the presentation of the website while keeping content separate from design.

### Experiment 6: Media Management

**Steps:**

## Navigate to **Content → Media**

## Create a folder named `college` ## Upload a college logo ## Upload a campus photograph ## Open an article ## Insert the uploaded image using the editor ## Save and preview the article

**Observation:** Media files can be reused across different website pages and articles.

### Experiment 7: Contact Management

**Steps:**

## Navigate to **Components → Contacts**

## Create a contact category named `College Administration`
## Create a new contact
## Enter the name `College Office`
## Enter the college's test email and contact details
6. Save
## Create a menu item of type **Contact** and select this contact
## Open frontend and verify the contact page

**Observation:** Visitors can find college contact information and, if enabled, use the contact form.

### Experiment 8: Smart Search

**Steps:**

## Navigate to **Components → Smart Search**

## Open the indexing section ## Run the indexer to index website content ## Create or enable the Smart Search module ## Publish the module in a suitable template position ## Search for a word such as `admissions` or `departments` on the frontend

**Observation:** Visitors can search indexed content rather than manually navigating every page.

### Experiment 9: Publishing and Article Workflow

Common article statuses: **Published**, **Unpublished**, **Archived**, **Trashed**.

**Steps:**

## Log in as a faculty author

## Create an article named `Upcoming Technical Event` ## Save as unpublished or submit for review ## Log in as content manager ## Review the article ## Publish if the user has the necessary permission ## Open frontend to verify publication

**Observation:** Joomla allows administrators to manage publication status through configurable workflows.

### Experiment 10: Search Engine Optimization (SEO)

**Steps:**

## Open **System → Global Configuration**

## Navigate to SEO settings ## Enable **Search Engine Friendly URLs** ## Configure URL rewriting if Apache supports it ## Configure required `.htaccess` file where appropriate ## Add descriptive title and metadata to articles ## Save and verify URLs

**Example:**

Before: ``` [http://localhost/joomla/index.php?option=com_content&id=10](http://localhost/joomla/index.php?option=com_content&id=10) ```

After enabling **SEF** URLs: ``` [http://localhost/joomla/about-us](http://localhost/joomla/about-us) ```

Actual URLs depend on menu aliases and Joomla routing configuration.

**Observation:** Search-friendly URLs and meaningful metadata improve the organization and discoverability of website content.

---

## 10. Comparison: Joomla vs Moodle vs Schoology

An important distinction is that **Joomla is primarily a general-purpose **CMS****, whereas **Moodle and Schoology are primarily Learning Management Systems (**LMS**)**.

An **LMS** is designed specifically to manage educational activities such as courses, assignments, assessments, student progress, and grades.

### Feature Comparison

| Feature | Joomla | Moodle | Schoology |
|---------|--------|--------|-----------|
| Primary purpose | Website management | Online learning | Online learning |
| Software type | CMS | LMS | LMS |
| Open source | Yes | Yes | No |
| Website creation | Excellent | Limited | Limited |
| Article/content management | Excellent | Course resources | Course materials |
| User management | Yes | Yes | Yes |
| User roles | ACL | Role-based | Role-based |
| Course management | Requires extensions | Excellent | Excellent |
| Assignment submission | Requires extensions | Built-in | Built-in |
| Online quizzes | Requires extensions | Built-in | Built-in |
| Gradebook | Requires extensions | Built-in | Built-in |
| Discussion forums | Extensions | Built-in | Built-in |
| Themes/design | Extensive templates | Themes | Platform customization |
| Best suited for | General websites | Schools/universities | School education |

### Major Differences

**Joomla vs Moodle:**

- Joomla builds and manages general websites; Moodle delivers and manages online education
- Joomla organizes content into articles, categories, and menus; Moodle organizes into courses, resources, and activities
- Moodle provides built-in assessment and grading that Joomla generally needs extensions for

**Joomla vs Schoology:**

- Joomla allows organizations to create and control their own websites; Schoology provides a specialized digital learning environment
- Joomla is open-source and self-hosted; Schoology is proprietary
- Schoology offers educational workflows such as assignments, gradebooks, and assessments

### Which Software to Select?

| Requirement | Recommended Software |
|-------------|---------------------|
| College official website | Joomla |
| Business website | Joomla |
| Online university courses | Moodle |
| Online quizzes and assignments | Moodle |
| School classroom management | Schoology |
| Student grading and assessment | Moodle / Schoology |
| Customizable organizational portal | Joomla |

**Conclusion:** Joomla, Moodle, and Schoology serve different purposes. Joomla is more suitable for general website management, whereas Moodle and Schoology are more suitable for educational content delivery and learning management.

---

## 11. Observations

## Joomla provides a centralized administrator dashboard.

## Multiple users can be created with different permissions. ## ACL controls what users can view, create, edit, and publish. ## Articles and categories make content management easier. ## Menus help visitors navigate the website. ## Modules display reusable content in different template positions. ## Templates allow customization of website appearance. ## Media management makes it easy to upload and organize files. ## Smart Search allows visitors to search website content. ## Joomla allows clients to manage their website without modifying source code.

---

## 12. Result

The installation, configuration, and features of **Joomla **CMS**** were studied and demonstrated.

Different users were created with different access permissions. A sample college website was designed to demonstrate how a developer can create a website and provide the client with facilities to manage website content.

The core features of Joomla, including article management, categories, menus, modules, templates, media management, contacts, Smart Search, publishing workflows, and **SEO**, were studied.

Joomla was also compared with Moodle and Schoology.

**Conclusion:** Joomla is an effective open-source **CMS** for developing and managing dynamic websites. Its user management, **ACL**, content management, and template features allow multiple users to maintain a website according to their responsibilities without requiring extensive programming knowledge.

---

## 13. Screenshots to Attach

Capture these screenshots while performing the experiment.

| No. | Screenshot | Demonstrates |
|-----|------------|--------------|
| 1 | Joomla installation page | Installation |
| 2 | Administrator dashboard | Backend |
| 3 | Frontend homepage | Public website |
| 4 | User management page | Creating users |
| 5 | User groups and permissions | ACL |
| 6 | Article creation page | Article management |
| 7 | Category management | Categories |
| 8 | Menu management | Navigation |
| 9 | Module management | Modules |
| 10 | Template settings | Design |
| 11 | Media manager | File management |
| 12 | Contact page | Contact management |
| 13 | Smart Search | Search functionality |
| 14 | Final college website | Complete demonstration |

---

## 14. Viva Questions and Answers

**Q1. What is a **CMS**?** A **CMS** is software used to create, edit, organize, and publish website content without requiring extensive programming knowledge.

**Q2. What is Joomla?** Joomla is a free and open-source **PHP**-based **CMS** used to create and manage dynamic websites.

**Q3. What is the difference between frontend and backend?**
- Frontend is the public-facing website.
- Backend is the administrative interface used to manage the website.

**Q4. What is an article in Joomla?** An article is a content item used to display information on a Joomla website.

**Q5. What is **ACL**?** **ACL** stands for Access Control List. It controls the permissions of different users and groups.

**Q6. What is the difference between a component and a module?** A component provides the main functionality and content of a page, whereas a module displays smaller blocks of content in predefined template positions.

**Q7. What is a plugin?** A plugin is an extension that adds functionality to Joomla by responding to specific system events.

**Q8. What is a template?** A template controls the appearance, layout, and visual design of a Joomla website.

**Q9. What is the purpose of categories?** Categories organize articles into groups to make website content easier to manage.

****Q10**. What is the role of a Super User?** A Super User has full administrative permissions over the Joomla website.

****Q11**. Can multiple users manage one Joomla website?** Yes. Joomla supports multiple users with different groups and permissions.

****Q12**. What is the difference between Joomla and Moodle?** Joomla is a general-purpose **CMS** used for website development, whereas Moodle is an **LMS** used for managing online courses, assignments, and assessments.

****Q13**. Is Joomla free?** Yes. Joomla is open-source software distributed under the **GNU** General Public License.

****Q14**. What is the purpose of modules?** Modules display reusable website elements such as menus, login forms, search boxes, and latest articles.

****Q15**. Can a client update a Joomla website without knowing programming?** Yes. A client with suitable permissions can update articles, images, announcements, and other content through the administrator interface.

---

## 15. Final Practical Checklist

Use this checklist when performing the experiment in your lab.

- [ ] Install Joomla and open the administrator dashboard
- [ ] Create the **ABC** College Website site structure
- [ ] Create administrator, manager, author, editor, and student users
- [ ] Demonstrate login using different user accounts
- [ ] Verify frontend and backend access permissions
- [ ] Create articles and categories
- [ ] Create and configure navigation menus
- [ ] Create and publish modules
- [ ] Customize the frontend template
- [ ] Upload and insert images using Media Manager
- [ ] Create a college contact page
- [ ] Configure and test Smart Search
- [ ] Demonstrate article publishing and approval
- [ ] Compare Joomla with Moodle and Schoology

### Quick Environment Verification

Before starting the demonstration, run:

```bash php -v php -m | grep -Ei 'mysqli|mysqlnd|pdo_mysql|json|simplexml|dom|zlib|gd|mbstring' apache2ctl -M | grep -E 'php|rewrite' ls -ld /var/www/html/joomla curl -I [http://localhost/joomla/](http://localhost/joomla/) ```

All commands should produce healthy output, confirming the installation environment is ready.

---

## Recommendation for the Lab

Give particular importance to the **user-management and **ACL** demonstration**. Creating multiple users and showing that each user has different permissions is the clearest way to demonstrate how Joomla manages a client's website rather than merely displaying a website created with a template.

---

**End of Experiment – Demonstration of **CMS** Software: Joomla**
