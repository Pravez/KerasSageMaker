#!/bin/bash
# You could also create the bucket from the CLI with this command
# aws s3api create-bucket --bucket cats-n-dogs --acl public read --region eu-west-1
# Then send to S3
aws s3 cp ./cats_n_dogs s3://cats-n-dogs/data --recursive
