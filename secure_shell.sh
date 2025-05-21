#!/bin/bash

CORRECT_PASSWORD="nihal123"

# Ensure it only runs in interactive shells
if [[ $- == *i* ]]; then
  echo -n "Enter password to access container: "
  read -s entered
  echo

  if [ "$entered" != "$CORRECT_PASSWORD" ]; then
    echo "Access denied."
    exit 1
  else
    echo "Access granted."
  fi
fi

