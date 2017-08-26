
## package check
function log_info(){ echo $1;}
sudo echo 'package check start.'

PACKAGES=(python-pip python-dev build-essential python3-yaml)
for package in ${PACKAGES[@]}; do
	dpkg -l $package | grep -E "^i.+[ \t]+$package" > /dev/null
	if [ $? -ne 0 ];then
		m="$package not installed.\nsudo apt-get install -y $package."
		log_info "$m"
		sudo apt-get install -y $package
	else
		m="$package already installed."
		log_info "$m"
	fi
done

sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv 

PACKAGES=(pyyaml selenium)
for package in ${PACKAGES[@]}; do
	sudo pip list | grep $package > /dev/null
	if [ $? -ne 0 ];then
		m="$package not installed.\npip install $package."
		log_info "$m"
		sudo pip install $package
	else
		m="$package already installed."
		log_info "$m"
	fi
done
