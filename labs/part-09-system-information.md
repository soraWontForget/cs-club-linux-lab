# Part 9: System Information and Environment

By the end of this lab, students should be able to inspect basic system
information, disk usage, memory usage, uptime, environment variables, and the
command search path.

## Commands

| Command | System-information use |
| --- | --- |
| `uname` | Show the operating system name. |
| `df` | Show filesystem disk space. |
| `du` | Show disk usage for files and directories. |
| `free` | Show memory usage. |
| `uptime` | Show how long the system has been running. |
| `env` | Show environment variables. |
| `echo $PATH` | Print the command search path. |

## System Information

These commands report facts about the current Linux system. Output can differ
between computers, containers, and cloud systems. That is normal.

In this lab:

- Use `uname` to identify the operating system.
- Use `df` to read available filesystem space.
- Use `du` to estimate disk usage in the current directory.
- Use `free` to inspect memory.
- Use `uptime` to inspect running time and load average.
- Use `env` and `echo $PATH` to inspect shell environment settings.

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

## Activity 1: Identify the System

Run:

```bash
uname
```

Checkpoint:

- What operating system name did `uname` print?
- Is the output a long description or a short name?
- Why might a command like this be useful before troubleshooting?

## Activity 2: Check Disk Space

Run:

```bash
df
```

Checkpoint:

- What column shows available disk space?
- How much disk space is available inside the container?
- Which filesystem row is mounted on `/`?

## Activity 3: Check Directory Disk Usage

Run:

```bash
du
```

Checkpoint:

- What directories did `du` list?
- Which listed path appears to use the most disk space?
- How is `du` different from `df`?

## Activity 4: Check Memory

Run:

```bash
free
```

Checkpoint:

- What row shows memory?
- What columns show used and free memory?
- Why might memory information help when a system feels slow?

## Activity 5: Check Uptime

Run:

```bash
uptime
```

Checkpoint:

- How long has the system been running?
- How many users are shown?
- What load average values do you see?

## Activity 6: View Environment Variables

Run:

```bash
env
```

Checkpoint:

- What environment variables do you recognize?
- Do you see `HOME`?
- Do you see `PATH`?

## Activity 7: Print the PATH

Run:

```bash
echo $PATH
```

Checkpoint:

- What character separates directories in `PATH`?
- What is one directory listed in your `PATH`?
- Why does the shell need a command search path?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What command shows the operating system name?
2. What command shows filesystem disk space?
3. Which `df` column shows available space?
4. What command estimates disk usage for files and directories?
5. What command shows memory usage?
6. What command shows how long the system has been running?
7. What command prints environment variables?
8. What command prints only the `PATH` value?
9. What character separates directories in `PATH`?

## Exit Ticket

Before leaving, run:

```bash
grade-part9
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. How much disk space is available inside the container.
2. One environment variable you recognize.
3. One difference between `df` and `du`.

## Instructor Notes

Suggested timing: 30 to 40 minutes.

Recommended flow:

1. Remind students that system-information output changes from machine to
   machine.
2. For `df`, focus on the `Available` column and the row mounted on `/`.
3. For `du`, keep the goal simple: it estimates usage for files and directories
   under the current location.
4. For `free`, focus on identifying memory rows and columns, not memorizing
   every number.
5. Use `env` before `echo $PATH` so students see that `PATH` is one environment
   variable among many.

Common student questions:

- `df` reports filesystem space. `du` reports file and directory usage.
- `free` reports memory, not disk space.
- `uptime` includes load averages, which are a quick summary of system demand.
- `PATH` is a colon-separated list of directories the shell searches for
  commands.
- Environment variable names are usually uppercase by convention.
