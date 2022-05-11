if [ -d "resized" ]
then
  echo "Directory exists"
  echo "Do you want to re-run the script? (Y)es, (N)o"
  read choice
fi

echo $choice

if [ $choice == "Y" ] || [ $choice == "y" ]
then
  rm -rf resized
  mkdir resized
  mkdir resized/sugimori
  for f in sugimori/*.png; do
    echo "Resizing $f"
    # ffmpeg -i "$f" -vf scale=640:-1 resized/"${f%.*}.jpg"
    convert "$f" -background white -alpha remove -alpha off -resize 30% resized/"${f%.*}.jpg"
  done
  cp resized/sugimori/*.jpg resized
  rm -rf resized/sugimori
else
  echo "Ok BYE BYE!"
fi

