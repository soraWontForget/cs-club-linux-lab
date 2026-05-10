export HISTFILE="$HOME/.linux-basics-history"
export HISTSIZE=10000
export HISTFILESIZE=20000
export LAB_HOME="${LAB_HOME:-/home/student/lab}"
export MANPAGER=less

shopt -s histappend
PROMPT_COMMAND="history -a; history -n"

alias grade-part1='history -a; "$LAB_HOME"/scripts/grade_part_01_terminal_survival.py --history-file "$HISTFILE"'
alias grade-part2='history -a; "$LAB_HOME"/scripts/grade_part_02_filesystem_navigation.py --history-file "$HISTFILE"'
alias start-lab='less "$LAB_HOME"/labs/part-01-terminal-survival.md'
alias start-lab1='less "$LAB_HOME"/labs/part-01-terminal-survival.md'
alias start-lab2='less "$LAB_HOME"/labs/part-02-filesystem-navigation.md'

cd "$LAB_HOME" || exit

echo "Linux Basics Lab"
echo "Start Part 1: start-lab1"
echo "Start Part 2: start-lab2"
echo "Check progress: grade-part1 or grade-part2"
