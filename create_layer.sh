#!/bin/bash

DIRECTORY=lambda_layers
TEMP_DIR=$DIRECTORY/tmp
ZIP_NAME=crypto-layer.zip

mkdir -p $TEMP_DIR/python

echo "Installing dependencies..."
pip install -r requirements.txt -t $TEMP_DIR/python -q
cp -r crypto_lib $TEMP_DIR/python/crypto_lib

echo "Creating archive..."
cd $TEMP_DIR
zip -rq5 $ZIP_NAME .
cd - > /dev/null

echo "Finishing..."
mv $TEMP_DIR/$ZIP_NAME $DIRECTORY/$ZIP_NAME
rm -rf $TEMP_DIR
