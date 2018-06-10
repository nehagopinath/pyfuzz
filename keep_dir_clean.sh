#!/bin/bash

DIR=$1

inotifywait -m --exclude "/\..+" -e create --format '%f' "$DIR" | while read f

do
   rm -r $f
done

