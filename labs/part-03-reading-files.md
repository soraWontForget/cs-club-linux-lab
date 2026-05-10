# Part 3: Reading Files

By the end of this lab, students should be able to print a small file, page
through a longer file, preview the beginning and end of logs, count file
contents, and watch a log file with `tail -f`.

## Commands

| Command | File-reading use |
| --- | --- |
| `cat` | Print a file to the terminal. |
| `less` | Open a file one screen at a time. |
| `head` | Show the beginning of a file. |
| `tail` | Show the end of a file. |
| `wc` | Count lines, words, and bytes. |
| `tail -f` | Follow new lines added to a file. |

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

## Activity 1: Print a Short File

Run:

```bash
cat notes.txt
```

Checkpoint:

- Did the whole file fit on your screen?
- When is `cat` useful?
- When might `cat` be annoying?

## Activity 2: Page Through a Longer File

Run:

```bash
less logs/app.log
```

Inside `less`:

- Press `Space` to move down one page.
- Press `b` to move back one page.
- Press `/` to search.
- Press `q` to quit.

Checkpoint:

- Why is `less` better than `cat` for a longer file?
- What search term did you try?
- How do you quit `less`?

## Activity 3: Read the Beginning

Run:

```bash
head logs/app.log
```

Checkpoint:

- How many lines did `head` show by default?
- What was happening at the beginning of the log?

## Activity 4: Read the End

Run:

```bash
tail logs/errors.log
```

Checkpoint:

- How many lines did `tail` show by default?
- What was the most recent error shown?

## Activity 5: Count a File

Run:

```bash
wc notes.txt
```

Checkpoint:

- Which number is the line count?
- Which number is the word count?
- Which number is the byte count?

## Activity 6: Follow a Log

Run:

```bash
tail -f logs/app.log
```

This command keeps running so it can show new lines as they are added to the
file. Press `Ctrl+C` to stop following the log and return to the prompt.

Checkpoint:

- What did the terminal do after you ran `tail -f`?
- Which keys stopped it?
- Why would following a log be useful while debugging?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What command prints `notes.txt`?
2. What command opens `logs/app.log` one page at a time?
3. What command shows the first lines of `logs/app.log`?
4. What command shows the last lines of `logs/errors.log`?
5. What command counts lines, words, and bytes in `notes.txt`?
6. What command follows `logs/app.log` until you stop it?

## Exit Ticket

Before leaving, run:

```bash
grade-part3
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One file-reading command you feel confident using.
2. One command that still feels confusing.
3. One situation where `less`, `head`, `tail`, or `tail -f` would be better
   than `cat`.

## Instructor Notes

Suggested timing: 35 to 45 minutes.

Recommended flow:

1. Start with `cat notes.txt` so students see a small whole-file example.
2. Use `less logs/app.log` to practice pager movement and quitting.
3. Compare `head` and `tail` with the app and error logs.
4. Treat `tail -f` as a controlled demo: students should stop it with
   `Ctrl+C` after observing that it waits for new lines.

Common student questions:

- `cat` does not let you scroll by itself; it just prints the file.
- `less` opens an interactive viewer and returns to the shell when you quit.
- `head` and `tail` show 10 lines by default.
- `tail -f` keeps running until you stop it.
