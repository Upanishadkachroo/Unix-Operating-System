# Experiment: Demonstration of Online Project Management Tool – SonarCloud

## 1. Aim

To study and demonstrate the features of the online project management and code quality tool SonarCloud (now called SonarQube Cloud) using a suitable Free and Open Source Software (**FOSS**) project from GitHub.

The experiment will demonstrate:

## Code coverage analysis.

## Detection of bugs and security vulnerabilities. ## Review of security hotspots. ## Identification of code smells. ## Technical debt measurement and reduction. ## Code quality metrics and analysis history. ## Comparison with other project management tools.

## 2. Introduction to SonarCloud

SonarQube Cloud

Formerly known as SonarCloud, SonarQube Cloud is an online Software-as-a-Service (SaaS) platform developed by SonarSource.

[Open SonarQube Cloud](https://sonarcloud.io/?utm_source=chatgpt.com)

SonarQube Cloud automatically examines source code and provides reports about software reliability, security, and maintainability.

It integrates with GitHub, GitLab, Bitbucket, and Azure DevOps to analyze repositories during the software development process.

Unlike the locally installed SonarQube Server, SonarQube Cloud does not require us to install and maintain a SonarQube server or database on our computer.

### Main features

| Feature                 | Purpose                                                    |
| ----------------------- | ---------------------------------------------------------- |
| Code Coverage           | Measures how much source code is tested                    |
| Bug Detection           | Identifies potential programming defects                   |
| Vulnerability Detection | Finds security weaknesses                                  |
| Security Hotspots       | Identifies security-sensitive code requiring manual review |
| Code Smells             | Identifies maintainability problems                        |
| Technical Debt          | Estimates effort required to fix maintainability issues    |
| Quality Gate            | Evaluates whether code meets quality requirements          |
| Quality History         | Tracks changes in quality metrics over time                |
| CI/CD Integration       | Automatically analyzes code during development             |

SonarQube Cloud uses static analysis to identify issues and security hotspots. Coverage information is imported from an external testing and coverage tool rather than calculated by SonarQube Cloud itself.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+2

## 3. Software requirements

| Component            | Requirement      |
| -------------------- | ---------------- |
| Operating system     | Ubuntu 24.04     |
| Browser              | Chrome / Firefox |
| Online platform      | SonarQube Cloud  |
| Source code hosting  | GitHub           |
| Programming language | Java             |
| Build tool           | Maven            |
| Coverage tool        | JaCoCo           |
| Source code          | Spring PetClinic |
| Internet             | Required         |

No Docker installation or local SonarQube server is required for this experiment.

## 4. Open-source project selected

We will use Spring PetClinic, an open-source Java Spring Boot application.

[Software Architecture - Slidev](https://images.openai.com/static-rsc-4/OVn-JQ7DxJh5pRdyh7EW0fhPZd456OL3NIgVNZyUMdy8dJWxv0LBLExAJl0J_AQxJaNN8J5WcSF8H-**Y0U**-q8wC_HQbzK8_Ju7HMIa30KLzHIymWhifdNfuFnMkQcyM9e2mb42Ag3G95RTxMk1LYxnXo9LFap1a4veRyAYrM2f7U?purpose=inline)

Spring PetClinic

- Language: Java
- Build system: Maven
- Testing: JUnit
- Coverage: JaCoCo
- Repository: [GitHub source code](https://github.com/spring-projects/spring-petclinic?utm_source=chatgpt.com)

### Why Spring PetClinic?

- It is a real open-source application.
- It contains multiple Java classes and packages.
- It includes unit and integration tests.
- It can be built using Maven.
- It is suitable for demonstrating code coverage and static code analysis.
- It allows us to demonstrate changes to source code and their impact on quality metrics.

## 5. Architecture and working

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/discovering-sonarcloud/analysis-process-overview/basic-principles?utm_source=chatgpt.com)

The workflow consists of the following components:

## GitHub: Stores the open-source project and its source code.

## Maven: Builds the Java application and executes tests. ## JaCoCo: Generates code coverage reports. ## SonarScanner: Collects source code analysis and coverage information. ## SonarQube Cloud: Processes the analysis and displays quality metrics. ## Developer: Reviews issues and fixes problems.

The workflow is:

```
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions / CI Pipeline
    |
    v
Maven Build and Unit Tests
    |
    v
JaCoCo Coverage Report
    |
    v
SonarScanner Analysis
    |
    v
SonarQube Cloud
    |
    +---- Bugs
    +---- Vulnerabilities
    +---- Security Hotspots
    +---- Code Smells
    +---- Code Coverage
    +---- Technical Debt
    +---- Quality History
```

## 6. Practical implementation

We will perform the experiment using GitHub and SonarQube Cloud.

The important point is that we will use CI-based analysis, not just automatic analysis, because we need to generate a JaCoCo coverage report and import it into SonarQube Cloud. Automatic analysis does not support importing test coverage reports.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

### Step 1: Create a GitHub account

Open:

[GitHub](https://github.com/?utm_source=chatgpt.com)

Log in to your GitHub account.

### Step 2: Fork Spring PetClinic

Open the original repository:

[Spring PetClinic GitHub repository](https://github.com/spring-projects/spring-petclinic?utm_source=chatgpt.com)

## Click the Fork button.

## Select your GitHub account as the owner. ## Keep the repository name as `spring-petclinic`. ## Click Create fork.

[Version Control with Git: Collaborating - Branching and Pull Requests](https://images.openai.com/static-rsc-4/PvF--E-bcv4WPINwNvDv1r7DPQoKUs91-L9nuIVRgCGIJyaqHHV6U--s27WxHaCTHw4riSsIm4cKNIqOxL4F1bMpJ5QMU6A-wp038ert7sVAUomwrtN_ZmZyb5Jsa9sbQofGr73TMhOm-_5aNq6KulG2lZUyTr8JTe_qkAjg3Vk?purpose=inline)

[hsf-training.github.io](https://hsf-training.github.io/git-novice/instructor/16-collab-branch-and-pr.html?utm_source=chatgpt.com)

Why fork?

A fork creates a copy of the original open-source repository under your GitHub account. This allows you to configure GitHub Actions, modify source code, and connect the repository to SonarQube Cloud without changing the original project.

### Step 3: Create a SonarQube Cloud account

Open:

[SonarQube Cloud](https://sonarcloud.io/?utm_source=chatgpt.com)

## Click Log in or Sign up.

## Select GitHub as the authentication provider. ## Authorize SonarQube Cloud to access GitHub. ## Create or import your organization. ## Select the Free plan if available for your account. ## Import your forked `spring-petclinic` repository.

[Getting started with GitHub | SonarQube Cloud | Sonar Documentation](https://images.openai.com/static-rsc-4/BJBi72SfdyCd29gTXCVf8bICTwNPcynl0lwhoaREc-XxfG4q-DFf8pLJPuEsJdOEoUlzLDvb9Tcf4GO0Qkem6owwuafgxZXZvgfzlMZiZsXAANUck9jDMUuXmzS_9je7mB8oLAar7tj6-9jgMZRrujvVKsd1TRwqpB9sAl5z6E0?purpose=inline)

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/getting-started/github?utm_source=chatgpt.com)

### Step 4: Create the SonarQube Cloud project

## Navigate to Analyze new project.

## Select your GitHub organization. ## Select the `spring-petclinic` repository. ## Click Set Up. ## Choose the new code definition. ## Create the project.

Your project will now be associated with the GitHub repository.

[SonarQube Cloud: Getting Started Developer's Guide | Sonar](https://images.openai.com/static-rsc-4/Um31ffXZ_SQvzt-kzbEtEjxVTst0A3Nnx_seSNtMuDWvBiMXZf8twRjh6wYBNaPrf-SgEzbLw9irmvDJArKFzwwTYB5-1S1VsqWFA8lVG1gNqAdIVM-vzxV1zrweIsYxZA4MCvUH43GncYO8SmW58xtPXdVJgIfPSMCktfpbiWA?purpose=inline)

[sonarsource.com](https://[www.sonarsource.com/resources/library/getting-started-with-sonarqube-cloud/?utm_source=chatgpt.com](https://www.sonarsource.com/resources/library/getting-started-with-sonarqube-cloud/?utm_source=chatgpt.com))

Record these values:

| Parameter        | Example                               |
| ---------------- | ------------------------------------- |
| Organization key | Your organization key                 |
| Project key      | Your generated project key            |
| Repository       | Your GitHub username/spring-petclinic |
| Analysis method  | CI-based analysis                     |

The project key and organization key will be required when configuring the analysis pipeline.

### Step 5: Generate a SonarQube Cloud token

## Open your SonarQube Cloud account.

## Navigate to your account security settings. ## Generate a token for project analysis. ## Copy the token.

[SonarQube Cloud: Getting Started Developer's Guide | Sonar](https://images.openai.com/static-rsc-4/pUzuAQ1LRrHNhIGIg31xJwh2ZZoVttxDoK4qgurt9bnQUA2V6GhSt-2D8RIQmwP8ftrhF6KIKIMB46wxmCyhHoh6Se9VuIfcb1pSECv0KTP5QXt1CLHq-gXeVnEXQqC5QXHd-6NfjaonW_IU7hdSebsjR6td30QTluaIIbYBtJc?purpose=inline)

[sonarsource.com](https://[www.sonarsource.com/resources/library/getting-started-with-sonarqube-cloud/?utm_source=chatgpt.com](https://www.sonarsource.com/resources/library/getting-started-with-sonarqube-cloud/?utm_source=chatgpt.com))

Keep the token private. Do not commit it to GitHub or write it directly into your source code.

### Step 6: Configure GitHub Secrets

Open your forked repository on GitHub.

Navigate to:

Settings → Secrets and variables → Actions → New repository secret

Create the following secret:

| Name          | Value                              |
| ------------- | ---------------------------------- |
| `SONAR_TOKEN` | Token generated in SonarQube Cloud |

This allows GitHub Actions to authenticate with SonarQube Cloud securely.

### Step 7: Clone the repository locally

On your Ubuntu machine:

``` mkdir -p ~/SonarCloud-Experiment cd ~/SonarCloud-Experiment ```

Clone your fork:

``` git clone [https://github.com/YOUR_USERNAME/spring-petclinic.git](https://github.com/YOUR_USERNAME/spring-petclinic.git) ```

Enter the project:

``` cd spring-petclinic ```

Check the files:

``` ls ```

Check Java and Maven:

``` java -version mvn -version ```

If Maven is not installed:

``` sudo apt update sudo apt install maven -y ```

### Step 8: Generate code coverage using JaCoCo

[Getting Code Coverage for e2e tests run on a Java codebase](https://images.openai.com/static-rsc-4/mEeYLMtTDgHoIiFumb_2oVj6VGLcgHDiTw9WkCHAfomtG-q8WswCG-mucL17dByNFLRImjsecArRR8ZxSgIkqWLsWtBNaZJF5Hs0goZVbT_i8lILJZx9nVSqElvVj-**YHL**-4ljxGCk-PoDkodMCF6vlM3bnCky8eHzOMJhiR6kQ4?purpose=inline)

JaCoCo

JaCoCo is a Java code coverage library that measures which instructions, lines, and branches are executed by test cases.

[Official JaCoCo website](https://[www.jacoco.org/jacoco/?utm_source=chatgpt.com](https://www.jacoco.org/jacoco/?utm_source=chatgpt.com))

SonarQube Cloud cannot independently execute test cases to calculate coverage. We therefore use JaCoCo to generate a coverage report and import it.

Open `pom.xml` in your Spring PetClinic repository.

Add the following JaCoCo plugin inside the `build/plugins` section:

```
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.14</version>

    <executions>
    <execution>
    <goals>
    <goal>prepare-agent</goal>
    </goals>
    </execution>

    <execution>
    <id>report</id>
    <phase>verify</phase>
    <goals>
    <goal>report</goal>
    </goals>
    </execution>
    </executions>
</plugin>
```

Save the file.

Run:

``` mvn clean verify ```

After successful execution, JaCoCo should generate:

``` target/site/jacoco/jacoco.xml ```

You can also open the **HTML** coverage report:

``` xdg-open target/site/jacoco/index.html ```

[Adding Test Coverage Badge on GitHub Without Using Third-party Services | HackerNoon](https://images.openai.com/static-rsc-4/8kKu6ejGGEvLgQPMmCRgNzfkSeOJhwQswpFdc4EGmiaAAFRY6l8Fmzr5JPkCSoMoFdJXsjBHfkbwL593be38QzD9tZaGNQzfI90qT21raa796Hzx6knOoYQs5FjwCHjWKKnzvwShbkPCxjeX0ZQ_x5lBxkgkrR8HlsC25xH-gss?purpose=inline)

[hackernoon.com](https://hackernoon.com/adding-test-coverage-badge-on-github-without-using-third-party-services?utm_source=chatgpt.com)

The JaCoCo report provides:

- Instruction coverage.
- Line coverage.
- Branch coverage.
- Method coverage.
- Class coverage.

Important: If the report is missing, check that Maven tests executed and that the JaCoCo `report` goal ran successfully.

### Step 9: Configure SonarQube Cloud analysis

We will configure Maven to submit the source code and JaCoCo report to SonarQube Cloud.

Execute:

```
mvn clean verify \
    org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
    -Dsonar.organization=YOUR_ORGANIZATION_KEY \
    -Dsonar.projectKey=YOUR_PROJECT_KEY \
    -Dsonar.host.url=[https://sonarcloud.io](https://sonarcloud.io) \
    -Dsonar.token=*$SONAR_TOKEN* \
    -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

First, export the token:

``` export SONAR_TOKEN='YOUR_GENERATED_TOKEN' ```

Replace the organization and project keys with the actual values from your SonarQube Cloud project.

After successful execution, SonarQube Cloud receives:

## Java source code.

## Static analysis results. ## JaCoCo coverage report. ## Project quality metrics.

### Step 10: Automate analysis using GitHub Actions

This is an important part of the experiment because it demonstrates continuous code quality monitoring.

Inside the repository, create:

``` .github/workflows/sonarcloud.yml ```

Add the following workflow:

```

name: SonarQube Cloud Analysis

on:
    push:
    branches:
    - main
    pull_request:
    branches:
    - main

jobs:
    sonarcloud:
    name: Build and Analyze
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
    uses: actions/checkout@v4
    with:
    fetch-depth: 0

    - name: Set up Java
    uses: actions/setup-java@v4
    with:
    distribution: temurin
    java-version: '17'
    cache: maven

    - name: Build, test and generate coverage
    run: mvn -B clean verify

    - name: SonarQube Cloud analysis
    env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    run: >
    mvn -B
    org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
    -Dsonar.organization=YOUR_ORGANIZATION_KEY
    -Dsonar.projectKey=YOUR_PROJECT_KEY
    -Dsonar.host.url=[https://sonarcloud.io](https://sonarcloud.io)
    -Dsonar.token=$SONAR_TOKEN
    -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

```

Replace the two placeholder keys with your actual organization and project keys.

Check the Java version specified in the repository's `pom.xml` and Maven configuration. If it requires a different **JDK**, change `java-version` accordingly.

Commit and push:

``` git add pom.xml .github/workflows/sonarcloud.yml

git commit -m *Configure SonarQube Cloud analysis and JaCoCo*

git push origin main ```

Now open:

[GitHub](https://github.com/?utm_source=chatgpt.com) → Your repository → Actions.

You should see the SonarQube Cloud workflow executing.

[GitHub - octodemo-forks/austenstone-actions-playground: Playground for actions · GitHub](https://images.openai.com/static-rsc-4/ElUv9p6iOi8cfOqiLkmlpEQXtMXdBv0PndwzIkDbvHtkbdbKYaY27-L2hphJc-tNG0g9mFX5aaIcHPfxOizinhLJ_oenEsn5HxXWRlW7GUGW04bA6BxFAc8kGBfrJR9B6W9H3SAgasFYNhLQERJZeQJnIcHrh02vLsPc3Y-Cl3c?purpose=inline)

[github.com](https://github.com/octodemo-forks/austenstone-actions-playground/?utm_source=chatgpt.com)

Once the workflow finishes successfully, open your SonarQube Cloud project and examine the results.

## 7. Demonstration of the required SonarQube Cloud features

### A. Code coverage analysis

Required demonstration

[SonarCloud shows zero issues for new code (last 30 days) - SonarQube Cloud - Sonar Community](https://images.openai.com/static-rsc-4/V4ZAyYIBwpIRNuF4dr4nmIpgzt8eNY8-Z2rZGJQ0dM2sqAcQ7e5aSi2qWznUtUDO-43o_VNcqFLtTjgJC0PmYdD19nF1SOsaMgZGcoBXKwUM1bEJmzlKFBLEWBpjx-m6rCiTB7iQ2fnUDLUVFk-eqLR9Ow0wBRtD6DoVRTKb4hU?purpose=inline)

[community.sonarsource.com](https://community.sonarsource.com/t/sonarcloud-shows-zero-issues-for-new-code-last-30-days/**34355**?utm_source=chatgpt.com)

Procedure:

## Open your project dashboard.

## Find the Coverage metric. ## Click the coverage percentage. ## Examine the source files and their coverage. ## Identify files with low coverage. ## Open the JaCoCo report to compare coverage details.

Example:

Suppose a project has **100** executable lines and tests cover 75 lines.

\\[ \text{Coverage}=\frac{75}{**100**}\times100=75\\% \\]

Interpretation:

- Higher coverage indicates more code is exercised by tests.
- Lower coverage identifies code that may require additional testing.
- Coverage alone does not prove that the tests are correct or effective.

Expected observation: SonarQube Cloud displays coverage metrics imported from JaCoCo.

### B. Detect bugs and vulnerabilities

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/getting-started/github?utm_source=chatgpt.com)

Procedure:

## Open your project.

## Navigate to the Issues section. ## Select the Bugs filter. ## Examine the detected issues. ## Select the Vulnerabilities filter. ## Open an individual issue. ## Examine the affected source code, rule description, severity, and recommended fix.

Difference:

| Bugs                           | Vulnerabilities             |
| ------------------------------ | --------------------------- |
| Programming defects            | Security weaknesses         |
| Affect application reliability | Affect application security |
| May cause incorrect output     | May allow exploitation      |
| Example: incorrect logic       | Example: SQL injection      |

SonarQube Cloud identifies issues through language-specific static analysis rules.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

### C. Review Security Hotspots

Required demonstration

[Overview of SonarQube capabilities for code reviewers - **GEANT** Software Development Support - GÉ**ANT** federated confluence](https://images.openai.com/static-rsc-4/opfqRPVW5HD8AnQFTRZuIPoefT4JSPiqJaRYDMyBOXIqvM257Dhf7Z-gIqn64PjUGYojYdAr1FSxX7MIYEAWfdhwL_I8NdUBivcVM-s5IOzvyqP9MUwrKjJlZ8KtJWqpPs4ao8tlbPMOyx7mbK3WF9rSXERICBLBWkEv9Dm2pXI?purpose=inline)

[wiki.geant.org](https://wiki.geant.org/display/**GSD**/Overview%2Bof%2BSonarQube%2Bcapabilities%2Bfor%2Bcode%2Breviewers?utm_source=chatgpt.com)

A Security Hotspot is a piece of security-sensitive code that requires manual examination.

It is not automatically a confirmed vulnerability.

Procedure:

## Open your project.

## Navigate to Security Hotspots. ## Select an identified hotspot. ## Read the What's the risk? section. ## Examine the Are you at risk? section. ## Check the affected source code. ## Determine whether the code is safe or requires correction. ## Update its review status.

Possible review statuses:

| Status    | Meaning                                       |
| --------- | --------------------------------------------- |
| To Review | Requires security examination                 |
| Safe      | Code has been reviewed and is considered safe |
| Fixed     | Security problem has been corrected           |

Example: A security-sensitive method that handles user-controlled input might require review to determine whether the input is validated or sanitized.

The review history also records the status changes and reviewer comments.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

### D. Track Code Smells and fix Technical Debt

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/issues/retrieving?utm_source=chatgpt.com)

A Code Smell is a coding practice that makes software difficult to understand, maintain, or modify.

Examples:

- Duplicate code.
- Unnecessarily complex methods.
- Unused variables.
- Methods that are too long.
- Poor naming conventions.
- Excessive nested conditions.

Procedure:

## Open the Issues section.

## Select Code Smells. ## Examine the identified problems. ## Open an issue. ## Read the explanation and suggested correction. ## Modify the affected Java source file. ## Run the Maven tests again. ## Push the changes to GitHub. ## Wait for the next SonarQube Cloud analysis. ## Compare the number of issues before and after fixing them.

### Understanding Technical Debt

Technical debt is the estimated effort needed to fix maintainability-related issues.

For example, suppose SonarQube estimates that correcting the code smells requires **480** minutes.

\\[ \text{Technical Debt}=\frac{**480**}{60}=8\text{ hours} \\]

If the developer fixes issues estimated at **180** minutes:

\\[ \text{Remaining Debt}=**480**-**180**=**300**\text{ minutes} \\]

This is an illustrative calculation. The actual remediation estimates come from the analysis rules and reported issues.

Technical debt helps developers prioritize maintainability improvements.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

### E. Display Code Quality Metrics

[Code Quality & Security with SonarQube • Mikelopster](https://images.openai.com/static-rsc-4/isVFAHGnQwl9njg6EgI9-CQ5xL04Ux75CB8NDS6RKKXV9ve90c7E5BGTMdH-2OgLv68EvGUtFItOCVuK4xDS6yFVKfoZmKqLip3NG6b523j8gUgi6xCJg6-6Hx1j4IPEvhmHoyqSK49K8VOUWfL4CtZg9rhTqNtFa7lHPS5pF18?purpose=inline)

[mikelopster.dev](https://mikelopster.dev/posts/sonar-code-quality/?utm_source=chatgpt.com)

The Project Health dashboard provides an overview of the quality of the software.

Important metrics:

| Metric                 | Meaning                                        |
| ---------------------- | ---------------------------------------------- |
| Reliability Rating     | Indicates the impact of bugs                   |
| Security Rating        | Indicates the impact of vulnerabilities        |
| Maintainability Rating | Indicates maintainability and technical debt   |
| Coverage               | Percentage of executable code covered by tests |
| Duplications           | Percentage of duplicated code                  |
| Bugs                   | Number of detected bugs                        |
| Vulnerabilities        | Number of detected security vulnerabilities    |
| Code Smells            | Number of maintainability issues               |
| Quality Gate           | Overall pass/fail result                       |

SonarQube uses letter ratings from A to E for several quality dimensions, where A represents the best rating.

Demonstration:

## Open the project dashboard.

## Observe the Reliability Rating. ## Observe the Security Rating. ## Observe the Maintainability Rating. ## Check Code Coverage. ## Check Code Duplication. ## Examine the Quality Gate status.

The dashboard provides an overall view of project quality and allows you to navigate to individual problems.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

### F. View Code Quality Metrics and History

Required demonstration

[docs.sonarsource.com](https://docs.sonarsource.com/sonarqube-cloud/getting-started/first-analysis?utm_source=chatgpt.com)

SonarQube Cloud maintains information about previous project analyses so that developers can understand how code quality changes over time.

Procedure:

## Open your Spring PetClinic project.

## Navigate to the Activity section. ## Observe the previous analysis records. ## Select a metric such as Coverage. ## Examine how coverage has changed over successive analyses. ## Repeat for Bugs, Code Smells, and Duplications. ## Compare the Quality Gate status across analyses.

For a meaningful demonstration, perform at least three analyses:

| Analysis   | Activity                   | Expected observation        |
| ---------- | -------------------------- | --------------------------- |
| Analysis 1 | Initial source code scan   | Initial quality metrics     |
| Analysis 2 | Add or improve unit tests  | Coverage may increase       |
| Analysis 3 | Fix identified code smells | Maintainability may improve |

These are expected experimental trends, not guaranteed results.

You can also compare analysis history before and after committing changes to GitHub.

SonarQube Cloud provides project activity and history to monitor changes in project health.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

## 8. Demonstrating the Quality Gate

A Quality Gate determines whether the project satisfies specified code quality conditions.

[Bugs are not showing in my sonar cloud UI - SonarQube Cloud - Sonar Community](https://images.openai.com/static-rsc-4/C3HpuQl_A-qiK8Ql6vV-Gv5xJlwuBVwI_UVA9AQGvidOl8a5Zao5DFnV6SihbgYM0rxodSpDdLaUPQX1F7P3FKXXotw4zB1dc9tkL89CQjWi55gQBr_naLvdNbXKxhZQgc4lV_E7Qm9kro1DfWEWGrMeDMtHwW-EFavRzFqQWSI?purpose=inline)

[community.sonarsource.com](https://community.sonarsource.com/t/bugs-are-not-showing-in-my-sonar-cloud-ui/**67727**?utm_source=chatgpt.com)

For demonstration, consider these example conditions:

| Quality condition          | Target       |
| -------------------------- | ------------ |
| New bugs                   | 0            |
| New vulnerabilities        | 0            |
| New code coverage          | At least 80% |
| New duplicated lines       | Less than 3% |
| Security hotspots reviewed | 100%         |

These are illustrative targets, not mandatory default settings.

Procedure:

## Open Project Administration.

## Navigate to Quality Gate. ## Examine the assigned Quality Gate. ## Review its conditions. ## Compare the project metrics against the conditions. ## Observe whether the Quality Gate passes or fails.

If the conditions are not satisfied, the project may receive a failed Quality Gate status.

A Quality Gate can also be integrated into GitHub Actions to provide feedback on pull requests and CI builds.&#x20;

[image](https://[www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32](https://www.google.com/s2/favicons?domain=https://docs.sonarsource.com\&sz=32))

Sonar Documentation+1

## 9. Comparison with other Project Management Tools

We will compare SonarQube Cloud with Jira and OpenProject.

[Jira Logo .**PNG** and .AI, .**EPS**, .**CDR**, .**PDF**, .**SVG** - iconLogoVector](https://images.openai.com/static-rsc-4/1nl0SQvb00h6We4VPO3tm52nqkIIaOiw94ddsca9Y7u8E_k4TVYDJrPVKuiqITItzmw3qUcxr09fSJBW9NiWz8eTo6dT1TrrLAIngupcZQyPYIlnw6vi6QyP8si5TdAxXIzGigR0TOGzY5pHUen1__H1ht2oDvRUDb_BqqRKtnk?purpose=inline)

Jira

Website: [Atlassian Jira](https://[www.atlassian.com/software/jira?utm_source=chatgpt.com](https://www.atlassian.com/software/jira?utm_source=chatgpt.com))

Used for Agile project management, task tracking, Scrum, Kanban, and team collaboration.

[OpenProject Pricing & Reviews **2026** | Techjockey.com](https://images.openai.com/static-rsc-4/Qn6HeNl2IImEL4tZER_wtINiTrF-NarHsHInxJnF12N_wEN61IhRRq-_lsT81g09mg3099eA1RxgwpyWuNo4tjDmqI3JwdxBPtHkmlE5XJaceW0-wLoMywulL9zVkG8gqfqP_RPv-MD7xo6m-A-7VmFdK7akMxEnzd7YMtZVzPE?purpose=inline)

OpenProject

Website: [OpenProject](https://[www.openproject.org/?utm_source=chatgpt.com](https://www.openproject.org/?utm_source=chatgpt.com))

Used for project planning, scheduling, Gantt charts, task management, time tracking, and budgeting.

### Feature comparison

| Feature                 | SonarQube Cloud  | Jira                   | OpenProject            |
| ----------------------- | ---------------- | ---------------------- | ---------------------- |
| Project planning        | Limited          | Yes                    | Yes                    |
| Project scheduling      | No               | Yes                    | Yes                    |
| Product roadmap         | Limited          | Yes                    | Yes                    |
| Task management         | Code issues      | Yes                    | Yes                    |
| Team collaboration      | Limited          | Yes                    | Yes                    |
| Agile/Scrum             | Quality feedback | Yes                    | Yes                    |
| Bug tracking            | Code defects     | Yes                    | Yes                    |
| Code coverage           | Yes              | Through integration    | Through integration    |
| Vulnerability detection | Yes              | Through integration    | Through integration    |
| Security hotspots       | Yes              | Through integration    | Through integration    |
| Code smells             | Yes              | Through integration    | Through integration    |
| Technical debt          | Yes              | Through integration    | Through integration    |
| Quality history         | Yes              | Limited / integrations | Limited / integrations |
| Time tracking           | No               | Apps/integrations      | Yes                    |
| Cost reporting          | No               | Apps/integrations      | Yes                    |
| Budgeting               | No               | Apps/integrations      | Yes                    |

### Detailed comparison

1\. SonarQube Cloud

- Cloud-based code quality platform.
- Automatically analyzes source code.
- Detects bugs and vulnerabilities.
- Identifies security hotspots.
- Measures code coverage using imported reports.
- Tracks code smells and technical debt.
- Provides Quality Gates and analysis history.

2\. Jira

- Provides Scrum and Kanban boards.
- Supports sprint planning.
- Allows developers to create and assign tasks.
- Supports bug tracking and issue management.
- Provides project progress reporting.
- Can integrate with SonarQube Cloud.

3\. OpenProject

- Supports project scheduling and Gantt charts.
- Provides work packages for task management.
- Supports Agile boards and Scrum.
- Offers time tracking.
- Supports cost reporting and budgeting.
- Provides project roadmaps and collaboration features.

### Which tool is best?

| Requirement                      | Best suited tool |
| -------------------------------- | ---------------- |
| Code quality analysis            | SonarQube Cloud  |
| Security vulnerability detection | SonarQube Cloud  |
| Code coverage monitoring         | SonarQube Cloud  |
| Agile and Scrum management       | Jira             |
| Task and team management         | Jira             |
| Open-source project management   | OpenProject      |
| Project scheduling               | OpenProject      |
| Time and cost management         | OpenProject      |

Important observation: SonarQube Cloud is not a complete project management replacement. It is primarily a code quality and security management platform. Jira and OpenProject are more suitable for managing the overall software project lifecycle.

A practical software development workflow can use Jira for task management and SonarQube Cloud for code quality analysis.

## 10. Expected observations

Record the actual results obtained from your SonarQube Cloud dashboard.

| Sr. No. | Experiment                      | Observation               |
| ------- | ------------------------------- | ------------------------- |
| 1       | GitHub repository imported      | Successful / Unsuccessful |
| 2       | SonarQube Cloud project created | Successful / Unsuccessful |
| 3       | JaCoCo report generated         | Yes / No                  |
| 4       | SonarQube analysis completed    | Yes / No                  |
| 5       | Code coverage displayed         | Yes / No                  |
| 6       | Bugs identified                 | Number: \_\_\_\_\_        |
| 7       | Vulnerabilities identified      | Number: \_\_\_\_\_        |
| 8       | Security hotspots reviewed      | Number: \_\_\_\_\_        |
| 9       | Code smells identified          | Number: \_\_\_\_\_        |
| 10      | Technical debt examined         | \_\_\_\_\_ minutes        |
| 11      | Quality Gate examined           | Passed / Failed           |
| 12      | Code quality history examined   | Yes / No                  |

## 11. Conclusion

SonarQube Cloud is an effective online platform for automated source code quality and security analysis.

In this experiment, we integrated an open-source Java application, Spring PetClinic, with SonarQube Cloud through GitHub. Maven was used to build the application and execute tests, while JaCoCo generated code coverage reports.

The experiment demonstrated the detection of bugs and vulnerabilities, review of security hotspots, identification of code smells, measurement of technical debt, and monitoring of code quality metrics and analysis history.

The comparison showed that SonarQube Cloud focuses on code quality and security, whereas Jira and OpenProject provide more comprehensive project planning, scheduling, task management, Agile development, and collaboration features.

Therefore, SonarQube Cloud is best used as a complementary tool alongside conventional project management software.

## 12. Viva questions and answers

Q1. What is SonarCloud?

SonarCloud, now called SonarQube Cloud, is an online code quality and security analysis platform that identifies bugs, vulnerabilities, and code smells.

Q2. What is the difference between SonarQube Server and SonarQube Cloud?

- SonarQube Server is self-hosted and requires infrastructure management.
- SonarQube Cloud is hosted online and managed by SonarSource.

Q3. What is JaCoCo?

JaCoCo is a Java code coverage tool that measures how much source code is executed during testing.

Q4. What is code coverage?

Code coverage is the percentage of executable source code exercised by test cases.

Q5. What is a security hotspot?

A security hotspot is a security-sensitive section of code that requires manual review to determine whether it introduces a security risk.

Q6. What is technical debt?

Technical debt is the estimated additional development effort required to fix maintainability issues in software.

Q7. What is a Quality Gate?

A Quality Gate is a set of conditions used to determine whether a project meets predefined code quality standards.

Q8. What is the difference between a bug and a code smell?

A bug can cause incorrect program behaviour, whereas a code smell indicates poor code structure or maintainability.

Q9. Why is GitHub integration required?

GitHub stores the source code and enables SonarQube Cloud to analyze repository changes and integrate with CI/CD workflows.

**Q10**. Can SonarQube Cloud calculate code coverage independently?

No. It imports coverage reports generated by external tools such as JaCoCo.

**Q11**. What is the purpose of GitHub Actions?

GitHub Actions automates tasks such as building, testing, and analyzing source code whenever specified repository events occur.

**Q12**. Which is better: SonarQube Cloud or Jira?

They serve different purposes. SonarQube Cloud focuses on code quality and security, while Jira focuses on project management and Agile issue tracking.

## 13. Official references

1. [SonarQube Cloud documentation](https://docs.sonarsource.com/sonarqube-cloud/?utm_source=chatgpt.com).
2. [GitHub integration guide](https://docs.sonarsource.com/sonarqube-cloud/getting-started/github?utm_source=chatgpt.com).
3. [Code coverage documentation](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/overview?utm_source=chatgpt.com).
4. [Security hotspot review guide](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/issues/reviewing-security-hotspots?utm_source=chatgpt.com).
5. [Project history documentation](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/managing-project-history?utm_source=chatgpt.com).
6. [Spring PetClinic GitHub repository](https://github.com/spring-projects/spring-petclinic?utm_source=chatgpt.com).
7. [JaCoCo documentation](https://[www.jacoco.org/jacoco/?utm_source=chatgpt.com](https://www.jacoco.org/jacoco/?utm_source=chatgpt.com)).

## 14. Screenshots required for the practical journal

Capture these screenshots in sequence:

[Containerize a Spring Boot application with Podman Desktop | Red Hat Developer](https://images.openai.com/static-rsc-4/AnGOca_4P_7-ovqFjai4k_aX8ap2oyK1xa_gg9egpF7eh0Lg_8mmPTeNY1cEppE_PG1qIVGlTvHYwAGOfdmJUpEwiUP0FCfHrfjiV_znuU-NXlFtBFTxzID720QKrcTVJFwbOymtUP0EMiQugNXf3OFlcNl_iP10yZPdUpHYPwg?purpose=inline)

1\. GitHub repository

Forked Spring PetClinic repository under your GitHub account.

2\. SonarQube Cloud project setup

Organization and imported repository.

[Toggle Coverage Example at Anna Beyers blog](https://images.openai.com/static-rsc-4/ekX0M7n_dwDnYb7L0XL5e0uqyHZcsq5E7CjQ_sP8pvQ91PBOOk7WuxPwM3P3PrDf9UixL6S6TxDvu7d_0I5qWxHA2UxkueL9q9U1EY0HNc3LAprab_a6EwSZ5bxjBAZJjWimF_kCGNAt5p2gWGVTeNyb81M5EwdshDwbv9LkWeg?purpose=inline)

3\. JaCoCo report

Coverage report generated after Maven testing.

[Project health dashboard is now your default landing page! - Announcements - Sonar Community](https://images.openai.com/static-rsc-4/YqiBiPqEzBfHvpX8cvAPvyir4YftGrTwyC5t9jJUkGqsnhbtUdC2k4RoBWao0qzVPX5ig4hpSuuVA_QGM6vgC6053aqeHFCu9idM8yKf9EPta67khDBnZvKm9XG5AM98S3BNMhxY7aA9Q1e-6VYz45fu0pYwR3BYFQzXoKfjOHM?purpose=inline)

4\. Project dashboard

Coverage, ratings, and Quality Gate.

[SonarCloud – Features, Pricing & Reviews **2026** | Krowdbase](https://images.openai.com/static-rsc-4/ixZPbPcLIPxsxbx2q7Yl2-i0fuo_otOvZSN3NvSuFGtm-ycop3KL31DOl3CzjPI0qWQtnh_55a1OTwGUjcUHkoDhu5UhJ-9tti5zKyP0pxt-vQ2uJb8ElVT6eAX8LGuxZqGEg3ofPabloGc6IDBWLHCLB7wk8Ch-QTqoVuvH5bg?purpose=inline)

5\. Bugs and vulnerabilities

Detected issues and their descriptions.

[Security Hotspots: a dedicated space to perform efficiently your security reviews - Announcements - Sonar Community](https://images.openai.com/static-rsc-4/yLV3Qe8Fu0mUW15T-cvmFaQ7mthSnMHOS0fM707nAgynMvCJXkxOEZIFn8LAYRtbZ0AvCZzOAqlAzbNHsLjD1_Fq7_hSNkOjUnUAm8HGEiWFHRKkHv5eMDOcQy6ccTNuV9Xb9AMEWIdwV8f2QpClZOK9mfGzvdsce-cBBIf3bw0?purpose=inline)

6\. Security Hotspots

Hotspot details and review status.

7\. Code smells and technical debt

Identified maintainability issues.

8\. Project activity and history

Quality metrics across multiple analyses.

Practical tip: For your demonstration, the most important evidence is the comparison between the first analysis and a later analysis after improving tests or fixing code smells. That proves you have actually used the platform rather than simply displaying its dashboard.
