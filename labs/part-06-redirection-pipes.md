# Part 6: Redirection and Pipelines

By the end of this lab, students should be able to send command output into
files, append output without erasing previous content, read input from a file,
save pipeline results, and redirect error messages.

## Commands and Operators

| Command or operator | Redirection and pipeline use |
| --- | --- |
| `>` | Send standard output to a file, replacing the file contents. |
| `>>` | Send standard output to a file, adding to the end. |
| `<` | Read standard input from a file. |
| `|` | Send output from the command on the left into the command on the right. |
| `tee` | Show output on screen and save a copy to a file. |
| `2>` | Send standard error to a file. |

## Safety First

The `>` operator overwrites files. If the file already has content, that
content is replaced.

- Use `>>` when you want to add to a file.
- Use `cat` to inspect a practice file after redirecting output.
- Work only inside `practice/part6/` in this lab.
- Slow down before redirecting into an important file.

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
mkdir -p practice/part6
```

Checkpoint:

- What does `-p` allow `mkdir` to do?
- Why is it useful to keep this lab inside its own directory?

## Activity 2: Save Output to a File

Run:

```bash
date > practice/part6/report.txt
cat practice/part6/report.txt
```

Checkpoint:

- Did `date` print to the screen or go into the file?
- Which operator sent the output into `report.txt`?

## Activity 3: Append Output to the Same File

Run:

```bash
whoami >> practice/part6/report.txt
hostname >> practice/part6/report.txt
cat practice/part6/report.txt
```

Checkpoint:

- Did `>>` erase the date line?
- How is `>>` different from `>`?
- How many lines are in `report.txt` now?

## Activity 4: Overwrite Output Intentionally

Run:

```bash
echo "New report" > practice/part6/report.txt
cat practice/part6/report.txt
```

Checkpoint:

- What happened to the earlier date, username, and hostname lines?
- Why should you be careful with `>`?

## Activity 5: Read Input From a File

Run:

```bash
wc -l < logs/errors.log
```

Then compare it with:

```bash
wc -l logs/errors.log
```

Checkpoint:

- What number did both commands show?
- Which version printed the filename?
- What does `<` give to `wc`?

## Activity 6: Count Matching Lines With a Pipeline

Run:

```bash
grep "ERROR" logs/errors.log | wc -l
```

Checkpoint:

- Which command found the matching lines?
- Which command counted them?
- How many `ERROR` lines are in the file?

## Activity 7: Save Pipeline Output

Run:

```bash
grep "ERROR" logs/errors.log | sort > practice/part6/errors-only.txt
cat practice/part6/errors-only.txt
```

Checkpoint:

- Which command created the matching lines?
- Which command organized them?
- Where did the final output go?

## Activity 8: Show and Save Output With `tee`

Run:

```bash
grep "WARN" logs/errors.log | tee practice/part6/warnings.txt
```

Checkpoint:

- Did the warning lines appear on screen?
- Which file received a saved copy?
- How is `tee` different from `>`?

## Activity 9: Redirect Error Messages

Run:

```bash
ls missing-file 2> practice/part6/error-message.txt
cat practice/part6/error-message.txt
```

Checkpoint:

- Why did `ls missing-file` create an error message?
- Why did the error message go into the file?
- What does the `2` in `2>` represent?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What operator saves standard output to a file and replaces old content?
2. What operator appends standard output to a file?
3. What command saves the current date into `practice/part6/report.txt`?
4. What command appends your username to `practice/part6/report.txt`?
5. What command counts lines in `logs/errors.log` using input redirection?
6. What pipeline counts only `ERROR` lines in `logs/errors.log`?
7. What command saves sorted `ERROR` lines to
   `practice/part6/errors-only.txt`?
8. What command shows `WARN` lines and saves them to
   `practice/part6/warnings.txt`?
9. What operator redirects error messages?

## Exit Ticket

Before leaving, run:

```bash
grade-part6
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One redirection operator you feel confident using.
2. One reason `>` can be risky.
3. One situation where a pipeline plus redirection would save time.

## Instructor Notes

Suggested timing: 40 to 50 minutes.

Recommended flow:

1. Emphasize that `>` overwrites and `>>` appends before students create files.
2. Have students inspect `report.txt` after each redirection so the difference
   is visible.
3. Compare `wc -l < logs/errors.log` with `wc -l logs/errors.log` to show how
   input redirection changes what the command sees.
4. Use `grep | wc -l` as a clear pipeline where each command has one job.
5. End with `2>` so students understand that normal output and error output
   are separate streams.

Common student questions:

- Standard output is normal command output.
- Standard error is where commands send error messages.
- `>` and `>>` affect standard output unless another stream is named.
- `2>` redirects standard error because file descriptor 2 is standard error.
- `tee` is useful when students want to see output and save it at the same
  time.
