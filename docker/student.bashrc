export HISTFILE="$HOME/.linux-basics-history"
export HISTSIZE=10000
export HISTFILESIZE=20000
export LAB_HOME="${LAB_HOME:-/home/student/lab}"
export MANPAGER=less

shopt -s histappend
PROMPT_COMMAND="history -a; history -n"

alias grade-part1='history -a; "$LAB_HOME"/scripts/grade_part_01_terminal_survival.py --history-file "$HISTFILE"'
alias grade-part2='history -a; "$LAB_HOME"/scripts/grade_part_02_filesystem_navigation.py --history-file "$HISTFILE"'
alias grade-part3='history -a; "$LAB_HOME"/scripts/grade_part_03_reading_files.py --history-file "$HISTFILE"'
alias grade-part4='history -a; "$LAB_HOME"/scripts/grade_part_04_file_management.py --history-file "$HISTFILE" --lab-home "$LAB_HOME"'
alias grade-part5='history -a; "$LAB_HOME"/scripts/grade_part_05_searching_filtering.py --history-file "$HISTFILE"'
alias start-lab='less "$LAB_HOME"/labs/part-01-terminal-survival.md'
alias start-lab1='less "$LAB_HOME"/labs/part-01-terminal-survival.md'
alias start-lab2='less "$LAB_HOME"/labs/part-02-filesystem-navigation.md'
alias start-lab3='less "$LAB_HOME"/labs/part-03-reading-files.md'
alias start-lab4='less "$LAB_HOME"/labs/part-04-creating-copying-moving-deleting.md'
alias start-lab5='less "$LAB_HOME"/labs/part-05-searching-filtering-pipes.md'

cd "$LAB_HOME" || exit

echo "Linux Basics Lab"
echo "Start Part 1: start-lab1"
echo "Start Part 2: start-lab2"
echo "Start Part 3: start-lab3"
echo "Start Part 4: start-lab4"
echo "Start Part 5: start-lab5"
echo "Check progress: grade-part1, grade-part2, grade-part3, grade-part4, or grade-part5"
