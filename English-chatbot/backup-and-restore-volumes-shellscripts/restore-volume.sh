#!/bin/bash
#
docker_project_root_path=$1
project_name_old=$2
backup_source_dir=$3
project_name_new=$4

echo $1
echo $2
echo $3
echo $4


function restore_volume {
  volume_name_old=$1
  backup_source=$2
  volume_name_new=$3
  #volume_name_to_restore=$(sed 's/-backup-[0-9].*//' <<< $volume_name_old)
    echo $volume_name_old
    echo $backup_source
    echo $volume_name_new
    docker run --rm -v $volume_name_new:/data -v $backup_source:/backup ubuntu tar -xzvf /backup/$volume_name_old.tar.gz -C /data
}

current_dir="$PWD"

# cd "$docker_project_root_path/$project_name_old"

# echo "Stopping running containers"
# docker-compose stop

cd "$docker_project_root_path/$project_name_new"
echo $PWD

echo "Stopping running containers"
docker-compose stop


search="$backup_source_dir/$project_name_old"
echo $search
echo "Mounting volumes and performing backup..."
# volumes=($(docker volume ls -f name=$project_name | awk '{if (NR > 1) print $2}'))
volumes=($(ls -l $search/*.tar.gz | awk '{if (sub(".tar.gz","",$9)) print $9}'))
for v in "${volumes[@]}"
do
  volume="${v/$search\//""}"
  restore_volume "$volume" "$backup_source_dir/$project_name_old" "${volume/$project_name_old/$project_name_new}" 
done

# echo "Restarting containers"
# cd "$docker_project_root_path/$project_name_old"

# echo "Stopping running containers"
# docker-compose start

cd "$docker_project_root_path/$project_name_new"

echo "Starting running containers"
docker-compose start


cd $current_dir
