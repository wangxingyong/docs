#!/bin/sh

MYDATE=`date +%F`

cat <<eof
-------------------------------------------------------------------------------
        Select the choice you want to Build      Date:$MYDATE
-------------------------------------------------------------------------------
        1) Build Biz Components
	2) Build Web Components
        3) Build Myalibaba
	4) Update Second Party Library
-------------------------------------------------------------------------------
eof

echo -n "Selection:"

read select

case $select in
	1)
		echo -e " \033[40;32m ------------------ Build Biz Components Begin ----------------------\n \033[40;37m"
		echo -n "Please input biz components which you want to build:"
		read BizComponents
		for BizComponent in $BizComponents
		do
			echo -e " \033[40;32m ------------------ Build intl-biz/$BizComponent Begin ----------------------\n \033[40;37m"
			cd ../../intl-biz/$BizComponents
			antx
			cd ../../intl-myalibaba/all
			echo -e " \033[40;32m ------------------ Build intl-biz/$BizComponent End ----------------------\n \033[40;37m"
		done
		echo -e " \033[40;32m ------------------ Build Biz Components End  ----------------------\n \033[40;37m"
		;;
	2)
		echo -e " \033[40;32m ------------------ Build Web Components Begin ----------------------\n \033[40;37m"
		echo -n "Please input web components which you want to build:"
		read WebComponents
		for WebComponent in $WebComponents
		do
			echo -e " \033[40;32m ------------------ Build intl-web/$WebComponent Begin ----------------------\n \033[40;37m"
			cd ../../intl-web/$WebComponents
			antx
			cd ../../intl-myalibaba/all
			echo -e " \033[40;32m ------------------ Build intl-biz/$WebComponent End ----------------------\n \033[40;37m"
		done
		echo -e " \033[40;32m ------------------ Build Biz Components End  ----------------------\n \033[40;37m"
		;;
	3)
		echo -e " \033[40;32m ------------------ Build Myalibaba Begin ----------------------\n \033[40;37m"
		antx reactor goals=clean,default
		echo -e " \033[40;32m ------------------ Build Myalibaba End  ----------------------\n \033[40;37m"
		;;
	4)
		echo -e " \033[40;32m ------------------ Update Second Party Library Begin ----------------------\n \033[40;37m"
		CurrentDir=`pwd`
		cd ~/.antx/repository.project
		svn up *
		cd $CurrentDir
		;;
	*)
		echo "Bad Selection, Exit!!!" >&2
		;;
esac
