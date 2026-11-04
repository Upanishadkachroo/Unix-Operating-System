# Experiment: Demonstration of SonarQube for Project Management and Comparison with Other Project Management Tools

## 1. Aim

To study and demonstrate the features of the project management tool SonarQube using a suitable open-source software project downloaded from the internet. To understand its capabilities for project planning, scheduling, task management, Agile/Scrum, bug tracking, and project quality management, and compare it with other project management tools.

## 2. Introduction to SonarQube

[SonarQube Logo **PNG** Vector (**SVG**) Free Download](https://images.openai.com/static-rsc-4/0x5xf8SzWSGAgz4yz1mZ5k1jloOOxx2hd5dGO0mi7wGDlMHdQtbmwBQZW4pMOKp-5NgJBuBPTWJM7NJJCDqhW0yDYzh65KbKiJyvg5DVlVFOxUCgYLbIg82Pmt1buY-BpoLeCq55OWDrxZcC_-_czVIK1m-sE8q43em9fn649Rw?purpose=inline)

SonarQube

SonarQube is an open-source code quality and security analysis platform. It automatically examines source code to identify bugs, security vulnerabilities, code smells, and maintainability problems.

Website: [Official SonarQube website](https://[www.sonarsource.com/products/sonarqube/?utm_source=chatgpt.com](https://www.sonarsource.com/products/sonarqube/?utm_source=chatgpt.com))

SonarQube is primarily a software quality management tool, not a complete project management tool like Jira or OpenProject.

It supports software project management indirectly by providing measurable information about code quality, technical debt, security, and development progress.

### Main features

## Static code analysis.

## Bug detection and tracking. ## Security vulnerability detection. ## Code smell identification. ## Quality Gates. ## Project quality dashboards. ## Code coverage and duplication analysis. ## Integration with CI/CD pipelines. ## Quality trend monitoring.

## 3. Software and hardware requirements

| Component        | Requirement                                              |
| ---------------- | -------------------------------------------------------- |
| Operating system | Ubuntu 24.04                                             |
| SonarQube        | Community Build                                          |
| Runtime          | Docker and Docker Compose                                |
| Browser          | Firefox / Chrome                                         |
| Source code      | Open-source GitHub project                               |
| RAM              | 4 GB minimum for a basic demonstration; more recommended |
| Docker           | Installed and running                                    |

For this experiment, Docker is convenient because it avoids manually configuring SonarQube and its Java runtime dependencies.

## 4. Architecture of SonarQube

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-server/**2025**.3/analyzing-source-code/analysis-overview?utm_source=chatgpt.com)

The architecture consists of three main components:

- SonarScanner: Examines source code and generates analysis results.
- SonarQube Server: Processes analysis results and displays issues, metrics, and quality reports.
- Database: Stores project information, analysis history, and configuration.

The general workflow is:

## Developer writes source code.

## SonarScanner analyzes the source code. ## Analysis results are submitted to SonarQube Server. ## SonarQube processes the results. ## The developer views bugs, vulnerabilities, code smells, and quality metrics through the dashboard.

## 5. Practical demonstration using an open-source project

We will use Spring PetClinic.

[Setting Up Your Development Environment | Azul Prime](https://images.openai.com/static-rsc-4/9MATbeY-SpYCmHHLX-pc6DKhPGbbBzKLKJhxnSFTpPd7LIdyBMryG5megeAeNusnfRbp6aEGEaxxgYKctANGghubdIigeKNAJ-mKH-iHphCEc4AZnLlDOJ29dep7dVk7bOCU19MIGw6341_WKfe6jYFGQ_uBs37vQkLugZQftTI?purpose=inline)

Spring PetClinic

An open-source Java application built using Spring Boot. It is suitable for demonstrating static code analysis, maintainability, bugs, code smells, and quality metrics.

Source: [GitHub repository](https://github.com/spring-projects/spring-petclinic?utm_source=chatgpt.com)

### Step 1: Install and start Docker

Check whether Docker is installed:

``` docker --version docker compose version ```

If Docker is already installed and working, proceed.

### Step 2: Start SonarQube using Docker

Run:

```
sudo docker run -d \
    --name sonarqube \
    -p **9000**:**9000** \
    sonarqube:community
```

Check the container:

``` sudo docker ps ```

Check its logs:

``` sudo docker logs -f sonarqube ```

Wait until SonarQube has finished starting. Press `Ctrl+C` to exit the log display; the container will continue running.

Open the following **URL** in your browser:

[http://localhost:**9000**](http://localhost:**9000**?utm_source=chatgpt.com)

[Unable to see the administration tab even though we log in as administrator - SonarQube Server / Community Build - Sonar Community](https://images.openai.com/static-rsc-4/**3GN**-xvt451IyfTKWGU-eQNIKdBpr20zCY0lHMXyt4nJoUhXqVWO-j6OgZ5MxMIbchM1L8VKftuhMKPJ5nNuaWvysdLvoa9MNS-fvcxfgRhVH48wQlOn3sGSW7OF9z4A_HRGkEE8rhgBMyypwdCKzuV7fnITQeO6M1PpOLO1Wbms?purpose=inline)

[community.sonarsource.com](https://community.sonarsource.com/t/unable-to-see-the-administration-tab-even-though-we-log-in-as-administrator/**70488**?utm_source=chatgpt.com)

Default login credentials:

| Field    | Value |
| -------- | ----- |
| Username | admin |
| Password | admin |

SonarQube will ask you to change the default password.

### Step 3: Download the open-source project

Open a terminal:

``` mkdir -p ~/SonarQube-Experiment cd ~/SonarQube-Experiment ```

Clone Spring PetClinic:

``` git clone [https://github.com/spring-projects/spring-petclinic.git](https://github.com/spring-projects/spring-petclinic.git) ```

Enter the project directory:

``` cd spring-petclinic ```

Examine its contents:

``` ls ```

You should find files such as:

- `pom.xml` – Maven project configuration.
- `src/main/java` – Java source files.
- `src/test/java` – Test source files.
- `**README**.md` – Project documentation.

### Step 4: Create a project in SonarQube

## Log in to SonarQube.

## Open the Projects section. ## Select Create Project. ## Choose the option to create a project manually. ## Enter the following details.

| Field                | Value            |
| -------------------- | ---------------- |
| Project display name | Spring PetClinic |
| Project key          | spring-petclinic |
| Main branch          | main             |

## Generate an analysis token.

## Copy the token and keep it private.

[Integrating Quality Gates into Your CI/CD Pipeline: SonarQube Setup Guide | Sonar](https://images.openai.com/static-rsc-4/22BqObMq3DRZ35vpxD6LpQQrov9Y0U21KpnqysfgWLW4V_uphCxCgGVP6VpcKDmuH0EmCg1r19RpWAvUugKoEEitr5ydtCAgu07x1DaT2_goJ2EGPUPDih9zeS9Gvau3-25SbMSHpPtoSC71PvlCWVYt_JOzHSQPDVVxLWu0sbQ?purpose=inline)

[sonarsource.com](https://[www.sonarsource.com/resources/library/integrating-quality-gates-ci-cd-pipeline/?utm_source=chatgpt.com](https://www.sonarsource.com/resources/library/integrating-quality-gates-ci-cd-pipeline/?utm_source=chatgpt.com))

### Step 5: Configure Maven for SonarQube analysis

Spring PetClinic is a Maven project, so we can use the SonarScanner for Maven.

First, check Java and Maven:

``` java -version mvn -version ```

If Maven is missing:

``` sudo apt update sudo apt install maven -y ```

Now build and analyze the project:

```
mvn clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
    -Dsonar.projectKey=spring-petclinic \
    -Dsonar.host.url=[http://localhost:**9000**](http://localhost:**9000**) \
    -Dsonar.token=YOUR_SONAR_TOKEN
```

Replace `YOUR_SONAR_TOKEN` with the token generated in SonarQube.

For a safer approach, avoid putting the token directly into shell history. Store it in an environment variable:

``` export SONAR_TOKEN='your_generated_token' ```

Then execute:

```
mvn clean verify org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
    -Dsonar.projectKey=spring-petclinic \
    -Dsonar.host.url=[http://localhost:**9000**](http://localhost:**9000**) \
    -Dsonar.token=*$SONAR_TOKEN*
```

Note: The first Maven execution may take time because Maven downloads the required dependencies and scanner plugin.

### Step 6: View the analysis results

After successful analysis, return to:

[SonarQube Dashboard](http://localhost:**9000**?utm_source=chatgpt.com)

Open the Spring PetClinic project.

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/getting-started/github?utm_source=chatgpt.com)

Observe the following metrics:

| Metric            | Description                                              |
| ----------------- | -------------------------------------------------------- |
| Bugs              | Coding problems that could cause incorrect behaviour     |
| Vulnerabilities   | Security weaknesses in the code                          |
| Code Smells       | Maintainability problems                                 |
| Code Coverage     | Percentage of code covered by tests                      |
| Duplications      | Repeated source code                                     |
| Security Hotspots | Code requiring security review                           |
| Quality Gate      | Overall assessment against configured quality conditions |

The actual results depend on the source code, scanner version, analysis configuration, and available test reports.

## 6. Demonstration of SonarQube features

This section maps the features mentioned in the experiment syllabus to what SonarQube can actually demonstrate.

### A. Project planning and scheduling

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/managing-your-project-as-developer?utm_source=chatgpt.com)

SonarQube provides project-level dashboards and quality monitoring.

Demonstration:

## Open the Projects page.

## Select Spring PetClinic. ## Observe the project's quality metrics. ## Review its latest analysis. ## Monitor changes in code quality over successive analyses.

Limitation: SonarQube does not provide a native Gantt chart, project calendar, task dependencies, or resource scheduling system.

### B. Product roadmap and release planning

SonarQube helps development teams evaluate whether code meets quality standards before a release.

Demonstration:

## Open the project dashboard.

## Examine its Quality Gate status. ## Review outstanding bugs and vulnerabilities. ## Identify code quality problems that should be resolved before release. ## Run a new analysis after fixing the issues.

For example, a development team can establish the following release criteria:

| Release condition   | Target               |
| ------------------- | -------------------- |
| New bugs            | 0                    |
| New vulnerabilities | 0                    |
| New code smells     | Within defined limit |
| Code coverage       | At least 80%         |
| Quality Gate        | Passed               |

These are example project-defined targets, not universal SonarQube defaults.

Limitation: SonarQube does not provide a complete product roadmap, sprint release calendar, or release backlog.

### C. Task management and team collaboration

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-server/user-guide/issues/retrieving?utm_source=chatgpt.com)

SonarQube helps developers identify and review code-related issues.

Demonstration:

## Open the Issues section.

## Select an identified bug or code smell. ## Examine the issue description. ## Check the affected source file and line number. ## Review the suggested remediation. ## Assign or manage the issue where supported by the edition and permissions.

Developers can use these findings to decide which code quality problems should be fixed first.

Limitation: It is not a replacement for a complete task assignment, team discussion, sprint backlog, or collaboration platform.

### D. Agile and Scrum

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-community-build/user-guide/issues/retrieving/?utm_source=chatgpt.com)

SonarQube can support Agile development by providing continuous feedback during development iterations.

Example Scrum workflow:

| Scrum activity       | SonarQube contribution                              |
| -------------------- | --------------------------------------------------- |
| Sprint planning      | Identify existing technical debt and quality issues |
| Daily Scrum          | Review newly detected code problems                 |
| Sprint development   | Analyze code after changes                          |
| Sprint review        | Demonstrate quality improvements                    |
| Sprint retrospective | Review recurring code quality problems              |

Limitation: SonarQube does not natively provide Scrum ceremonies, sprint boards, story points, product backlogs, or burndown charts.

### E. Time tracking, cost reporting and budgeting

SonarQube provides information about code remediation effort and technical debt.

Demonstration:

## Open the project dashboard.

## Examine maintainability and technical debt metrics. ## Review the effort estimated to fix identified code issues, where available. ## Compare the quality metrics across successive analyses.

Example:

Suppose the project contains technical debt estimated at 20 hours.

If the team allocates 5 hours per week to technical debt reduction, the estimated effort is:

\\[ \text{Weeks required} = \frac{20}{5}=4 \\]

This is a planning calculation, not a native SonarQube budget report.

Limitation: SonarQube does not natively provide employee timesheets, hourly labour costs, project budgets, or financial expenditure reports.

### F. Bug tracking

Core SonarQube capability

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-for-vs-code/using/investigating-issues?utm_source=chatgpt.com)

This is one of the most important features to demonstrate.

SonarQube performs static code analysis and identifies potential bugs in the source code.

Procedure:

## Open Spring PetClinic.

## Navigate to Issues. ## Select the Bugs filter. ## Examine the identified issues. ## Open an individual issue. ## Observe its severity, location, description, and recommended fix. ## Fix the relevant source code. ## Execute the Maven analysis again. ## Check whether the issue has been resolved.

You can also examine:

- Vulnerabilities.
- Code smells.
- Security hotspots.
- Issue severity.
- Issue status.
- Quality Gate status.

Important distinction: SonarQube identifies code defects through static analysis. It is not a general-purpose bug reporting system for users to submit application complaints, feature requests, or support tickets.

## 7. Comparison with other project management tools

We will compare SonarQube with:

## Jira – Agile project and issue management.

## OpenProject – Comprehensive open-source project management.

[Jira Logo .**PNG** and .AI, .**EPS**, .**CDR**, .**PDF**, .**SVG** - iconLogoVector](https://images.openai.com/static-rsc-4/1nl0SQvb00h6We4VPO3tm52nqkIIaOiw94ddsca9Y7u8E_k4TVYDJrPVKuiqITItzmw3qUcxr09fSJBW9NiWz8eTo6dT1TrrLAIngupcZQyPYIlnw6vi6QyP8si5TdAxXIzGigR0TOGzY5pHUen1__H1ht2oDvRUDb_BqqRKtnk?purpose=inline)

Jira

Agile project management and issue tracking

[Official website](https://[www.atlassian.com/software/jira?utm_source=chatgpt.com](https://www.atlassian.com/software/jira?utm_source=chatgpt.com))

[OpenProject Pricing & Reviews **2026** | Techjockey.com](https://images.openai.com/static-rsc-4/Qn6HeNl2IImEL4tZER_wtINiTrF-NarHsHInxJnF12N_wEN61IhRRq-_lsT81g09mg3099eA1RxgwpyWuNo4tjDmqI3JwdxBPtHkmlE5XJaceW0-wLoMywulL9zVkG8gqfqP_RPv-MD7xo6m-A-7VmFdK7akMxEnzd7YMtZVzPE?purpose=inline)

OpenProject

Open-source project and portfolio management

[Official website](https://[www.openproject.org/?utm_source=chatgpt.com](https://www.openproject.org/?utm_source=chatgpt.com))

### Feature comparison

| Feature               | SonarQube                 | Jira                    | OpenProject          |
| --------------------- | ------------------------- | ----------------------- | -------------------- |
| Project planning      | Limited                   | Yes                     | Yes                  |
| Scheduling            | No                        | Yes                     | Yes                  |
| Product roadmap       | Limited quality insights  | Yes                     | Yes                  |
| Task management       | Code issues               | Yes                     | Yes                  |
| Team collaboration    | Limited                   | Yes                     | Yes                  |
| Agile/Scrum           | Supports quality feedback | Yes                     | Yes                  |
| Bug tracking          | Code analysis issues      | Yes                     | Yes                  |
| Time tracking         | Remediation estimates     | Basic/native and apps   | Yes                  |
| Cost reporting        | No                        | Extensions/integrations | Yes                  |
| Budgeting             | No                        | Extensions/integrations | Yes                  |
| Code quality analysis | Yes                       | Through integrations    | Through integrations |
| Security analysis     | Yes                       | Through integrations    | Through integrations |

The comparison describes general product capabilities; exact functionality depends on edition, configuration, and integrations.

### Detailed differences

1\. SonarQube

- Best suited for source code quality and security analysis.
- Identifies bugs, vulnerabilities, and code smells.
- Helps teams maintain coding standards.
- Provides Quality Gates for release quality control.
- Does not replace project planning software.

2\. Jira

- Provides Scrum and Kanban boards.
- Supports backlogs, sprints, epics, and user stories.
- Supports issue assignment and tracking.
- Helps teams plan releases and monitor project progress.
- Can integrate with SonarQube to combine task management and code quality analysis.

3\. OpenProject

- Supports project planning and scheduling through Gantt charts.
- Provides work packages for task and issue management.
- Supports Agile boards and Scrum.
- Provides product roadmaps and release planning.
- Supports time tracking, cost reporting, and budgeting.
- Suitable for organizations looking for an open-source project management solution.

OpenProject's official documentation describes these project lifecycle capabilities, including planning, roadmaps, work packages, Agile boards, time tracking, and budgets.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://www.openproject.org\&sz=32](https://www.google.com/s2/favicons?domain=https://www.openproject.org\&sz=32))

OpenProject+1

### Which tool should be selected?

| Requirement                                 | Recommended tool |
| ------------------------------------------- | ---------------- |
| Source code quality analysis                | SonarQube        |
| Scrum and Agile development                 | Jira             |
| Open-source project management              | OpenProject      |
| Financial project management                | OpenProject      |
| Security and vulnerability analysis         | SonarQube        |
| Comprehensive software development workflow | Jira + SonarQube |

Important observation: SonarQube and Jira/OpenProject are complementary rather than direct substitutes. A development organization can use SonarQube to detect code issues and Jira or OpenProject to assign, schedule, and manage the work required to resolve them.

## 8. Expected practical observations

After completing the experiment, record the following:

| Sr. No. | Observation                                  | Result |
| ------- | -------------------------------------------- | ------ |
| 1       | SonarQube server started successfully        | Yes/No |
| 2       | Spring PetClinic downloaded                  | Yes/No |
| 3       | Project created successfully                 | Yes/No |
| 4       | Maven analysis completed                     | Yes/No |
| 5       | Project dashboard displayed                  | Yes/No |
| 6       | Bugs and code smells examined                | Yes/No |
| 7       | Quality Gate status examined                 | Yes/No |
| 8       | SonarQube compared with Jira and OpenProject | Yes/No |

Record the actual number of bugs, vulnerabilities, code smells, coverage, and duplication shown in your dashboard rather than assuming fixed values.

## 9. Conclusion

SonarQube is a useful software quality management platform that helps developers identify bugs, security vulnerabilities, code smells, and maintainability issues through automated static code analysis.

The experiment demonstrates how an open-source Java application can be integrated with SonarQube using Maven and how its quality metrics can be monitored through a web dashboard.

Compared with Jira and OpenProject, SonarQube focuses primarily on code quality and security rather than complete project management. Jira provides extensive Agile and issue management capabilities, whereas OpenProject provides comprehensive project planning, scheduling, budgeting, time tracking, and collaboration.

Therefore, SonarQube is best used alongside a dedicated project management platform.

## 10. Important commands to remember

| Purpose           | Command                         |
| ----------------- | ------------------------------- |
| Check Docker      | `sudo docker ps`                |
| Start SonarQube   | `sudo docker start sonarqube`   |
| Stop SonarQube    | `sudo docker stop sonarqube`    |
| View logs         | `sudo docker logs sonarqube`    |
| Restart SonarQube | `sudo docker restart sonarqube` |
| Remove container  | `sudo docker rm -f sonarqube`   |
| Check Maven       | `mvn -version`                  |
| Check Java        | `java -version`                 |

Note: Removing the container also removes its internal data if you have not configured persistent volumes. For a longer-term setup, use Docker volumes for SonarQube data, extensions, and logs.

## 11. Screenshots to capture for your practical journal

Capture these screenshots during execution:

## Docker container running SonarQube.

## SonarQube login page. ## Project creation page showing Spring PetClinic. ## Successful Maven analysis in terminal. ## SonarQube project overview dashboard. ## Issues page showing bugs and code smells. ## Quality Gate report. ## Comparison table of SonarQube, Jira, and OpenProject.

## 12. Viva questions and answers

Q1. What is SonarQube?

SonarQube is a platform used for continuous inspection of source code to identify bugs, vulnerabilities, and code smells.

Q2. Is SonarQube a complete project management tool?

No. It is primarily a code quality and security analysis platform. It does not provide complete project scheduling, budgeting, Scrum, or resource management features.

Q3. What is static code analysis?

Static code analysis examines source code without executing the application to identify potential defects and coding problems.

Q4. What is a Quality Gate?

A Quality Gate is a set of conditions that determines whether a project meets specified code quality requirements.

Q5. What is a code smell?

A code smell is a structural or programming practice that may make software difficult to maintain, understand, or modify.

Q6. What is the difference between a bug and a vulnerability?

- Bug: A defect that may cause incorrect application behaviour.
- Vulnerability: A weakness that could potentially be exploited to compromise security.

Q7. What is SonarScanner?

SonarScanner is the analysis component that scans source code and submits the analysis results to the SonarQube server.

Q8. What is the difference between SonarQube and Jira?

SonarQube focuses on source code quality and security, whereas Jira focuses on task management, Agile workflows, project tracking, and collaboration.

Q9. What is technical debt?

Technical debt represents the estimated additional effort required to correct maintainability problems in software.

**Q10**. Can SonarQube be integrated with CI/CD?

Yes. It can be integrated with development pipelines to automatically analyze code during software development and delivery.

## 13. Official references

For additional study and accurate feature verification:

1. [SonarQube official documentation](https://docs.sonarsource.com/sonarqube-server/?utm_source=chatgpt.com).

2. [SonarQube Community Build downloads](https://[www.sonarsource.com/products/sonarqube/downloads/?utm_source=chatgpt.com](https://www.sonarsource.com/products/sonarqube/downloads/?utm_source=chatgpt.com)).&#x20;

   [image](https://[www.google.com/s2/favicons?domain=https://www.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://www.sonarsource.com\&sz=32))

   Sonar

3. [Spring PetClinic source code](https://github.com/spring-projects/spring-petclinic?utm_source=chatgpt.com).

4. [OpenProject documentation](https://[www.openproject.org/docs/?utm_source=chatgpt.com](https://www.openproject.org/docs/?utm_source=chatgpt.com)).

5. [Jira guides](https://[www.atlassian.com/software/jira/guides?utm_source=chatgpt.com](https://www.atlassian.com/software/jira/guides?utm_source=chatgpt.com)).

My recommendation for your laboratory demonstration: Complete the SonarQube practical using Spring PetClinic, but explicitly explain its limitations when discussing project planning, Scrum, and budgeting. This distinction is important because the experiment syllabus lists general project management features that SonarQube does not natively implement. OpenProject is a much closer match to the complete list of required features.
