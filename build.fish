#!/usr/bin/env fish

set version "$argv[1]"

if [ -z "$version" ]
	echo "Usage: $argv[0] <version>" 1>&2
	exit 1
end

docker build -t wregab/netshootws:$version . ; and \
docker tag wregab/netshootws:$version wregab/netshootws:latest ; and \
docker push wregab/netshootws:$version ; and \
docker push wregab/netshootws:latest ; and \
docker run -it --rm -p 8080:8080 wregab/netshootws:$version --my-name=lolkek --others-names="dyn.niziol.pl;wp.pl;ren.niziol.pl"
