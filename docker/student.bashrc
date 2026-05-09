export HISTFILE="$HOME/.linux-basics-history"
export HISTSIZE=10000
export HISTFILESIZE=20000
export LAB_HOME="${LAB_HOME:-/opt/linux-basics-lab}"
export MANPAGER=less

shopt -s histappend
PROMPT_COMMAND="history -a; history -n"

alias grade-part1='history -a; "$LAB_HOME"/scripts/grade_part_01_terminal_survival.py --history-file "$HISTFILE"'
alias start-lab='less "$LAB_HOME"/labs/part-01-terminal-survival.md'

cd "$LAB_HOME" || exit

echo "Linux Basics Lab"
echo "Start: start-lab"
echo "Check progress: grade-part1"
