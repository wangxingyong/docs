#!/bin/bash


PWD="/home/leo/work3/work"
regex="/home/leo/work([0-9])"

if [[ $PWD =~ $regex ]] ; then
    echo "from_ip or to_ip has errors!"
	n=${#BASH_REMATCH[*]}
	echo $n
  while [[ $i -lt $n ]] ; do
	  echo "capture[$i]: ${BASH_REMATCH[$i]}"
	  let i++
  done
fi
echo 111

exit 0

TIME=30
if [ $# = 1 ]; then
    TIME=$1
fi
read -n1 -t $TIME -p "Press any key to continue..."
echo

