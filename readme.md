setup jktapi.py main:
- app.run(host='0.0.0.0', port=5000, debug=True) for server homelab
- app.run(debug=True) for local running with IDE pycharm

build image
create folder python-docker
create folder WORKDIR
create folder WORKDIR/app
copy Dockerfile inside python-docker
copy requirement.txt inside WORKDIR (ignore requirement for local use if caused error)
copy all python file inside WORKDIR

change directory to WORKDIR
- build the image: sudo docker build -t python-docker .
- run the image: sudo docker run -it --rm -e TZ=Asia/Jakarta -p 5000:5000 -v /home/python-docker/WORKDIR:/app python-docker