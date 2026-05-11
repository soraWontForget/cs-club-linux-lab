# Part 5: Searching, Filtering, and Pipes

By the end of this lab, students should be able to find files, search inside
files, send output from one command into another command, and use small filters
to organize command output.

## Commands and Operators

| Command or operator | Search and filtering use |
| --- | --- |
| `find` | Search for files and directories. |
| `find . -name "*.txt"` | Find paths by filename pattern. |
| `find . -type f` | Find regular files. |
| `grep` | Print lines that match a pattern. |
| `grep -i` | Search without matching case exactly. |
| `|` | Pipe output from the command on the left into the command on the right. |
| `sort` | Sort lines alphabetically. |
| `uniq` | Collapse repeated neighboring lines. |
| `cut` | Select fields from each line. |

## Before You Start

If you are using the lab container, go to the lab directory:

```bash
cd /home/student/lab
```

If you cloned the repository directly on your computer, move into your clone
instead. The exact path may be different.

## Activity 1: Find Text Files by Name

Run:

```bash
find . -name "*.txt"
```

Checkpoint:

- What does `.` tell `find` to search?
- Which paths ended in `.txt`?
- Why are quotes useful around `*.txt`?

## Activity 2: Find Regular Files

Run:

```bash
find . -type f
```

Checkpoint:

- Did this show directories or only files?
- How is this different from `find . -name "*.txt"`?
- Which files did you recognize from earlier labs?

## Activity 3: Search for Matching Lines

Run:

```bash
grep "ERROR" logs/errors.log
```

Checkpoint:

- How many matching lines did you see?
- Did `grep` print the whole file or only matching lines?
- What kind of problem did one `ERROR` line describe?

## Activity 4: Search Without Matching Case Exactly

Run:

```bash
grep -i "warn" logs/errors.log
```

Checkpoint:

- Why did lowercase `warn` match uppercase `WARN`?
- How is `grep -i` different from plain `grep`?
- When would case-insensitive search be helpful?

## Activity 5: Pipe Into `grep`

Run:

```bash
cat logs/errors.log | grep ERROR
```

The pipe sends the output of `cat logs/errors.log` into `grep ERROR`.

Checkpoint:

- Which command ran before the pipe?
- Which command received the output after the pipe?
- Why is `grep "ERROR" logs/errors.log` shorter for this specific task?

## Activity 6: Sort Search Results

Run:

```bash
find . -name "*.txt" | sort
```

Checkpoint:

- What changed when you added `| sort`?
- Why might sorted output be easier to scan?
- Which command created the list, and which command organized it?

## Activity 7: Select One Field

Run:

```bash
cut -d',' -f1 lab-files/search-practice/incidents.csv
```

Checkpoint:

- What character separates the fields in this file?
- Which field did `-f1` select?
- What repeated values do you see?

## Activity 8: Combine Filters

Run:

```bash
cut -d',' -f1 lab-files/search-practice/incidents.csv | sort | uniq
```

Checkpoint:

- Why does `uniq` work better after `sort`?
- How many unique incident types are in the file?
- Which command selected the field, which sorted it, and which removed
  repeats?

## Mini Challenge

Use only commands from this lab to answer these questions:

1. What command finds every `.txt` file below the current directory?
2. What command finds regular files below the current directory?
3. What command searches `logs/errors.log` for `ERROR`?
4. What command searches `logs/errors.log` for `warn` without caring about
   case?
5. What does the pipe symbol do?
6. What command sorts the output from `find . -name "*.txt"`?
7. What command prints only the first comma-separated field from
   `lab-files/search-practice/incidents.csv`?
8. What pipeline prints each incident type only once?

## Exit Ticket

Before leaving, run:

```bash
grade-part5
```

Use your computer's screenshot tool to capture the terminal window showing your
progress check. Then write three sentences:

1. One search command you feel confident using.
2. One pipe or filter command that still feels confusing.
3. One situation where piping commands together would save time.

## Instructor Notes

Suggested timing: 40 to 50 minutes.

Recommended flow:

1. Start with `find` so students see that search can work on filenames before
   file contents.
2. Compare `grep "ERROR" logs/errors.log` with
   `cat logs/errors.log | grep ERROR` to introduce pipes without implying that
   every `grep` needs `cat`.
3. Use `find . -name "*.txt" | sort` as the first low-stakes pipeline.
4. End with `cut | sort | uniq` so students see a useful multi-step pipeline.

Common student questions:

- `find .` starts searching from the current directory.
- `*.txt` is a filename pattern. Quotes keep the shell from expanding it before
  `find` sees it.
- `grep` prints matching lines, not just matching words.
- `grep -i` ignores uppercase/lowercase differences.
- `uniq` removes repeated neighboring lines, so sorting first usually matters.
