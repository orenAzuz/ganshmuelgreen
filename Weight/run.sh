# Parent directory since required by docker-compose & OPS team in this way
export GIT_HOME=../
#export GIT_HOME=$PWD

mkdir -p $PWD/mysql/datadir

docker-compose down
docker-compose up
