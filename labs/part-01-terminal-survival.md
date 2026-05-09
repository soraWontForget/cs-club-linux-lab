# Part 1: Terminal Survival

By the end of this lab, students should be able to open a terminal, understand
where they are in the filesystem, list files and folders, clear the screen,
identify the current user and computer, check the date, review command history,
and use built-in help tools.

## Commands

| Command | Survival use |
| --- | --- |
| `pwd` | Print the current directory path. |
| `ls` | List files and directories. |
| `clear` | Clear the terminal screen. |
| `whoami` | Show the current username. |
| `hostname` | Show the computer's network name. |
| `date` | Show the current date and time. |
| `history` | Show recently used commands. |
| `man` | Open a command's manual page. |
| `--help` | Ask many commands for a short help message. |

## Before You Start

Open a terminal and move into this repository:

```bash
cd linux-basics-lab
```

If you cloned the repository somewhere else, use your own path.

## Activity 1: Where Am I?

Run:

```bash
pwd
```

Write down the full path that appears.

Checkpoint:

- What directory are you in right now?
- Is the path absolute or relative?
- What symbol separates each directory name?

## Activity 2: What Is Here?

Run:

```bash
ls
```

Then try:

```bash
ls lab-files
ls lab-files/campus
ls lab-files/campus/clubs
ls lab-files/campus/classes
```

Checkpoint:

- Which entries are files?
- Which entries are directories?
- What clues does your terminal give you?

## Activity 3: Add Detail With Options

Many Linux commands accept options. Options usually start with `-` or `--`.

Try:

```bash
ls -l
ls -a
ls -la
ls -lh lab-files/campus/classes
```

Checkpoint:

- What extra information does `ls -l` show?
- What changes when you add `-a`?
- What does `-h` make easier to read?

## Activity 4: Clean Up Your View

Run several commands, then clear the terminal:

```bash
pwd
ls
date
clear
```

The command history is still saved even though the screen is clear.

## Activity 5: Who and Where?

Run:

```bash
whoami
hostname
date
```

Checkpoint:

- What username are you using?
- What machine are you on?
- Does the displayed time match your local time?

## Activity 6: Command Memory

Run:

```bash
history
```

Find the command number for one command you ran earlier.

Optional challenge:

```bash
!NUMBER
```

Replace `NUMBER` with the command number from your history. Be careful: this
runs that command again.

## Activity 7: Get Help Without Leaving the Terminal

Use short help first:

```bash
ls --help
date --help
whoami --help
```

Then use the manual:

```bash
man ls
```

Inside a `man` page:

- Press `Space` to move down one page.
- Press `b` to move back one page.
- Press `/` to search.
- Press `q` to quit.

Checkpoint:

- Which option lists hidden files?
- Which option shows file sizes in a human-readable format?
- Which help format was easier for you: `--help` or `man`?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What directory are you in?
2. What files and directories are inside `lab-files/campus`?
3. What command shows hidden files?
4. What is your username?
5. What is your computer's hostname?
6. What time did your system report?
7. What was the fifth command in your history list?

## Exit Ticket

Before leaving, write three sentences:

1. One command you feel confident using.
2. One command that still feels confusing.
3. One thing you can do when you forget how a command works.

## Instructor Notes

Suggested timing: 35 to 45 minutes.

Recommended flow:

1. Demo each command briefly.
2. Let students work through the activities in pairs.
3. Pause after Activity 3 to compare `ls` options.
4. End with the mini challenge and exit ticket.

Common student questions:

- `pwd` means "print working directory."
- A directory is another word for a folder.
- Hidden files usually start with a dot, such as `.profile`.
- `man` pages can feel dense. Students do not need to memorize them; they only
  need to learn that help exists locally.
