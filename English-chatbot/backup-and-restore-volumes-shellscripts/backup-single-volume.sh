#!/bin/bash

# STEPS:
# 1. Validate that the docker-volume and backup dir exists
# 2. Start a new container that mounts the docker-volume and the backup dir
# 3. Create a "tar" of the content of the docker-volume and place it in the backup dir

volume_name=$1
backup_destination=$2
#BACKUP_FILE=${volume_name}-backup-$(date +%d-%m-%y-%H.%M.%S).tar.gz
BACKUP_FILE=${volume_name}.tar.gz
DOCKER_IMAGE=ubuntu
echo $backup_destination
function validateInput() {
    if [ ! -d "${backup_destination}" ] ; then
        echo "> Error: backup directory doesn't exist at '${backup_destination}'"
        exit 1
    fi

    INSPECT_VOLUME=$(docker volume inspect ${volume_name} 2>&1)
    if [[ ${INSPECT_VOLUME} == *"No such volume"* ]] ; then
        echo "> Error: docker volume '${volume_name}' not found"
        exit 1
    fi
}

validateInput

echo "> Backing up the docker-volume '${volume_name}' to '${backup_destination}/${BACKUP_FILE}'"

docker run --rm	\
    -v ${volume_name}:/data \
    -v ${backup_destination}:/backup ${DOCKER_IMAGE} \
    sh -c "cd /data && tar -czvf ${BACKUP_FILE} * && mv ${BACKUP_FILE} /backup"

echo "> Backup of docker-volume finished!"
