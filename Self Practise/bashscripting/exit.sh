#!/bin/bash 

package=htop

sudo apt install $package >> package_install_results.log

#echo "The exit code for the package is: $?"

if [ $? -eq 0 ]; then
	echo "the installation of $package was sucessfull"
	echo "the command is available in:"
	which $package
else
	echo "the package was not insatalled" >> package_failure.log
fi
