Tested on Debian 10 (buster) and Python 3.7.

## Prerequisite

* Acquire administrative privileges on a Debian 10 server.
* Install docker: https://docs.docker.com/engine/install/debian/

## Recommended

Follow: https://cloud.google.com/container-registry/docs/advanced-authentication

## Quick Start

* Pull image from: gcr.io/PROJECT_ID/YOUR_IMAGE:latest

* Artifact Registry offers granular access control.  Consider migrating from Container Registry to Artifact Registry (me including).

> docker run --name prod -dt gcr.io/PROJECT_ID/YOUR_IMAGE:latest

> docker container ls -f name=prod

* Or, you can build from source code within this repository, in which case, you will also need to access the secrets within GCP.

## Reference

Templates from: https://github.com/lins05/slackbot

## Special Thanks

Ministry of the Environment Government of Japan.

![iriomote cat](https://www.env.go.jp/park/iriomote/guide/img/M19.jpg)
