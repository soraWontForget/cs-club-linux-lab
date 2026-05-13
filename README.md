# Linux Basics Lab

Hands-on Linux practice for a community college computer science club.

This repository is organized as a multi-part learning lab. Each part is meant
to be short, practical, and friendly to students who may be using a terminal for
the first time.

## Lab Parts

- Part 1: [Terminal Survival](labs/part-01-terminal-survival.md)
- Part 2: [Moving Around the Filesystem](labs/part-02-filesystem-navigation.md)
- Part 3: [Reading Files](labs/part-03-reading-files.md)
- Part 4: [Creating, Copying, Moving, and Deleting](labs/part-04-creating-copying-moving-deleting.md)
- Part 5: [Searching, Filtering, and Pipes](labs/part-05-searching-filtering-pipes.md)
- Part 6: [Redirection and Pipelines](labs/part-06-redirection-pipes.md)
- Part 7: [File Permissions](labs/part-07-file-permissions.md)
- Part 8: [Processes and Jobs](labs/part-08-processes.md)

## Part 1: Terminal Survival

Students learn the first commands they need to survive in a Linux terminal:

- `pwd`
- `ls`
- `clear`
- `whoami`
- `hostname`
- `date`
- `history`
- `man`
- `--help`

This part focuses on confidence, orientation, and basic directory awareness:
Where am I? What is here? How do I ask the system for help?

## Part 2: Moving Around the Filesystem

Students learn how to move through the filesystem and inspect directory
structure:

- `cd`
- `ls`
- `ls -l`
- `ls -a`
- `ls -la`
- `tree`
- `.`
- `..`
- `~`

## Part 3: Reading Files

Students learn how to inspect file contents from the terminal:

- `cat`
- `less`
- `head`
- `tail`
- `wc`
- `tail -f`

## Part 4: Creating, Copying, Moving, and Deleting

Students learn basic file management and safer deletion habits:

- `touch`
- `mkdir`
- `cp`
- `mv`
- `rm`
- `rmdir`
- `rm -i`
- `rm -r`

## Part 5: Searching, Filtering, and Pipes

Students learn how to locate files, search inside files, and connect commands
with pipes:

- `find`
- `find . -name "*.txt"`
- `find . -type f`
- `grep`
- `grep -i`
- `|`
- `sort`
- `uniq`
- `cut`

## Part 6: Redirection and Pipelines

Students learn how to control where command output and error messages go:

- `>`
- `>>`
- `<`
- `|`
- `tee`
- `2>`

## Part 7: File Permissions

Students learn how to read permission strings, connect permissions to their
user and groups, and make a script executable:

- `ls -l`
- `id`
- `groups`
- `chmod`
- `chmod +x`
- `./scripts/hello.sh`

## Part 8: Processes and Jobs

Students learn how to inspect processes, use shell job control, and stop a
process by PID:

- `ps`
- `top`
- `sleep 100`
- `jobs`
- `fg`
- `bg`
- `kill PID`

## Setup

### Local Clone

```bash
git clone <REPO_URL>
cd linux-basics-lab
```

Then start with:

```bash
less labs/part-01-terminal-survival.md
```

If students are not comfortable with `less` yet, they can open the file in a
browser or editor instead.

### Disposable Docker Lab

Build the image:

```bash
docker build -t linux-basics-lab .
```

Start a fresh disposable lab:

```bash
docker run --rm -it linux-basics-lab
```

If you want `date` inside the container to use a specific timezone, pass `TZ`:

```bash
docker run --rm -it -e TZ=America/Los_Angeles linux-basics-lab
```

Inside the container, start Part 1 with:

```bash
start-lab1
```

Start Part 2 with:

```bash
start-lab2
```

Start Part 3 with:

```bash
start-lab3
```

Start Part 4 with:

```bash
start-lab4
```

Start Part 5 with:

```bash
start-lab5
```

Start Part 6 with:

```bash
start-lab6
```

Start Part 7 with:

```bash
start-lab7
```

Start Part 8 with:

```bash
start-lab8
```

Check progress with:

```bash
grade-part1
grade-part2
grade-part3
grade-part4
grade-part5
grade-part6
grade-part7
grade-part8
```

The container is intentionally disposable. When the student exits, command
history and progress disappear with the container.

## Progress Checkers

Each part includes a history-based progress checker:

```bash
scripts/grade_part_01_terminal_survival.py
scripts/grade_part_02_filesystem_navigation.py
scripts/grade_part_03_reading_files.py
scripts/grade_part_04_file_management.py
scripts/grade_part_05_searching_filtering.py
scripts/grade_part_06_redirection_pipes.py
scripts/grade_part_07_permissions.py
scripts/grade_part_08_processes.py
```

The Docker image configures the student shell to append history after each
command and provides `grade-part1`, `grade-part2`, `grade-part3`,
`grade-part4`, `grade-part5`, `grade-part6`, `grade-part7`, and `grade-part8`
aliases. For local testing outside Docker, you may need to run `history -a`
before using a checker.

Students should use their host operating system's screenshot tool to capture
the terminal after running the relevant `grade-part` command. The container
does not include or need a screenshot utility.
