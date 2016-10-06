#!/usr/bin/env bash

# install the following dependency
#sudo apt-get install python-pip python-dev
#sudo pip install protobuf

PROTO_DIR=./proto
mkdir -p $PROTO_DIR
cp ../../../../common/proto/*/*.proto $PROTO_DIR
cp ../../protos/*.proto $PROTO_DIR
touch ./proto/__init__.py
protoc -I=$PROTO_DIR --python_out=$PROTO_DIR $PROTO_DIR/*.proto


