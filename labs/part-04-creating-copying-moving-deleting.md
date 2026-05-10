# Part 4: Creating, Copying, Moving, and Deleting

By the end of this lab, students should be able to create files and
directories, copy files, rename or move files, and delete files and directories
safely.

## Commands

| Command | File-management use |
| --- | --- |
| `touch` | Create an empty file or update a file timestamp. |
| `mkdir` | Create a directory. |
| `cp` | Copy a file. |
| `mv` | Move or rename a file. |
| `rm` | Remove a file. |
| `rmdir` | Remove an empty directory. |
| `rm -i` | Ask before removing each file. |
| `rm -r` | Remove a directory and its contents recursively. |

## Safety First

Deleting files from the terminal can be permanent. Slow down before using
`rm`, especially with directories.

- Use `rm -i` when you are practicing or unsure.
- Use `rmdir` for empty directories because it refuses to remove directories
  that still contain files.
- Use `rm -r` only on directories you intentionally want to remove.
- Check your current directory with `pwd` before deleting.
- Check the target with `ls` before deleting.

In this lab, only work inside the `practice/` directory you create.

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

## Activity 1: Create a Practice Directory

Run:

```bash
mkdir practice
ls
```

Checkpoint:

- Did `practice` appear in the listing?
- Is `practice` a file or a directory?

## Activity 2: Create an Empty File

Run:

```bash
touch practice/file1.txt
ls -l practice
```

Checkpoint:

- What size is `file1.txt`?
- What does `touch` create when the file does not exist?

## Activity 3: Copy a File

Run:

```bash
cp notes.txt practice/notes-copy.txt
ls -l practice
```

Checkpoint:

- Which file is the original?
- Which file is the copy?
- Did copying remove or change `notes.txt`?

## Activity 4: Rename a File

Run:

```bash
mv practice/file1.txt practice/renamed.txt
ls -l practice
```

Checkpoint:

- Which filename disappeared?
- Which filename appeared?
- Why can `mv` be used for renaming?

## Activity 5: Remove a File Safely

Run:

```bash
rm -i practice/renamed.txt
```

When prompted, type `y` and press `Enter`.

Then run:

```bash
ls -l practice
```

Checkpoint:

- What did `rm -i` ask before deleting?
- Is `renamed.txt` still there?
- Why is confirmation useful?

## Activity 6: Remove an Empty Directory

Run:

```bash
mkdir practice/empty-folder
ls practice
rmdir practice/empty-folder
ls practice
```

Checkpoint:

- Why did `rmdir` work on `empty-folder`?
- What would happen if the directory contained a file?

## Activity 7: Remove a Directory With Contents

Create a small directory tree:

```bash
mkdir practice/remove-me
touch practice/remove-me/temp.txt
ls -l practice/remove-me
```

Remove it:

```bash
rm -r practice/remove-me
ls practice
```

Checkpoint:

- Why was `rm -r` needed here?
- Why should you be careful with `rm -r`?
- What path did you remove?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What command creates a directory named `practice`?
2. What command creates an empty file named `practice/file1.txt`?
3. What command copies `notes.txt` to `practice/notes-copy.txt`?
4. What command renames `practice/file1.txt` to `practice/renamed.txt`?
5. What safer command asks before deleting `practice/renamed.txt`?
6. What command removes an empty directory?
7. What command removes a directory and everything inside it?

## Exit Ticket

Before leaving, run:

```bash
grade-part4
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One file-management command you feel confident using.
2. One deleting command you want to be careful with.
3. One safety habit you will use before deleting files.

## Instructor Notes

Suggested timing: 40 to 50 minutes.

Recommended flow:

1. Emphasize that students should only work inside `practice/`.
2. Demo `rm -i` and make students read the prompt before typing `y`.
3. Compare `rmdir` and `rm -r` after students have created both examples.
4. End by checking that `practice/notes-copy.txt` remains and the temporary
   files/directories have been removed.

Common student questions:

- `touch` does not add text to a file; it creates the file if needed.
- `cp` leaves the original file in place.
- `mv` changes where a file is or what it is named.
- `rmdir` only removes empty directories.
- `rm -r` is powerful because it removes a directory and everything below it.
