# Part 7: File Permissions

By the end of this lab, students should be able to read a file permission
string, identify the owner, group, and others permission sets, check their own
user and group membership, and make a script executable with `chmod`.

## Commands

| Command | Permissions use |
| --- | --- |
| `ls -l` | Show permissions, owner, group, size, and modified time. |
| `id` | Show your user ID, group ID, and group memberships. |
| `groups` | Show the groups your user belongs to. |
| `chmod` | Change file permissions. |
| `chmod +x FILE` | Add execute permission to a file. |

## Permission Strings

`ls -l` shows a permission string at the start of each long listing line.

Example:

```text
-rw-r--r--
```

Read it as:

```text
- rw- r-- r--
  |   |   |
  |   |   +-- others
  |   +------ group
  +---------- owner
```

The first character describes the file type. A regular file usually starts
with `-`. A directory usually starts with `d`.

The next nine characters are three permission sets:

```text
owner | group | others
```

Each set can contain:

```text
r = read
w = write
x = execute
- = permission is missing
```

For a script, `x` means the file can be run as a program.

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

Do not use `sudo` in this lab. You will practice permissions on a file your
user already owns.

## Activity 1: Check Your User and Groups

Run:

```bash
id
groups
```

Checkpoint:

- What is your username?
- What groups does your user belong to?
- Why might groups matter when reading a permission string?

## Activity 2: Inspect a Script

Run:

```bash
ls -l scripts/hello.sh
```

Checkpoint:

- What is the permission string for `scripts/hello.sh`?
- Which three characters belong to the owner?
- Which three characters belong to the group?
- Which three characters belong to others?
- Does the file have `x` permission yet?

## Activity 3: Try to Run the Script

Run:

```bash
./scripts/hello.sh
```

Checkpoint:

- Did the script run?
- If it failed, what error message did you see?
- Which missing permission explains the error?

## Activity 4: Add Execute Permission

Run:

```bash
chmod +x scripts/hello.sh
```

`chmod +x` adds execute permission. It usually does not print anything when it
works.

Checkpoint:

- Why did this command target `scripts/hello.sh`?
- Why did you not need `sudo` for this file?

## Activity 5: Inspect the Script Again

Run:

```bash
ls -l scripts/hello.sh
```

Checkpoint:

- What changed in the permission string?
- Where do you see `x` now?
- Which users can run the script based on the new permission string?

## Activity 6: Run the Script Successfully

Run:

```bash
./scripts/hello.sh
```

Checkpoint:

- Did the script run this time?
- What message did it print?
- What changed between the first run attempt and the second run attempt?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What command shows a long listing for `scripts/hello.sh`?
2. What are the three permission groups after the file type character?
3. What does `r` mean?
4. What does `w` mean?
5. What does `x` mean?
6. What command shows your user and group IDs?
7. What command shows your group names?
8. What command makes `scripts/hello.sh` executable?

## Exit Ticket

Before leaving, run:

```bash
grade-part7
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One part of a permission string you understand now.
2. One permission character that still feels confusing.
3. One reason a script may fail before `chmod +x`.

## Instructor Notes

Suggested timing: 35 to 45 minutes.

Recommended flow:

1. Start with `id` and `groups` so students know who they are before reading
   file ownership and group information.
2. Make students read the `ls -l` output before explaining every column.
3. Let the first `./scripts/hello.sh` attempt fail so the permission problem is
   visible.
4. Use `chmod +x` as the main fix and compare the before/after permission
   strings.
5. Save `chown` and `sudo` for a later administrative commands lesson.

Common student questions:

- The first character is file type, not an owner permission.
- `r`, `w`, and `x` appear in groups of three: owner, group, and others.
- `chmod +x` changes permissions; it does not run the file.
- `./scripts/hello.sh` uses a relative path to run the script from the current
  lab directory.
