for filename in *.dat
do
    cut -d , -f 10 $filename
done
