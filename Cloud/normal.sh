#!/bin/bash
for i in {1..10}
do
   wget http://172.30.171.224:8003/frame$i.jpg
done
