#!/bin/bash

# run from parent cwd

cur_dir=$(pwd)

rm ./logs/*.log
rm ./output/*.yaml
rm ./output/*.rul

echo $cur_dir

# python3 ./yammler/yammler.py ~/Games/openxcom/user/mods/Piratez
python3 ./yammler/yammler.py ~/Games/openxcom/user/mods/ROSIGMA
# python3 ./yammler/yammler.py ~/Games/openxcom/standard/xcom1 ~/Games/openxcom/user/mods/OXCE_40k ~/Games/openxcom/user/mods/ROSIGMA

exit

cd output
bash ../helpers/sorter.sh

echo "Autogenerated by yammler with xcom1, ROSIGMA and OXCE_40k as arguments" > readme.txt
echo "Last ran: $(date)" >> readme.txt

cd $cur_dir
rm ./logs/*.log
rm ./output/*.yaml