#!/bin/bash

# shopt -s nullglob

cur_file="alienDeployments"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="alienMissions"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="alienRaces"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="arcScripts"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="armors"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="enviroEffects"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="facilities"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="research"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="soldiers"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="ufopaedia"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file

cur_file="units"
delete_file=$(echo "delete_$cur_file.rul")
cat_file=$(echo "*$cur_file.yaml")
echo "$cur_file:" > $delete_file
cat $cat_file | grep -v "\[\]" | sed 's/- -/  -/g' | awk 'BEGIN { FS = " "} /-/ { $2 = "delete:"; print "  " $0 }' | sort -u >> $delete_file