#!/bin/bash
export LANG=C

function grepconf(){
	result=`echo "$2" | grep -E ^"$1":| awk -F ": " '{print $2}'`
	echo `eval echo $result`
}

function getconf(){
	#set PATH of CONFIG_FILE
	if [ ! -z $2 ];then
		CONFIG_FILE=$2
	else
		CONFIG_FILE="../../etc/config.yml"
	fi

	if [ ! -e "$CONFIG_FILE" ];then
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >&2
		echo "[[[FATAL]]]] CONFIG_FILE $CONFIG_FILE NOT exist." >&2
		exit 1
	fi

	confs=`cat $CONFIG_FILE`
	confs=${confs//\<%= ENV[\'/\$}
	confs=${confs//\'] %\>/}

	LOG_LEVEL=`grepconf "loglevel" "$confs"`
	LOG_FILE=`grepconf "logdir" "$confs"``grepconf "logfile" "$confs"`

	if [ $LOG_LEVEL == "DEBUG" ];then
		echo "--------"`date +%Y%m%d%H%M%S` $0 "--------" >> $LOG_FILE;echo -e "[DEBUG] getconf start. ARGV[1]=$1, ARGV[2]=$2, CONFIG_FILE=$CONFIG_FILE, LOG_LEVEL=$LOG_LEVEL, LOG_FILE=$LOG_FILE" >> $LOG_FILE
	fi

	if [ -z "$1" ];then
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[[FATAL]]]] ARGV[1] $1 is empty." >> $LOG_FILE
		exit 1
	fi

	conf=`grepconf "$1" "$confs"`
	if [ -z "$conf" ];then
		echo "--FATAL-- "`date +%Y%m%d%H%M%S` $0"--------" >> $LOG_FILE
		echo "[[[FATAL]]]] getconf [$1] NOT hit." >> $LOG_FILE
		exit 1
	fi
	if [ $LOG_LEVEL == "DEBUG" ];then
		echo "--------"`date +%Y%m%d%H%M%S` $0 "--------" >> $LOG_FILE;echo -e "[DEBUG] return $conf" >> $LOG_FILE
	fi
	echo $conf
	#exit 0
}
