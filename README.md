# Linux Basics Lab

Hands-on Linux practice for a community college computer science club.

This repository is organized as a multi-part learning lab. Each part is meant
to be short, practical, and friendly to students who may be using a terminal for
the first time.

## Lab Parts

1. [Terminal Survival](labs/part-01-terminal-survival.md)

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
start-lab
```

Check progress with:

```bash
grade-part1
```

The container is intentionally disposable. When the student exits, command
history and progress disappear with the container.

## Progress Checker

Part 1 includes a history-based progress checker:

```bash
scripts/grade_part_01_terminal_survival.py
```

The Docker image configures the student shell to append history after each
command and provides a `grade-part1` alias. For local testing outside Docker,
you may need to run `history -a` before using the checker.

Students should use their host operating system's screenshot tool to capture
the terminal after running `grade-part1`. The container does not include or need
a screenshot utility.
