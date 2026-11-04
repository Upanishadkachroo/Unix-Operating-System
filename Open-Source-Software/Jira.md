# Experiment: Demonstration of Online Bug Tracking and Management using Jira

## 1. Aim

To study and demonstrate the features of the online bug-tracking and management tool Jira by selecting an open-source software project, identifying at least three bugs or feature improvements, creating and managing bug reports, and comparing Jira with another bug-tracking tool.

## 2. Software requirements

- Web browser and internet connection.
- Jira Software (Atlassian).
- An Atlassian account.
- An open-source project hosted on GitHub.
- Source code editor (optional).

## 3. Introduction to Jira

[Jira Logo .PNG and .AI, .EPS, .CDR, .PDF, .SVG - iconLogoVector](https://images.openai.com/static-rsc-4/1nl0SQvb00h6We4VPO3tm52nqkIIaOiw94ddsca9Y7u8E_k4TVYDJrPVKuiqITItzmw3qUcxr09fSJBW9NiWz8eTo6dT1TrrLAIngupcZQyPYIlnw6vi6QyP8si5TdAxXIzGigR0TOGzY5pHUen1__H1ht2oDvRUDb_BqqRKtnk?purpose=inline)

Jira

Jira is an issue-tracking and project-management platform developed by Atlassian. It is used by software development teams to report bugs, assign tasks, track development progress, manage releases, and improve software quality.

[Official Jira website](https://www.atlassian.com/software/jira?utm_source=chatgpt.com)

### Important features of Jira

1. Issue tracking: Create and track bugs, tasks, stories, and feature requests.
2. Bug reporting: Record bug descriptions, severity, priority, and reproduction steps.
3. Workflow management: Track issues through statuses such as To Do, In Progress, In Review, and Done.
4. Assignment: Assign bugs to developers or team members.
5. Priority management: Classify issues as Highest, High, Medium, Low, etc.
6. Sprint management: Organize development tasks into sprints.
7. Dashboard and reports: Monitor project progress and unresolved bugs.
8. Comments and attachments: Allow team members to discuss issues and upload screenshots or log files.
9. Search and filtering: Find issues using filters and JQL (Jira Query Language).
10. Integration: Connect Jira with GitHub, Bitbucket, CI/CD tools, and other development platforms.

## 4. Selection of open-source project

For this experiment, we select:

[TheAlgorithms C-Plus-Plus · Discussions · GitHub](https://images.openai.com/static-rsc-4/bmlCf-P0oLlTkLIYtrKW0bLQtpWn-lNd4mbqe_nDDp4pvzRF2Q6T8c_qQOE0RFvU-pDRTVhnE0JMF2azsPWfw50AL4NFUsIcclaZ2XcygJhkEoLIAkghkARLcCWEIPw-OpE0qD2AtQtAcPbZHXYmpT13bcBxhpwwvcd3OPAiwsY?purpose=inline)

TheAlgorithms/C-Plus-Plus

Open source

C++ algorithms and data structures repository

[View GitHub repository](https://github.com/TheAlgorithms/C-Plus-Plus?utm_source=chatgpt.com)

Project description:

The repository contains implementations of algorithms and data structures in C++. It is intended for educational purposes and is licensed under the MIT License. It contains implementations of searching, sorting, trees, graphs, dynamic programming, and other algorithms.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



Selected source file:

`data_structures/binary_search_tree2.cpp`

This file implements a generic Binary Search Tree (BST) with operations such as insertion, deletion, searching, finding minimum and maximum elements, and tree traversal.

Source code: [binary_search_tree2.cpp](https://github.com/TheAlgorithms/C-Plus-Plus/blob/master/data_structures/binary_search_tree2.cpp?utm_source=chatgpt.com)

## 5. Identification of three issues

After reviewing the source code, the following three issues are suitable for demonstrating Jira's bug and feature management.

These are proposed issues for the practical exercise, not claims that they are already confirmed or reported upstream bugs. The first is a code-level compatibility defect; the other two are improvement requests.

### Issue 1: BST does not support non-default-constructible data types

Bug / Defect

- Issue ID: BST-1
- Issue type: Bug
- Priority: High
- Component: Binary Search Tree
- Affected file: `binary_search_tree2.cpp`
- Problem: The `bst_node` constructor assigns a value inside its constructor body:

```
explicit bst_node(T _value) {
    value = _value;
    left = nullptr;
    right = nullptr;
}
```

The member `T value` is default-initialized before the constructor body. Therefore, this implementation requires `T` to be default-constructible and assignable.

Expected result: The BST should support types that can be directly constructed from the supplied key, even if they do not have a default constructor.

Proposed solution: Initialize the member directly using a member initializer list.

```
explicit bst_node(T _value)
    : value(std::move(_value)),
      left(nullptr),
      right(nullptr) {}
```

Type: Compatibility / Compile-time defect.

### Issue 2: Add a clear() operation to the BST

Feature Request

- Issue ID: BST-2
- Issue type: New Feature
- Priority: Medium
- Component: Binary Search Tree
- Affected file: `binary_search_tree2.cpp`

Problem: The BST provides insertion, deletion, searching, and traversal operations, but does not expose a public operation to remove all elements at once.

Expected result: The user should be able to clear the entire tree using one function call.

Proposed solution:

```
void clear() {
    root_.reset();
    size_ = 0;
}
```

Type: Functional enhancement / Feature addition.

### Issue 3: Add a height() operation to the BST

Feature Request

- Issue ID: BST-3
- Issue type: New Feature
- Priority: Low
- Component: Binary Search Tree
- Affected file: `binary_search_tree2.cpp`

Problem: The existing implementation provides `size()`, `find_min()`, and `find_max()`, but does not provide a public operation to calculate the height of the tree.

Expected result: The user should be able to calculate the height of the BST to understand its structure and performance characteristics.

Proposed solution:

```
int height(const std::unique_ptr<bst_node>& node) {
    if (!node)
        return -1;

    return 1 + std::max(
        height(node->left),
        height(node->right)
    );
}
```

A public wrapper can call this recursive function using `root_`.

Type: Functional enhancement / Feature addition.

Note: These three tickets demonstrate both defect reporting and feature requests. The proposed implementations are illustrative; a real contribution should also include suitable unit tests and code review.

## 6. Procedure to demonstrate Jira

### Step 1: Create a Jira account

1. Open [Jira official website](https://www.atlassian.com/software/jira?utm_source=chatgpt.com).
2. Click Get it free or the free-plan sign-up option.
3. Register using an email account.
4. Log in to your Atlassian account.
5. Open Jira Software.

[Agile Project Plan Template | Jira Templates](https://images.openai.com/static-rsc-4/-ZWSzCS2L006SmwdVIpOWD-IFvBh7MdB3PUnCBoYnVmudoxWJJ3vVzJLCxXO3lgaSwxfEgZ6ATaPpc6H6f2ZBWQB58KE5yaYzEPReEcqRpDdwgF3NOBoB6hgw-ZWAfJdbQNfHGD2vJ3DXgfRjHvysnABPIoBIzArBmukVm1Pn6w?purpose=inline)

[atlassian.com](https://www.atlassian.com/software/jira/templates/agile-project-plan-template?utm_source=chatgpt.com)

### Step 2: Create a new project

1. Select Projects from the navigation menu.
2. Click Create project.
3. Select the Software Development project category.
4. Select the Kanban template.
5. Enter the project name: `Binary Search Tree Bug Tracking`.
6. Set the project key to `BST`.
7. Click Create project.

The project will be used to manage the issues identified in the open-source source code.

[How to Use Jira for Project Management: A Complete Guide](https://images.openai.com/static-rsc-4/cD5PceJ7C_AFDnTWhhrNeV1r42fYFhO9aCEiDUeWAf7IKmQ3RPaQwV198ckm0l-1kH51k60f-Wg0mbE9k_KikQfChDQieypUnGnYyy5qJkuc5fklvFRuHWzR4OQHfxlDjdC9xZXqxYfQmKgRhSwpsk-JZhfCzUnzkO1Vrjk2pY4?purpose=inline)

[project-management.com](https://project-management.com/how-to-use-jira/?utm_source=chatgpt.com)

### Step 3: Create the first bug

1. Click the Create button in Jira.
2. Select the project `Binary Search Tree Bug Tracking`.
3. Select issue type Bug.
4. Enter the following information:

| Field       | Value                                         |
| ----------- | --------------------------------------------- |
| Summary     | BST fails for non-default-constructible types |
| Issue Type  | Bug                                           |
| Priority    | High                                          |
| Component   | Binary Search Tree                            |
| Description | Explain the constructor compatibility problem |
| Labels      | cpp, compatibility                            |

5\. Click Create.

[Software automation testing-Online Software Testing Tutorial-Jira-management tool-Create Issue](https://images.openai.com/static-rsc-4/Y5QrXwQlAobCR4amSswHCebzXK93qF_oMtEfB4Wa4QPjr6GkbVf7xaJM_OWNGg_-rOM8AlTsuvkkb-fEeHXBjs5_HkI_65Q3zdsrZA6NlqmdiFyh9X4qp49dinfwxTcmMvIRLUh4y9opfwyMTMp0_srmORz5xVhH38KZIw-uzSo?purpose=inline)

[etestinghub.com](https://etestinghub.com/create_issue_jira.php?utm_source=chatgpt.com)

### Step 4: Create the remaining issues

Repeat the same procedure for the other two issues.

| Issue key | Summary                                       | Type               | Priority |
| --------- | --------------------------------------------- | ------------------ | -------- |
| BST-1     | BST fails for non-default-constructible types | Bug                | High     |
| BST-2     | Add clear() operation                         | New Feature / Task | Medium   |
| BST-3     | Add height() operation                        | New Feature / Task | Low      |

If the project does not offer a separate New Feature issue type, use Task and identify it as a feature request in the summary and description.

### Step 5: Assign issues to developers

1. Open an issue.
2. Click the Assignee field.
3. Select a project member.
4. Add a comment describing the required correction.
5. Save the changes.

This allows the project manager to distribute work among developers.

### Step 6: Track issue status

Jira allows issues to move through a workflow.

Example issue workflow

1. To Do

   Bug is reported and waiting for a developer.
2. In Progress

   Developer is investigating and modifying the code.
3. In Review

   Code changes are being reviewed and tested.
4. Done

   Fix or feature is completed and verified.

Move the issues between the available workflow columns by dragging them on the Kanban board or using the issue's status transition controls.

[Master JIRA Agile: Board Types, Sprint Creation & Reporting](https://images.openai.com/static-rsc-4/GB64VcNjXgSaIMDWH1COnOoXPwzZLKVM0agnsaKyL486ICnv8wAklYlVha7_VGNYy9pwKZpT-mXKOH13YQMNtEnrj7pTtp1rU9CKfTpQb9n4MFrZZofa0jOILFfyTsf92cw0iocCnjHbpgqH6-sF4H7qYkAdYjh02z9PwR6HfFw?purpose=inline)

[hevodata.com](https://hevodata.com/learn/jira-agile/?utm_source=chatgpt.com)

### Step 7: View project reports and dashboard

1. Open the project.
2. Select Reports or Dashboards.
3. View the available issue statistics.
4. Check the number of open, in-progress, and completed issues.
5. Use filters to find bugs by priority or assignee.

For example, Jira Query Language (JQL) can be used to find all unresolved bugs:

```
project = BST
AND issuetype = Bug
AND status != Done
ORDER BY priority DESC
```

JQL supports advanced issue searching and filtering.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.atlassian.com\&sz=32)

Atlassian



### Step 8: Integrate Jira with GitHub (optional)

Jira can be connected to GitHub so that development activity can be associated with Jira issues.

1. Open Jira project settings.
2. Find the development tools or integrations section.
3. Select GitHub if the integration is available.
4. Authorize the GitHub account.
5. Connect the selected repository.
6. Include Jira issue keys such as `BST-1` in branch names and commit messages.

Example:

```
git checkout -b BST-1-fix-constructor

git commit -m "BST-1 Fix BST node constructor"

git checkout -b BST-2-add-clear

git commit -m "BST-2 Add clear operation"
```

This helps developers associate source-code changes with reported issues.

## 7. Comparison between Jira and Bugzilla

For comparison, we select Bugzilla.

[Lifecycles Intranet - Life Cycle Assessment Experts - Lifecycles](https://images.openai.com/static-rsc-4/kb6GcgEOQMLJmuC7YEJUvksPd_dWHm4BnxlWZjixaSiqZgwMq_FDAW5ADUahDCBINHMlcllaFOY2b4X93KsdaQa0fOxJWBhTJlwagz5yvYDfNdFve3pCsiiqqhaYMCCblBlBNoOM6zT-HIdkVMYpGr3by9OdlRcHfXs4MvkJL34?purpose=inline)

Jira

Atlassian issue and project management platform

[Bugzilla Pricing & Reviews 2025 | Techjockey.com](https://images.openai.com/static-rsc-4/CIxfvpJgVWaLfpKURXURdGQexKBYVsaMUwLwrjlkG70qDUqHMQsAfza_YhvBAWdCpcAD4sY5xhG6LHwqxys_Mmxc4n4jaRcCLxX4uaPn-MV8VZdR5yZL6PnS3oKqyigCyBxfiPJ2OO0AGWHu94d2JyyQfh8eiECKl1kHjGbjCvU?purpose=inline)

Bugzilla

Open-source defect tracking system

| Feature                 | Jira                                     | Bugzilla                                     |
| ----------------------- | ---------------------------------------- | -------------------------------------------- |
| Primary purpose         | Project and issue management             | Bug and defect tracking                      |
| Interface               | Modern, customizable interface           | More traditional interface                   |
| Issue types             | Bugs, tasks, stories, epics              | Primarily bugs and change requests           |
| Workflow                | Configurable workflows                   | Customizable bug workflow                    |
| Agile support           | Scrum and Kanban boards                  | Limited built-in Agile planning              |
| Priority management     | Multiple priority levels                 | Configurable priorities and severities       |
| Search                  | JQL and basic search                     | Advanced bug search                          |
| Notifications           | Email and application notifications      | User-controlled email notifications          |
| Reports                 | Dashboards, charts and project reports   | Reports, charts and scheduled reports        |
| Customization           | Custom fields, workflows and apps        | Custom fields, workflows and extensions      |
| Source code integration | Integrations with GitHub and other tools | Patch viewer and source-control integrations |
| Licensing               | Commercial cloud offering with free tier | Free and open source                         |

Advantages of Jira:

- Suitable for large software development projects.
- Provides Scrum and Kanban boards.
- Supports sprint planning and project monitoring.
- Provides extensive integrations.
- Allows teams to manage bugs and other development tasks together.

Advantages of Bugzilla:

- Free and open-source defect tracking.
- Powerful bug searching and reporting.
- Automatic duplicate bug detection.
- Customizable bug workflows.
- Detailed bug comments, attachments and notifications.

Bugzilla's official documentation describes its advanced search, reporting, duplicate detection, custom workflows and patch-viewing facilities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.bugzilla.org\&sz=32)

Bugzilla+1



Conclusion of comparison: Jira is more suitable when a team needs complete Agile project management along with bug tracking. Bugzilla is particularly suitable when the primary requirement is detailed defect tracking and management.

## 8. How does bug tracking improve the quality of code?

Bug tracking improves software quality in the following ways:

1. Early detection of defects: Bugs are identified and recorded before they affect the final software product.
2. Systematic resolution: Each bug is assigned to a developer and tracked until it is resolved.
3. Better code reliability: Fixing reported defects reduces unexpected program failures.
4. Improved testing: Bug reports provide test cases that can be reused during regression testing.
5. Accountability: Every issue has an assignee, priority, status and development history.
6. Better collaboration: Developers, testers and project managers can communicate through comments and updates.
7. Reduced development cost: Finding and fixing defects early reduces the cost of correcting them later.
8. Continuous improvement: Historical bug reports help identify recurring problems and weak areas in the codebase.
9. Improved maintainability: Proper documentation of defects and fixes makes future maintenance easier.
10. Release management: Teams can monitor unresolved critical bugs before releasing software.

## 9. Expected result

The following results should be obtained after performing the experiment:

- A Jira account is created successfully.
- A new software project named `Binary Search Tree Bug Tracking` is created.
- Three issues are created for the selected open-source C++ project.
- Each issue is assigned an appropriate type and priority.
- Issues are assigned to developers and tracked using Jira workflows.
- The Kanban board displays the progress of the issues.
- Jira reports and filters are used to monitor the project.

## 10. Conclusion

In this experiment, we studied and demonstrated Jira as an online bug-tracking and project-management tool. We selected the open-source C++ repository TheAlgorithms/C-Plus-Plus and examined its Binary Search Tree implementation.

Three issues were identified for demonstration: one compatibility defect and two feature requests. These issues were entered into Jira, assigned priorities, and managed through a workflow.

We also compared Jira with Bugzilla and studied how systematic bug tracking improves code reliability, maintainability, testing, collaboration, and overall software quality.

Thus, Jira provides an effective platform for managing software defects and development activities throughout the software development life cycle.

## 11. Important screenshots to attach to your practical journal

Capture your own screenshots while performing the experiment. These are the most useful pieces of evidence:

| Screenshot | What it should show                         |
| ---------- | ------------------------------------------- |
| 1          | Jira homepage/dashboard                     |
| 2          | Created BST project                         |
| 3          | BST-1 bug creation form                     |
| 4          | BST-2 feature request                       |
| 5          | BST-3 feature request                       |
| 6          | All three issues in Jira issue list         |
| 7          | Kanban board showing issue statuses         |
| 8          | Issue details showing priority and assignee |
| 9          | Jira reports/dashboard                      |

Reference links

1. [Jira official website](https://www.atlassian.com/software/jira?utm_source=chatgpt.com)
2. [Selected open-source project](https://github.com/TheAlgorithms/C-Plus-Plus?utm_source=chatgpt.com)
3. [Bugzilla features](https://www.bugzilla.org/about/features.html?utm_source=chatgpt.com)
4. [Jira issue types documentation](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/?utm_source=chatgpt.com)

Practical tip: For your demonstration, make sure you actually create the three issues in Jira and capture screenshots of them. The issue descriptions and proposed fixes above can be used directly. Do not present the proposed issues as bugs officially confirmed by the upstream GitHub maintainers.
