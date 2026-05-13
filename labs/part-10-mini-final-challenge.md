# Part 10: Mini Final Challenge

By the end of this lab, students should be able to combine file management,
searching, redirection, backups, and directory listing commands to complete a
small realistic terminal task.

## Commands and Operators You May Need

| Command or operator | Final challenge use |
| --- | --- |
| `mkdir` | Create a directory for the final submission. |
| `grep -i` | Search for matching text without caring about case. |
| `>` | Save command output into a file. |
| `cp` | Make a backup copy of a file. |
| `mv` | Move a file into another directory. |
| `ls -l` | Confirm the final file is in the submission directory. |

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

Do not use `sudo` in this challenge. Everything you need is inside the lab
directory.

## Scenario

A program has been leaving log messages in the `logs/` folder. Your job is to
find the error messages in `logs/app.log`, save them to a new file, make a
backup of that file, and move the file into a `submission/` folder.

## Challenge

Complete these tasks from the lab directory:

1. Create a directory named `submission`.
2. Search `logs/app.log` for lines containing `error`, ignoring uppercase and
   lowercase differences.
3. Save those matching lines in a new file named `errors-found.txt`.
4. Make a backup copy named `errors-backup.txt`.
5. Move `errors-found.txt` into the `submission/` directory.
6. Show a long listing of the `submission/` directory.

Checkpoint:

- Which command created the `submission/` directory?
- Which command searched for error messages?
- Which operator saved the search results into a file?
- Which command made the backup copy?
- Which command moved the original file into `submission/`?
- What file is now inside `submission/`?

## Check Your Work

Your final files should look like this:

```text
errors-backup.txt
submission/errors-found.txt
```

The original `errors-found.txt` should no longer be in the top level of the lab
directory after you move it into `submission/`.

## Exit Ticket

Before leaving, run:

```bash
grade-part10
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One command you reused from an earlier lab.
2. One part of the challenge where combining commands mattered.
3. One thing you would check before submitting files for a real assignment.

## Instructor Notes

Suggested timing: 20 to 30 minutes.

Expected command sequence:

```bash
mkdir submission
grep -i "error" logs/app.log > errors-found.txt
cp errors-found.txt errors-backup.txt
mv errors-found.txt submission/
ls -l submission/
```

Recommended flow:

1. Let students attempt the challenge before showing the expected command
   sequence.
2. Remind students that `grep -i` handles uppercase and lowercase matches.
3. Ask students to explain why `errors-found.txt` moves but
   `errors-backup.txt` stays in the top-level lab directory.
4. Use `ls -l submission/` as the final visual confirmation.

Common student questions:

- `>` creates or replaces the destination file with command output.
- `cp` leaves the original file in place and creates another copy.
- `mv errors-found.txt submission/` places the file inside the existing
  directory.
- `ls -l submission/` lists the contents of the directory, not just the
  directory name.
