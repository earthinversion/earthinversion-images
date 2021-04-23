!#/bin/bash
for file in *.jpg; 
do 
filebase=`echo ${file} | cut -d"." -f1`;
echo $filebase; 
cwebp -q 80 ${file} -o ${filebase}.webp
done