#!/bin/bash
aws s3api create-bucket --bucket cats_n_dogs --acl public read --region eu-west-1
aws s3 cp ~/cats_n_dogs s3://cats_n_dogs/data --recursive
