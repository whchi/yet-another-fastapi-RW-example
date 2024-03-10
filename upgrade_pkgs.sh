#!/bin/sh

UPDATE_TYPE=${1:-all}

DEV_LIBS=$(poetry show --only=dev -o -T |awk '{print $1}')
MAIN_LIBS=$(poetry show --only=main -o -T |awk '{print $1}')

if [ "$UPDATE_TYPE" = "main" ]; then
    LIBS=$(poetry show --only=main -o -T |awk '{print $1}')
elif [ "$UPDATE_TYPE" = "dev" ]; then
    LIBS=$(poetry show --only=dev -o -T |awk '{print $1}')
elif [ "$UPDATE_TYPE" = "all" ]; then
    LIBS=$(poetry show -o -T |awk '{print $1}')
else
    echo "Invalid update type: $UPDATE_TYPE"
    exit 1
fi

echo "Upgrading $UPDATE_TYPE packages"
for pkg in $LIBS
do
  if echo $DEV_LIBS | grep -q $pkg; then
    EXTRA_OPTS="-G dev"
  else
    EXTRA_OPTS=""
  fi
  echo "[begin].....$pkg"
  poetry add $pkg@latest $EXTRA_OPTS
  echo "[end].......$pkg\n"
done
