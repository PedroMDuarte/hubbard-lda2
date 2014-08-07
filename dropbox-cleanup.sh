#!/bin/bash


counter=0
resolved=0
diffprompt=true 
mvprompt=true
mvall=false 
while read -r i;
do
	if [ ! -f "$i" ]; then
		break;
	fi
	echo 
	echo "Found conflicted file:"
	echo "    $i"
        old_file=`echo $i | sed 's/ (.*)//g'`
        echo "    $old_file"
        if [ "$diffprompt" = true ]; then
                echo
		while true; do
		    read -p "...Show diff between the two files [y/n]? (press q to quit, r to stop diff prompts)" yn </dev/tty
		    case $yn in
		        [Yy]* ) diffuse "$i" "$old_file"; break;;
		        [Nn]* ) break;;
		        [Qq]* ) exit;;
		        [Rr]* ) diffprompt=false; break;;
		        * ) echo "Please answer yes or no.";;
		    esac
		done
	fi
	
        if [ "$mvall" = true ]; then
		mv "$i" "$old_file"
        elif [ "$mvprompt" = true ]; then
                echo
		while true; do
		    read -p "...Keep the conflicted version and overwrite the plain version [y/n]? (press q to quit, r to stop mv prompts, a to move all files without prompting again)" yn </dev/tty
		    case $yn in
		        [Yy]* ) mv "$i" "$old_file"; resolved=$((resolved+1)); break;;
		        [Aa]* ) mv "$i" "$old_file"; mvall=true; break;;
		        [Nn]* ) break;;
		        [Qq]* ) exit;;
		        [Rr]* ) mvprompt=false; break;;
		        * ) echo "Please answer yes or no.";;
		    esac
		done
	fi
	counter=$((counter+1))
done <<< "$(find . -name '*(pmd-laptop*2014-08-06)*')"

# please note that my conflict device is called 'pmd-laptop'
# and that the date of the conflict is '2014-08-06'
# replace those in the find string according to your case

echo 
echo "Total number of conflicts = $counter"
echo "Conflicts resolved = $resolved"
