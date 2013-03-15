#!/bin/bash

APP_DIR=`pwd`/books/
LOCALE_DIR=$APP_DIR/locale/

echo $APP_DIR
pushd $APP_DIR

echo `pwd`


for lang in `ls $LOCALE_DIR`; do
  echo "Setting up locale for $lang"
  django-admin.py makemessages -l $lang
done
echo "*************************"

django-admin.py compilemessages


popd
