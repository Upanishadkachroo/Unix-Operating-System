# SVN Experiment — Troubleshooting & Configuration Guide

A practical reference for diagnosing authentication, authorization, and repository-access problems in an offline Subversion (`svnserve`) setup.

---

## 1. Background: Two Separate Issues

The troubleshooting notes cover two distinct problems, plus a verification checklist:

1. **Authentication failure** — `**E170001**: Authentication error from server: Password incorrect` (credentials rejected).
2. **Read-access failure** — `**E220001**: Item is not readable` (authorization / `authz` problem).
3. **Browser access** — why `svn://**127**.0.0.1/TeamProject` does not open as a webpage (and why that's expected).

> **Note:** Authentication (are you who you say you are?) must be fixed **before** authorization (are you allowed to do this?). Fix authentication first, then verify branch-level permissions.

---

## 2. Verifying Authentication

### 2.1 Check `svnserve.conf`

```bash cd ~/**SVN**-Experiment/repositories/TeamProject nano conf/svnserve.conf ```

Ensure these settings are **uncommented** and correct:

```ini [general] anon-access = none auth-access = write password-db = passwd authz-db = authz realm = TeamProject ```

Pay particular attention to:

```ini password-db = passwd ```

It **must** point to the password file inside this repository's `conf` directory.

### 2.2 Verify the exact password-file contents

```bash cat -A conf/passwd ```

Expected:

``` [users]$ leader=Leader123$ coder1=Coder123$ coder2=Coder123$ ```

Check for:

- Duplicate `coder1` / `coder2` entries
- Accidental spaces around usernames or passwords
- Misspelled usernames
- Incorrect capitalization — ****SVN** passwords are case-sensitive**

### 2.3 Inspect the configuration files

Run and share the output of these three commands:

```bash cat conf/svnserve.conf cat -A conf/passwd cat conf/authz ```

This isolates whether the issue is:

- an incorrect password,
- an incorrectly referenced password file, or
- a configuration problem.

---

## 3. Authorization Configuration (`authz`)

### 3.1 Original (insufficient) configuration

```ini [groups] team-leaders = leader coders = coder1,coder2

[TeamProject:/] @team-leaders = rw @coders = r ```

This gives both coders **read-only** access to the entire repository — coders cannot write to their own branches.

### 3.2 Recommended configuration

```ini [groups] team-leaders = leader coders = coder1, coder2

[TeamProject:/] @team-leaders = rw @coders = r

[TeamProject:/trunk] @team-leaders = rw @coders = r

[TeamProject:/branches] @team-leaders = rw @coders = r

[TeamProject:/branches/coder1-feature] @team-leaders = rw coder1 = rw coder2 = r

[TeamProject:/branches/coder2-feature] @team-leaders = rw coder2 = rw coder1 = r

[TeamProject:/tags] @team-leaders = rw @coders = r ```

This preserves read access to the repository while granting each coder **write access to their own branch only**.

### 3.3 Restart the SVN server

```bash pkill svnserve

svnserve -d \
    -r ~/**SVN**-Experiment/repositories \
    --listen-host **127**.0.0.1
```

Verify it is running:

```bash pgrep -a svnserve ```

---

## 4. Testing Authentication (Independent of Committing)

Before retrying commits, test whether the server accepts the credentials — without involving working copies.

**Coder 1:**

```bash
svn list svn://**127**.0.0.1/TeamProject \
    --username coder1 \
    --no-auth-cache
```

Enter password:

``` Coder123 ```

**Coder 2:**

```bash
svn list svn://**127**.0.0.1/TeamProject \
    --username coder2 \
    --no-auth-cache
```

Enter password:

``` Coder123 ```

> **Confirm:** Do these tests accept `Coder123`? This is the key signal that authentication is working.

---

## 5. Testing Repository Read Access (as Leader)

```bash svn list svn://**127**.0.0.1/TeamProject --username leader ```

Expected:

``` branches/ tags/ trunk/ ```

```bash svn log svn://**127**.0.0.1/TeamProject/trunk --username leader ```

Expected output (similar to):

## ```

r2 | leader | ... | 1 line

## Initial project created by team leader

r1 | ... | ... | 1 line

## Create standard SVN directory structure

```

You can also inspect your working copy:

```bash cd ~/**SVN**-Experiment/workspaces/leader-trunk svn info svn status svn log ```

To see files inside the trunk:

```bash svn list svn://**127**.0.0.1/TeamProject/trunk ```

Expected:

``` **README**.md main.cpp ```

---

## 6. Retrying Commits (after authentication succeeds)

You do **not** need to run `svn add` again — both files are already scheduled for addition.

**Coder 1:**

```bash cd ~/**SVN**-Experiment/workspaces/coder1

svn commit --username coder1 \
    --no-auth-cache \
    -m *Coder1 adds calculator module*
```

**Coder 2:**

```bash cd ~/**SVN**-Experiment/workspaces/coder2

svn commit --username coder2 \
    --no-auth-cache \
    -m *Coder2 adds greeting module*
```

---

## 7. Verifying Final Results

As leader:

```bash svn list svn://**127**.0.0.1/TeamProject/branches/coder1-feature svn list svn://**127**.0.0.1/TeamProject/branches/coder2-feature svn log svn://**127**.0.0.1/TeamProject ```

Expected branch contents:

| Coder1 branch  | Coder2 branch |
| -------------- | ------------- |
| README.md      | README.md     |
| main.cpp       | main.cpp      |
| calculator.cpp | greeting.cpp  |

---

## 8. Permission Matrix

This is the key demonstration for the practical:

| Operation                | Team Leader | Coder 1 | Coder 2 |
| ------------------------ | ----------- | ------- | ------- |
| Read trunk               | Allowed     | Allowed | Allowed |
| Commit to trunk          | Allowed     | Denied  | Denied  |
| Read Coder 1 branch      | Allowed     | Allowed | Allowed |
| Commit to Coder 1 branch | Allowed     | Allowed | Denied  |
| Commit to Coder 2 branch | Allowed     | Denied  | Allowed |

### Testing the permissions

Read trunk as Coder 1 (should succeed):

```bash svn list svn://**127**.0.0.1/TeamProject/trunk --username coder1 ```

Attempt a commit to trunk as Coder 1 (should **fail** with an authorization error).

> **Caching caveat:** If a previous authentication session cached credentials, **SVN** may reuse them. Use a fresh terminal, or clear the relevant cached authentication entry, if the displayed username is not the one you intended. Use `--no-auth-cache` to avoid this.

---

## 9. Why the SVN URL Does Not Open in a Browser

This **URL**:

``` svn://**127**.0.0.1/TeamProject ```

is an ****SVN** protocol **URL****, not an **HTTP** website **URL**. A normal browser cannot display an **SVN** repository over this protocol. You interact with it through **SVN** commands:

| Task                     | Command                                         |
| ------------------------ | ----------------------------------------------- |
| List repository contents | `svn list svn://127.0.0.1/TeamProject`          |
| List trunk files         | `svn list svn://127.0.0.1/TeamProject/trunk`    |
| Show repository info     | `svn info svn://127.0.0.1/TeamProject`          |
| View revision history    | `svn log svn://127.0.0.1/TeamProject/trunk`     |

These commands are the correct way to demonstrate an offline **SVN** repository.

### Optional: browsing via a browser

To view **SVN** through a browser, you need an **HTTP** server configuration using **Apache** and **`mod_dav_svn`**, typically at an address such as:

``` [http://localhost/svn/TeamProject/](http://localhost/svn/TeamProject/) ```

This is **optional**. The current `svnserve` setup is sufficient for demonstrating offline **SVN** operations: user authentication, permissions, commits, branches, and merges.

---

## 10. Quick Command Reference

| Purpose                     | Command                                                       |
| --------------------------- | ------------------------------------------------------------- |
| Start server                | `svnserve -d -r ~/SVN-Experiment/repositories --listen-host 127.0.0.1` |
| Stop server                 | `pkill svnserve`                                              |
| Check server                | `pgrep -a svnserve`                                           |
| Check config                | `cat conf/svnserve.conf`                                      |
| Check password file (exact) | `cat -A conf/passwd`                                          |
| Check authorization         | `cat conf/authz`                                              |
| Test auth (no commit)       | `svn list <URL> --username <user> --no-auth-cache`            |
| Commit (no cache)           | `svn commit --username <user> --no-auth-cache -m *<msg>*`     |

---

## 11. Next Steps

## Run the three inspection commands from §2.3 and share their output.

## Report whether the Step 4 authentication tests accept `Coder123`. ## Run the two read-access commands from §5 and share their output.

This will confirm whether the issue is an incorrect password, an incorrectly referenced password file, or a configuration problem — **fix authentication first, then verify branch-level authorization**.
