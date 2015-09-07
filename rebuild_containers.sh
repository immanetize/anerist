#!/usr/bin/bash
[ "$(id -u)" -eq 0 ] || ( echo "This script must be run with privileges, please use sudo"; exit 1 )
rpm -q docker || dnf -y install docker
systemctl -q is-active docker || systemctl start docker
# the slave should not change much, so the logic here is simple
docker images | grep -q anerist-slave || docker build -t anerist-slave -f slave.dockerfile .
REBUILD=

rebuild_master () {
  echo "rebuilding master container, standby"
  docker ps -f "name=anerist-master" --quiet && docker stop anerist-master
  docker rm anerist-master
  docker build -f master.dockerfile -t anerist-master .
  docker run -d --name anerist-master anerist-master
}

restart_slave () {
  echo "restarting slave container, standby"
  docker ps -f "name=anerist-slave" && docker stop anerist slave
  docker ps -f "name=anerist-master" || ( echo "master is not running, slave won't start"; exit 1 )
  #this could be better, but the master is not ready immediately
  since="(( $(date --utc +%s) - $(date --utc --date "$(docker inspect --format='{{.Created}}' anerist-master)" +%s) ))"
  if [[ $since -le 20 ]]; then
    wait=$(( 30 - $since))
    echo "waiting $wait seconds for master startup"
    sleep $wait
  fi
  docker ps -a -f "name=anerist-slave" || docker run -t --name anerist-slave --link anerist-master:anerist-slave anerist-slave && docker start anerist-slave
  echo "anerist slave running"
}


git diff-index --quiet HEAD -- src/ resources/ master.dockerfile || export REBUILD=true
[ -f rebuild ] && ( export REBUILD=true; rm -f rebuild )
[ -n $REBUILD ] && ( rebuild_master;restart_slave ) || echo "no changes found, \`touch rebuild\` to force rebuild"

master_addr="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' anerist-master)"
echo "master web interace on http://${master_addr}:8010"
echo "watch master backend via \`docker attach anerist-master\` (TODO: this may not detach nicely)"




