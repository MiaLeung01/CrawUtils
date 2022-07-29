
# # 在Resource目录下执行
# cat cwords.txt | while read line
# do
#   $line
# done
# rm video/*.mp4
# cat cwords.txt | while read line
# do
#   cm=$(echo $line | grep -E "([a-zA-Z_-]+\.mp3)" -o )
#   jp=$(echo $line | grep -E "([a-zA-Z_-]+\.mp3)" -o | sed -s "s/.mp3/.jpg/g")
#   name=$(echo $line | grep -E "([a-zA-Z_-]+\.mp3)" -o | sed -s "s/.mp3//g")
#   echo  $jp
#   # ffmpeg -framerate 1 -i './wordcard/bing/'$jp -i './audio/bing/br/'$name'.mp3' -shortest -c:v libx264 -r 30 -pix_fmt yuv420p -y './video/'$name'.mp4'
#   ffmpeg -framerate 1 -i './wordcard/bing/'$jp -i './audio/bing/br/'$name'.mp3' -c:v libx264 -r 30 -pix_fmt yuv420p -t 3 -y './video/'$name'.mp4'

# done

# rm ./video/video.txt

# cat cwords.txt | while read line
# do 
#   echo $line | sed -s "s/.mp3/.mp4/g" >> video.txt
#   echo $line | sed -s "s/.mp3/.mp4/g" >> video.txt
# done

# mv video.txt ./video/video.txt
# cd video
# sleep 60
# ffmpeg -f concat -i video.txt -c copy -y cwords.mp4
