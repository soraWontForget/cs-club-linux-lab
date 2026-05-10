# Part 2: Moving Around the Filesystem

By the end of this lab, students should be able to move between directories,
recognize their home directory, use relative directory shortcuts, and inspect a
folder tree before changing locations.

## Commands and Shortcuts

| Command or shortcut | Navigation use |
| --- | --- |
| `cd` | Change directories. |
| `ls` | List files and directories. |
| `ls -l` | List with details. |
| `ls -a` | List all entries, including hidden entries. |
| `ls -la` | List all entries with details. |
| `tree` | Show directories and files as a tree. |
| `.` | The current directory. |
| `..` | The parent directory. |
| `~` | Your home directory. |

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

## Activity 1: Start From the Lab Directory

Run:

```bash
cd /home/student/lab
pwd
ls
```

Checkpoint:

- What directory are you in?
- Which entries are files?
- Which entries are directories?
- Why is `/home/student/lab` an absolute path?

## Activity 2: Compare Listing Styles

Run:

```bash
ls -l
ls -a
ls -la
```

Checkpoint:

- Which command shows permissions, owners, sizes, and dates?
- Which command reveals hidden entries?
- What do `.` and `..` mean in the listing?

## Activity 3: Move Into a Directory

Run:

```bash
cd logs
pwd
ls
ls -la
```

Checkpoint:

- What changed after `cd logs`?
- What files are inside `logs`?
- Which hidden entry appears when you use `ls -la`?

## Activity 4: Move Back Up

Run:

```bash
cd ..
pwd
ls
```

Checkpoint:

- Where did `cd ..` move you?
- Why is `..` useful when you are deep inside folders?

## Activity 5: Jump Home

Run:

```bash
cd ~
pwd
ls
```

Checkpoint:

- What directory does `~` represent?
- Is your home directory the same as the lab directory?

Return to the lab:

```bash
cd ~/lab
pwd
```

## Activity 6: Use Current and Parent Directory Shortcuts

Run:

```bash
ls .
ls ..
cd ./logs
pwd
cd ..
pwd
```

Checkpoint:

- How is `ls .` different from plain `ls`?
- What does `ls ..` show?
- Why does `./logs` work?

## Activity 7: See the Shape With `tree`

Run:

```bash
tree
tree logs
```

Checkpoint:

- How is `tree` different from `ls`?
- Which view is better when you want to understand nested directories?

## Mini Challenge

Use only commands and shortcuts from this lab to answer these questions:

1. What is the absolute path to the lab directory?
2. What command moves into the `logs` directory from the lab directory?
3. What command moves from `logs` back to the lab directory?
4. What command jumps to your home directory?
5. What command lists hidden entries with details?
6. What does `.` mean?
7. What does `..` mean?
8. What does `tree logs` show?

## Exit Ticket

Before leaving, run:

```bash
grade-part2
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One filesystem shortcut that makes sense now.
2. One path or command that still feels confusing.
3. One situation where `tree` is more useful than `ls`.

## Instructor Notes

Suggested timing: 35 to 45 minutes.

Recommended flow:

1. Demo absolute paths with `/home/student/lab`.
2. Demo relative paths with `logs`, `.`, and `..`.
3. Pause after Activity 5 to compare home directory and lab directory.
4. End with `tree` so students can connect movement to structure.

Common student questions:

- `cd` by itself usually moves to the current user's home directory.
- `~` is a shortcut for the current user's home directory.
- `.` is the current directory, and `..` is the directory one level above.
- A path that starts with `/` is absolute.
- A path that does not start with `/` is relative to the current directory.
