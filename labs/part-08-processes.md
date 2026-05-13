# Part 8: Processes and Jobs

By the end of this lab, students should be able to list processes, recognize a
process ID, watch live process activity, pause and resume shell jobs, and stop a
process with `kill`.

## Commands

| Command | Process use |
| --- | --- |
| `ps` | Show processes running in the current terminal session. |
| `top` | Show a live, updating process view. Press `q` to quit. |
| `sleep 100` | Start a command that waits for 100 seconds. |
| `jobs` | Show jobs managed by the current shell. |
| `bg` | Continue a stopped job in the background. |
| `fg` | Bring a job back to the foreground. |
| `kill PID` | Ask a process to terminate by process ID. |

## Processes and Jobs

A process is a running program. Each process has a process ID, usually called a
PID.

A job is a command that your current shell is managing. Jobs have job numbers
such as `[1]`. Job numbers and PIDs are different.

In this lab:

- Use PIDs with `kill`.
- Use `jobs`, `bg`, and `fg` to manage jobs in your current shell.
- Only stop the `sleep 100` process you create.
- Do not use `sudo`.

Helpful keys:

- `Ctrl-Z` suspends the foreground command and returns you to the prompt.
- `Ctrl-C` cancels the foreground command.
- `q` quits `top`.

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

## Activity 1: List Current Processes

Run:

```bash
ps
```

Checkpoint:

- What columns do you see?
- Which column contains the PID?
- Do you see your shell?
- Do you see the `ps` command itself?

## Activity 2: Watch Processes Live

Run:

```bash
top
```

Watch the screen update for a few seconds. Then press `q` to quit.

Checkpoint:

- How is `top` different from `ps`?
- What key did you press to leave `top`?
- Why might a live process view be useful?

## Activity 3: Start and Suspend a Foreground Process

Run:

```bash
sleep 100
```

The command appears to do nothing because it is waiting. While it is waiting,
press `Ctrl-Z` once.

Then run:

```bash
jobs
```

Checkpoint:

- What happened when you pressed `Ctrl-Z`?
- What job number did `jobs` show?
- Does the job say `Stopped`?

## Activity 4: Resume the Job in the Background

Run:

```bash
bg
jobs
```

Checkpoint:

- What changed after `bg`?
- Does the job say `Running`?
- Why did the prompt come back even though `sleep 100` is still active?

## Activity 5: Bring the Job Back to the Foreground

Run:

```bash
fg
```

The `sleep 100` command is now in the foreground again. Press `Ctrl-C` to cancel
it and return to the prompt.

Checkpoint:

- What did `fg` bring back?
- Why did the prompt stop accepting new commands until you pressed `Ctrl-C`?
- What is the difference between a foreground job and a background job?

## Activity 6: Start a Background Process Directly

Run:

```bash
sleep 100 &
jobs
```

The `&` starts the command in the background immediately.

Checkpoint:

- What job number did the shell print?
- What PID did the shell print?
- How is `sleep 100 &` different from plain `sleep 100`?

## Activity 7: Find the PID and Stop the Process

Run:

```bash
ps
```

Find the line for `sleep`. Use the number in the PID column with `kill`.

Run this command, replacing `PID` with the real number from your `ps` output.
Do not type the letters `PID`.

```bash
kill PID
```

Then run:

```bash
jobs
```

Checkpoint:

- Which PID did you use?
- Did the `sleep` job stop?
- Why should you be careful before running `kill`?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What command lists processes in the current terminal session?
2. What does PID stand for?
3. What command shows a live process view?
4. What key quits `top`?
5. What command waits for 100 seconds?
6. What key suspends a foreground command?
7. What command lists jobs in the current shell?
8. What command continues a stopped job in the background?
9. What command brings a job back to the foreground?
10. What command stops a process when you know its PID?

## Exit Ticket

Before leaving, run:

```bash
grade-part8
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One difference between a process and a job.
2. One situation where `top` would be more useful than `ps`.
3. One safety habit you will use before running `kill`.

## Instructor Notes

Suggested timing: 35 to 45 minutes.

Recommended flow:

1. Start with `ps` so students see PID before they need to use one.
2. Keep `top` brief. The goal is recognizing that it updates live and exits
   with `q`.
3. Narrate the difference between `Ctrl-Z` and `Ctrl-C` before students start
   `sleep 100`.
4. Make students compare the job number from `jobs` with the PID from `ps`.
5. Emphasize that `kill PID` should target only the `sleep 100` process they
   created.

Common student questions:

- `sleep 100` is not frozen; it is waiting for 100 seconds.
- `Ctrl-Z` suspends a foreground command. It does not end the process.
- `bg` resumes a stopped job in the background.
- `fg` brings a job back to the foreground.
- A job number such as `[1]` is not the same thing as a PID.
- `kill` usually sends a polite terminate signal. It should still be used
  carefully.
