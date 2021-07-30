#!/bin/bash
#
docker_project_root_path=$1
project_name=$2
backup_path=$3
target_host=$4
#target_host=sam@10.10.77.252:$backup_path/$project_name/$sub_back_up_dir
sub_back_up_dir=$"backup-$(date +%y-%m-%d-%H.%M.%S)"

echo $1
echo $2
echo $3

current_dir=$PWD

echo "current:" $current_dir

cd "$docker_project_root_path/$project_name"

echo "Stopping running containers"
docker-compose stop

echo "Mounting volumes and performing backup..."
volumes=($(docker volume ls -f name=$project_name | awk '{if (NR > 1) print $2}'))
mkdir -p "$backup_path/$project_name/$sub_back_up_dir"
for v in "${volumes[@]}"
do
  bash "$docker_project_root_path/shellscripts/backup-single-volume.sh" $v "$backup_path/$project_name/$sub_back_up_dir"
done

echo "Move volumes to Target Host"
echo "$backup_path/$project_name/$sub_back_up_dir"
scp -r -i /var/lib/gitlab-runner/id_rsa "$backup_path/$project_name/$sub_back_up_dir" $target_host
#scp -r ~/backup $target_host

echo "Restarting containers"
docker-compose start



cd $current_dir
