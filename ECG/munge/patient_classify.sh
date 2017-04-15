#!/bin/bash

DATA_DIR="../data/PTB-mat"
CACHE_DIR="../cache/"
pat2age="$CACHE_DIR/patient_ages"
pat2sex="$CACHE_DIR/patient_sexs"

[ -f $pat2age ] && rm $pat2age
[ -f $pat2sex ] && rm $pat2sex

ls -l $DATA_DIR | grep 'patient' | awk '{print $NF}' | while read line
do
    heaFile=$(ls $DATA_DIR/$line/*.hea | head -n1)
    age=$(cat $heaFile | grep '# age: ' | awk '{print $NF}')
    sex=$(cat $heaFile | grep '# sex: ' | awk '{print $NF}')
    echo $line $age >> $pat2age
    echo $line $sex >> $pat2sex
done

