#!/bin/bash -ex

source .env

# There are two important configuration files required
# by AWS so the services know exactly what to do once
# our code makes it to their system. The first one is
# buildspec.yml. This file is needed by AWS CodeBuild
# and tells it how to create the required Docker images
# to run our infrastructure, after the images have been
# created, they are pushed to a private container
# registry, hosted by AWS as well.
#
# All configuration files can be part of the source code
# and live inside the repo, I decided to make them part
# of this script for simplicity-sake but they can be
# extracted any time without side effects.
cat << EOF > buildspec.yml
version: 0.2

phases:
  pre_build:
    commands:
     - echo Logging in to Amazon ECR...
     - \$(aws ecr get-login --no-include-email --region us-east-1)
     - echo Pulling Docker Images for cache ... | tee -a log.txt
     - docker-compose -f production.yml pull --ignore-pull-failures
  build:
    commands:
     - echo Build started on `date`
     - echo Building the Docker image...
     - docker-compose -f production.yml build django
     - docker tag "${COMPOSE_PROJECT_NAME}_${SERVICE_DJANGO_BUILD_NAME}" "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_DJANGO_BUILD_NAME}-latest"
     - docker-compose -f production.yml build nginx
     - docker tag "${COMPOSE_PROJECT_NAME}_${SERVICE_NGINX_BUILD_NAME}" "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_NGINX_BUILD_NAME}-latest"
  post_build:
    commands:
     - echo Build completed on `date`
     - echo Pushing the Docker image...
     - docker push "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_DJANGO_BUILD_NAME}-latest"
     - docker push "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_NGINX_BUILD_NAME}-latest"
     - echo printenv | tee -a log.txt
     - printenv | tee -a log.txt
artifacts:
  files:
    - 'Dockerrun.aws.json'
EOF

# The second required configuration file is
# Dockerrun.aws.json, similar to a Docker Compose
# configuration definition, it specifies the images to
# pull from the container registry, previously defined
# in the build step and how they should be layed ou
# in different containers.
cat << EOF > Dockerrun.aws.json
{
  "AWSEBDockerrunVersion": 2,
  "containerDefinitions": [
    {
     "name": "redis",
     "image": redis:3.2,
     "essential": true,
     "memory": 128
    },
    {
     "name": "django",
     "image": "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_DJANGO_BUILD_NAME}-latest",
     "essential": true,
     "links":[
       "redis"
     ],
     "command": [
        "/start"
      ],
     "memory": 768
    },
    {
     "name": "nginx",
     "image": "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_NGINX_BUILD_NAME}-latest",
     "essential": true,
     "memory": 128,
     "links": [
        "django"
     ],
     "portMappings": [
       {
         "hostPort": 80,
         "containerPort": 80
       }
     ],
     "mountPoints": [
        {
          "sourceVolume": "awseb-logs-nginx",
          "containerPath": "/var/log/nginx"
        }
      ]
    }
  ]
}
EOF

# Compress all files recursively into a ZIP
zip -r sac.zip * .[^.]*


# UPLOAD ZIP TO S3

# S3_SOURCE_FILE            (Required) Source file to upload to S3
#                               Example: "sac.zip"
# S3_SOURCE_CONTENT_TYPE    (Required) MIME content-type of the source file
#                               Example: "application/zip"
# AWS_S3_TARGET_FILE        (Required) Target file in S3
#                               Example: "sac-deployment/sac.zip"
# AWS_S3_BUCKET             (Required) Target AWS S3 bucket for upload
# AWS_ACCESS_KEY_ID         (Required) Access Key ID for the target AWS account
# AWS_SECRET_ACCESS_KEY     (Required, Secret) Secret Access Key for the target AWS account
# See: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html

file="${AWS_S3_TARGET_FILE}"
bucket=${AWS_S3_BUCKET}
resource="/${bucket}/${file}"
contentType="application/zip"
dateValue=`date -R`
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${resource}"
s3Key=${AWS_ACCESS_KEY_ID}
s3Secret=${AWS_SECRET_ACCESS_KEY}
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -X PUT -T "${file}" \
  -H "Host: ${bucket}.s3.amazonaws.com" \
  -H "Date: ${dateValue}" \
  -H "Content-Type: ${contentType}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  https://${bucket}.s3.amazonaws.com/${file}


