pids=`ps -ef | grep uwsgi | grep wsgi:application | awk '{ print $2 }'`

for i in $pids
do
	sudo kill -9 $i	
done
