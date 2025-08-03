#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: backup.sh <src_directory> <target_directory>"
	echo "Please try again"
	exit 1
fi

#chk if rsync is installed
if ! command -v rsync > /dev/null 2&1
then
	echo "the script requires to install it"
	echo "use ur package manager to install it"
	exit 2
fi

curr_date=$(date +%Y-%m-%d)

rsync_opt="-avb --backup-dir $2/curr_date --delete --dry-run"

$(which rsync) $rsync_opt $1 $2/current >> backup_$curr_date.log
