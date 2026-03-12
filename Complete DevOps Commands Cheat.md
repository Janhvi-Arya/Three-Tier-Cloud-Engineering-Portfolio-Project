# Complete DevOps Cheat Sheet: Linux, Docker, Kubernetes, Minikube & psql

This cheat sheet covers essential commands for daily DevOps work. Each command includes a description, syntax, and practical example. Use it as a quick reference.

---

## Table of Contents
- [Linux Commands](#linux-commands)
- [Docker Commands](#docker-commands)
- [Kubernetes Commands (kubectl)](#kubernetes-commands-kubectl)
- [Minikube Commands](#minikube-commands)
- [PostgreSQL (psql) Commands](#postgresql-psql-commands)

---

## Linux Commands

### File and Directory Management

| Command | Description | Example |
|---------|-------------|---------|
| `ls` | List directory contents | `ls -la` (list all files with details) |
| `cd` | Change directory | `cd /var/log` |
| `pwd` | Print current working directory | `pwd` |
| `mkdir` | Create a directory | `mkdir -p parent/child` (create parent and child) |
| `rmdir` | Remove empty directory | `rmdir emptydir` |
| `rm` | Remove files or directories | `rm -rf olddir/` (force remove recursively) |
| `cp` | Copy files or directories | `cp -r source/ dest/` |
| `mv` | Move or rename files/directories | `mv file.txt newname.txt` |
| `touch` | Create an empty file or update timestamp | `touch newfile.txt` |
| `find` | Search for files | `find /home -name "*.log"` |
| `tree` | Display directory tree (install separately) | `tree /etc` |

### File Permissions

| Command | Description | Example |
|---------|-------------|---------|
| `chmod` | Change file permissions | `chmod 755 script.sh` (rwxr-xr-x) |
| `chown` | Change file owner and group | `chown user:group file.txt` |
| `chgrp` | Change group ownership | `chgrp developers file.txt` |
| `umask` | Set default permissions for new files | `umask 022` |

### Process Management

| Command | Description | Example |
|---------|-------------|---------|
| `ps` | Show running processes | `ps aux` (all processes) |
| `top` / `htop` | Interactive process viewer | `top` |
| `kill` | Terminate a process by PID | `kill -9 1234` (force kill) |
| `killall` | Kill processes by name | `killall nginx` |
| `pgrep` / `pkill` | Find or signal processes by name | `pkill -f "python app.py"` |
| `jobs` | List background jobs | `jobs` |
| `bg` / `fg` | Resume job in background/foreground | `fg %1` |
| `nohup` | Run command immune to hangups | `nohup longscript.sh &` |
| `systemctl` | Control systemd services | `systemctl start nginx` |

### System Information

| Command | Description | Example |
|---------|-------------|---------|
| `uname` | Print system information | `uname -a` |
| `df` | Disk space usage | `df -h` (human-readable) |
| `du` | Disk usage of files/directories | `du -sh /var` |
| `free` | Memory usage | `free -h` |
| `uptime` | How long system has been running | `uptime` |
| `whoami` | Current username | `whoami` |
| `id` | User and group IDs | `id` |
| `hostname` | System hostname | `hostname -I` (IP addresses) |
| `date` | Show or set date/time | `date` |

### Networking

| Command | Description | Example |
|---------|-------------|---------|
| `ping` | Test network connectivity | `ping -c 4 google.com` |
| `curl` | Transfer data from/to a server | `curl http://example.com` |
| `wget` | Download files | `wget https://example.com/file.zip` |
| `ifconfig` / `ip` | Network interface configuration | `ip addr show` |
| `netstat` | Network statistics | `netstat -tulpn` |
| `ss` | Socket statistics (modern netstat) | `ss -tulw` |
| `nslookup` / `dig` | DNS lookup | `dig google.com` |
| `traceroute` | Trace route to host | `traceroute google.com` |
| `ssh` | Secure shell to remote host | `ssh user@192.168.1.10` |
| `scp` | Secure copy over SSH | `scp file.txt user@remote:/path/` |
| `rsync` | Remote sync (efficient copy) | `rsync -avz source/ user@remote:/dest/` |

### Text Processing

| Command | Description | Example |
|---------|-------------|---------|
| `cat` | Concatenate and display files | `cat file.txt` |
| `less` / `more` | View file page by page | `less large.log` |
| `head` / `tail` | Show first/last lines | `tail -f app.log` (follow) |
| `grep` | Search text using patterns | `grep -r "error" /var/log` |
| `awk` | Pattern scanning and processing | `awk '{print $1}' file.txt` |
| `sed` | Stream editor for filtering/transforming | `sed 's/old/new/g' file.txt` |
| `sort` | Sort lines | `sort -n numbers.txt` |
| `uniq` | Report or omit repeated lines | `sort file.txt | uniq -c` |
| `wc` | Count lines, words, characters | `wc -l file.txt` |
| `cut` | Remove sections from each line | `cut -d: -f1 /etc/passwd` |
| `tr` | Translate or delete characters | `echo "hello" | tr 'a-z' 'A-Z'` |
| `tee` | Read from stdin and write to stdout and files | `echo "data" | tee file.txt` |

### Compression and Archiving

| Command | Description | Example |
|---------|-------------|---------|
| `tar` | Archive files | `tar -czvf archive.tar.gz /path` (create gzip) |
| `gzip` / `gunzip` | Compress or decompress files | `gzip file.txt` |
| `zip` / `unzip` | Zip/unzip files | `zip -r archive.zip folder/` |
| `xz` | Compress with xz | `xz -k file.txt` (keep original) |

### Package Management (Debian/Ubuntu - apt)

| Command | Description | Example |
|---------|-------------|---------|
| `apt update` | Update package list | `sudo apt update` |
| `apt upgrade` | Upgrade all packages | `sudo apt upgrade -y` |
| `apt install` | Install a package | `sudo apt install nginx` |
| `apt remove` | Remove a package | `sudo apt remove nginx` |
| `apt search` | Search for packages | `apt search python` |
| `apt show` | Show package details | `apt show nginx` |

### User Management

| Command | Description | Example |
|---------|-------------|---------|
| `useradd` | Create a new user | `sudo useradd -m -s /bin/bash john` |
| `usermod` | Modify user account | `sudo usermod -aG sudo john` (add to sudo group) |
| `userdel` | Delete a user | `sudo userdel -r john` (remove home) |
| `passwd` | Change user password | `passwd john` |
| `groupadd` | Create a new group | `sudo groupadd developers` |
| `groups` | Show user groups | `groups john` |
| `su` | Switch user | `su - john` |
| `sudo` | Execute command as another user | `sudo -u john command` |

### Disk Usage

| Command | Description | Example |
|---------|-------------|---------|
| `df` | Report file system disk space | `df -h` |
| `du` | Estimate file space usage | `du -sh *` |
| `mount` / `umount` | Mount/unmount filesystems | `mount /dev/sdb1 /mnt` |
| `lsblk` | List block devices | `lsblk` |
| `fdisk` | Partition table manipulator | `sudo fdisk -l` |

### Environment Variables

| Command | Description | Example |
|---------|-------------|---------|
| `env` | Print environment variables | `env` |
| `export` | Set environment variable | `export MY_VAR=value` |
| `unset` | Remove environment variable | `unset MY_VAR` |
| `echo` | Display a line of text | `echo $PATH` |

### SSH

| Command | Description | Example |
|---------|-------------|---------|
| `ssh` | Connect to remote host | `ssh -i key.pem user@host` |
| `ssh-keygen` | Generate SSH key pair | `ssh-keygen -t rsa -b 4096` |
| `ssh-copy-id` | Copy public key to remote host | `ssh-copy-id user@host` |
| `scp` | Secure copy | `scp file.txt user@host:/path/` |
| `sftp` | Secure FTP | `sftp user@host` |

---

## Docker Commands

### Image Management

| Command | Description | Example |
|---------|-------------|---------|
| `docker images` | List local images | `docker images` |
| `docker pull` | Pull an image from registry | `docker pull ubuntu:22.04` |
| `docker push` | Push an image to registry | `docker push myrepo/app:latest` |
| `docker build` | Build an image from Dockerfile | `docker build -t myapp:1.0 .` |
| `docker rmi` | Remove one or more images | `docker rmi myapp:1.0` |
| `docker tag` | Tag an image | `docker tag myapp:1.0 myrepo/app:latest` |
| `docker history` | Show image history | `docker history myapp:1.0` |
| `docker save` | Save image to tar archive | `docker save -o myapp.tar myapp:1.0` |
| `docker load` | Load image from tar archive | `docker load -i myapp.tar` |

### Container Management

| Command | Description | Example |
|---------|-------------|---------|
| `docker run` | Run a command in a new container | `docker run -it --name test ubuntu bash` |
| `docker ps` | List containers | `docker ps -a` (all) |
| `docker start` | Start a stopped container | `docker start test` |
| `docker stop` | Stop a running container | `docker stop test` |
| `docker restart` | Restart a container | `docker restart test` |
| `docker rm` | Remove a container | `docker rm -f test` (force) |
| `docker exec` | Execute a command in a running container | `docker exec -it test bash` |
| `docker logs` | Fetch container logs | `docker logs -f test` (follow) |
| `docker inspect` | Show low-level info | `docker inspect test` |
| `docker cp` | Copy files between container and host | `docker cp test:/app/log.txt .` |
| `docker commit` | Create image from container changes | `docker commit test myapp:new` |
| `docker export` | Export container filesystem as tar | `docker export test > test.tar` |
| `docker import` | Import tar to create image | `cat test.tar | docker import - myimage:latest` |

### Docker Hub / Registry

| Command | Description | Example |
|---------|-------------|---------|
| `docker login` | Log in to a registry | `docker login -u username` |
| `docker logout` | Log out | `docker logout` |
| `docker search` | Search Docker Hub for images | `docker search nginx` |

### Dockerfile Instructions

| Instruction | Description | Example |
|-------------|-------------|---------|
| `FROM` | Base image | `FROM python:3.9-slim` |
| `RUN` | Execute command in new layer | `RUN apt-get update && apt-get install -y curl` |
| `CMD` | Default command | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Configure container as executable | `ENTRYPOINT ["docker-entrypoint.sh"]` |
| `COPY` | Copy files from host | `COPY . /app` |
| `ADD` | Copy with extra features (URL, tar) | `ADD https://example.com/file.tar.gz /tmp/` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `ENV` | Set environment variable | `ENV NODE_ENV=production` |
| `EXPOSE` | Document port | `EXPOSE 8080` |
| `VOLUME` | Create mount point | `VOLUME /data` |
| `USER` | Set user | `USER node` |
| `LABEL` | Add metadata | `LABEL version="1.0"` |
| `ARG` | Build-time variable | `ARG VERSION=latest` |

### Docker Compose

| Command | Description | Example |
|---------|-------------|---------|
| `docker-compose up` | Create and start containers | `docker-compose up -d` (detached) |
| `docker-compose down` | Stop and remove containers | `docker-compose down -v` (remove volumes) |
| `docker-compose ps` | List containers | `docker-compose ps` |
| `docker-compose logs` | View logs | `docker-compose logs -f` |
| `docker-compose exec` | Run command in service | `docker-compose exec web bash` |
| `docker-compose build` | Build images | `docker-compose build` |
| `docker-compose pull` | Pull service images | `docker-compose pull` |
| `docker-compose restart` | Restart services | `docker-compose restart` |
| `docker-compose stop` | Stop services | `docker-compose stop` |
| `docker-compose start` | Start services | `docker-compose start` |

### Volumes and Bind Mounts

| Command | Description | Example |
|---------|-------------|---------|
| `docker volume create` | Create a volume | `docker volume create myvol` |
| `docker volume ls` | List volumes | `docker volume ls` |
| `docker volume inspect` | Show volume details | `docker volume inspect myvol` |
| `docker volume rm` | Remove a volume | `docker volume rm myvol` |
| `docker volume prune` | Remove unused volumes | `docker volume prune` |
| Mount in `docker run` | Bind mount a host directory | `docker run -v /host/path:/container/path ...` |
| Mount in `docker run` | Use a named volume | `docker run -v myvol:/data ...` |

### Networking

| Command | Description | Example |
|---------|-------------|---------|
| `docker network ls` | List networks | `docker network ls` |
| `docker network create` | Create a network | `docker network create --driver bridge mynet` |
| `docker network inspect` | Show network details | `docker network inspect mynet` |
| `docker network connect` | Connect container to network | `docker network connect mynet container1` |
| `docker network disconnect` | Disconnect container | `docker network disconnect mynet container1` |
| `docker network rm` | Remove a network | `docker network rm mynet` |
| `docker network prune` | Remove unused networks | `docker network prune` |

### System and Cleanup

| Command | Description | Example |
|---------|-------------|---------|
| `docker system df` | Show docker disk usage | `docker system df` |
| `docker system prune` | Remove unused data | `docker system prune -a --volumes` |
| `docker container prune` | Remove stopped containers | `docker container prune` |
| `docker image prune` | Remove unused images | `docker image prune -a` |
| `docker volume prune` | Remove unused volumes | `docker volume prune` |
| `docker network prune` | Remove unused networks | `docker network prune` |
| `docker info` | Display system info | `docker info` |
| `docker version` | Show Docker version | `docker version` |

---

## Kubernetes Commands (kubectl)

### Cluster Information

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl cluster-info` | Display cluster info | `kubectl cluster-info` |
| `kubectl get nodes` | List nodes | `kubectl get nodes -o wide` |
| `kubectl describe node <node>` | Show node details | `kubectl describe node minikube` |
| `kubectl api-resources` | List API resources | `kubectl api-resources` |
| `kubectl explain <resource>` | Documentation of resource | `kubectl explain pod` |
| `kubectl version` | Show client/server versions | `kubectl version --short` |
| `kubectl config view` | Show merged kubeconfig settings | `kubectl config view` |
| `kubectl config get-contexts` | List contexts | `kubectl config get-contexts` |
| `kubectl config current-context` | Show current context | `kubectl config current-context` |
| `kubectl config use-context <name>` | Switch context | `kubectl config use-context minikube` |
| `kubectl config set-context` | Set a context entry | `kubectl config set-context --current --namespace=dev` |

### Resource Management (Pods, Deployments, Services, etc.)

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl get <resource>` | List resources | `kubectl get pods,svc,deploy` |
| `kubectl describe <resource> <name>` | Show details | `kubectl describe pod my-pod` |
| `kubectl create <resource>` | Create from file or stdin | `kubectl create -f deployment.yaml` |
| `kubectl apply` | Apply configuration changes | `kubectl apply -f manifest.yaml` |
| `kubectl delete` | Delete resources | `kubectl delete pod my-pod` |
| `kubectl edit` | Edit a resource | `kubectl edit deployment nginx` |
| `kubectl expose` | Expose a resource as a service | `kubectl expose pod my-pod --port=80 --target-port=8080` |
| `kubectl run` | Run a pod (imperative) | `kubectl run nginx --image=nginx --restart=Never` |
| `kubectl set image` | Update image of a resource | `kubectl set image deployment/nginx nginx=nginx:1.21` |
| `kubectl scale` | Scale a deployment | `kubectl scale deployment nginx --replicas=5` |
| `kubectl autoscale` | Auto-scale a deployment | `kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80` |
| `kubectl rollout status` | Watch rollout status | `kubectl rollout status deployment nginx` |
| `kubectl rollout history` | Show rollout history | `kubectl rollout history deployment nginx` |
| `kubectl rollout undo` | Rollback to previous version | `kubectl rollout undo deployment nginx` |
| `kubectl rollout restart` | Restart a deployment | `kubectl rollout restart deployment nginx` |
| `kubectl port-forward` | Forward ports to local machine | `kubectl port-forward pod/my-pod 8080:80` |
| `kubectl exec` | Execute command in container | `kubectl exec -it my-pod -- bash` |
| `kubectl logs` | Print container logs | `kubectl logs -f my-pod` |
| `kubectl attach` | Attach to running container | `kubectl attach my-pod -i` |
| `kubectl cp` | Copy files to/from container | `kubectl cp ./file.txt my-pod:/tmp/` |
| `kubectl top` | Show resource usage (metrics required) | `kubectl top pod` |

### Namespaces

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl get namespaces` | List namespaces | `kubectl get ns` |
| `kubectl create namespace` | Create a namespace | `kubectl create ns dev` |
| `kubectl delete namespace` | Delete a namespace | `kubectl delete ns dev` |
| `kubectl config set-context --current --namespace=<ns>` | Switch namespace | `kubectl config set-context --current --namespace=dev` |

### ConfigMaps and Secrets

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl create configmap` | Create from literals, files, or directories | `kubectl create configmap app-config --from-literal=key=value` |
| `kubectl get configmap` | List configmaps | `kubectl get configmap` |
| `kubectl describe configmap` | Show details | `kubectl describe configmap app-config` |
| `kubectl delete configmap` | Delete | `kubectl delete configmap app-config` |
| `kubectl create secret generic` | Create secret | `kubectl create secret generic db-secret --from-literal=password=pass` |
| `kubectl get secret` | List secrets | `kubectl get secrets` |
| `kubectl describe secret` | Show details (values hidden) | `kubectl describe secret db-secret` |
| `kubectl delete secret` | Delete | `kubectl delete secret db-secret` |

### Ingress

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl get ingress` | List ingresses | `kubectl get ingress` |
| `kubectl describe ingress` | Show details | `kubectl describe ingress my-ingress` |
| `kubectl create ingress` | Create from file or command | `kubectl create ingress my-ingress --rule="host.com/path=service:port"` |
| `kubectl delete ingress` | Delete | `kubectl delete ingress my-ingress` |

### Persistent Volumes and Claims

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl get pv` | List persistent volumes | `kubectl get pv` |
| `kubectl get pvc` | List persistent volume claims | `kubectl get pvc` |
| `kubectl describe pv/pvc` | Show details | `kubectl describe pvc my-claim` |
| `kubectl delete pv/pvc` | Delete | `kubectl delete pvc my-claim` |

### Debugging and Troubleshooting

| Command | Description | Example |
|---------|-------------|---------|
| `kubectl describe` | Detailed info about resource | `kubectl describe pod failing-pod` |
| `kubectl logs` | Container logs | `kubectl logs failing-pod --previous` (previous instance) |
| `kubectl exec` | Interactive shell | `kubectl exec -it failing-pod -- /bin/sh` |
| `kubectl port-forward` | Access service locally | `kubectl port-forward service/my-service 8080:80` |
| `kubectl get events` | Show cluster events | `kubectl get events --sort-by='.lastTimestamp'` |
| `kubectl debug` | Create debugging session (1.18+) | `kubectl debug node/minikube -it --image=ubuntu` |

---

## Minikube Commands

### Cluster Lifecycle

| Command | Description | Example |
|---------|-------------|---------|
| `minikube start` | Start a local Kubernetes cluster | `minikube start --cpus=4 --memory=8g` |
| `minikube stop` | Stop the cluster | `minikube stop` |
| `minikube delete` | Delete the cluster | `minikube delete` |
| `minikube status` | Get cluster status | `minikube status` |
| `minikube pause` / `unpause` | Pause/unpause cluster | `minikube pause` |
| `minikube update-context` | Update kubectl context | `minikube update-context` |
| `minikube ip` | Get cluster IP address | `minikube ip` |
| `minikube ssh` | SSH into minikube VM | `minikube ssh` |
| `minikube kubectl --` | Use kubectl via minikube | `minikube kubectl -- get pods` |

### Addons

| Command | Description | Example |
|---------|-------------|---------|
| `minikube addons list` | List available addons | `minikube addons list` |
| `minikube addons enable <addon>` | Enable an addon | `minikube addons enable ingress` |
| `minikube addons disable <addon>` | Disable an addon | `minikube addons disable ingress` |
| `minikube addons configure <addon>` | Configure addon | `minikube addons configure registry-creds` |

### Service Access

| Command | Description | Example |
|---------|-------------|---------|
| `minikube service <service>` | Expose service and open browser | `minikube service my-service` |
| `minikube service list` | List services and their URLs | `minikube service list` |
| `minikube tunnel` | Create a tunnel for LoadBalancer services | `minikube tunnel` |

### Profile Management

| Command | Description | Example |
|---------|-------------|---------|
| `minikube profile list` | List profiles | `minikube profile list` |
| `minikube profile <name>` | Set/switch profile | `minikube profile my-cluster` |
| `minikube config set` | Set configuration (e.g., driver) | `minikube config set driver docker` |

---

## PostgreSQL (psql) Commands

### Connecting

| Command | Description | Example |
|---------|-------------|---------|
| `psql` | Connect to default database as current user | `psql` |
| `psql -d <db> -U <user> -h <host> -p <port>` | Connect with parameters | `psql -d mydb -U admin -h localhost -p 5432` |
| `\c <db>` or `\connect` | Switch to another database | `\c mydb` |
| `\conninfo` | Show connection info | `\conninfo` |
| `\q` | Quit psql | `\q` |

### Database Operations

| Command | Description | Example |
|---------|-------------|---------|
| `CREATE DATABASE <name>;` | Create new database | `CREATE DATABASE myapp;` |
| `DROP DATABASE <name>;` | Delete database | `DROP DATABASE myapp;` |
| `\l` or `\list` | List all databases | `\l` |
| `ALTER DATABASE <name> ...;` | Modify database | `ALTER DATABASE myapp OWNER TO newuser;` |

### Table Operations

| Command | Description | Example |
|---------|-------------|---------|
| `CREATE TABLE ...` | Create table | `CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT);` |
| `DROP TABLE <name>;` | Delete table | `DROP TABLE users;` |
| `ALTER TABLE ...` | Modify table | `ALTER TABLE users ADD COLUMN email TEXT;` |
| `\dt` | List tables in current database | `\dt` |
| `\d <table>` | Describe table (columns, indexes) | `\d users` |
| `\d+ <table>` | Detailed description | `\d+ users` |
| `TRUNCATE <table>;` | Remove all rows | `TRUNCATE users;` |

### Data Manipulation

| Command | Description | Example |
|---------|-------------|---------|
| `INSERT INTO ... VALUES ...;` | Insert data | `INSERT INTO users (name) VALUES ('Alice');` |
| `SELECT ... FROM ...;` | Query data | `SELECT * FROM users;` |
| `UPDATE ... SET ... WHERE ...;` | Update data | `UPDATE users SET name='Bob' WHERE id=1;` |
| `DELETE FROM ... WHERE ...;` | Delete data | `DELETE FROM users WHERE id=1;` |
| `COPY ... TO ...` | Export table to file | `COPY users TO '/tmp/users.csv' DELIMITER ',' CSV HEADER;` |
| `COPY ... FROM ...` | Import from file | `COPY users FROM '/tmp/users.csv' DELIMITER ',' CSV HEADER;` |

### psql Meta-Commands

| Command | Description | Example |
|---------|-------------|---------|
| `\?` | Help with psql commands | `\?` |
| `\h` | Help with SQL commands | `\h SELECT` |
| `\timing` | Toggle query execution time display | `\timing` |
| `\x` | Toggle expanded output (vertical) | `\x auto` |
| `\e` | Edit query in external editor | `\e` |
| `\i <file>` | Execute commands from file | `\i /path/to/script.sql` |
| `\o <file>` | Save query output to file | `\o /tmp/output.txt` |
| `\pset` | Set output format (border, format, etc.) | `\pset format aligned` |
| `\echo` | Print message | `\echo 'Hello'` |
| `! <command>` | Execute shell command | `! ls -l` |
| `\watch` | Execute query repeatedly | `SELECT count(*) FROM users; \watch 1` |

### User and Permission Management

| Command | Description | Example |
|---------|-------------|---------|
| `CREATE ROLE <name> ...;` | Create role/user | `CREATE ROLE alice WITH LOGIN PASSWORD 'secret';` |
| `ALTER ROLE ...;` | Modify role | `ALTER ROLE alice WITH SUPERUSER;` |
| `DROP ROLE <name>;` | Delete role | `DROP ROLE alice;` |
| `\du` | List roles | `\du` |
| `GRANT ... ON ... TO ...;` | Grant privileges | `GRANT SELECT ON users TO alice;` |
| `REVOKE ... ON ... FROM ...;` | Revoke privileges | `REVOKE INSERT ON users FROM alice;` |
| `ALTER DEFAULT PRIVILEGES ...;` | Set default privileges | `ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO alice;` |

### Backup and Restore (using pg_dump / psql)

| Command | Description | Example |
|---------|-------------|---------|
| `pg_dump <db> > backup.sql` | Backup database to SQL file | `pg_dump mydb > mydb_backup.sql` |
| `pg_dump -h <host> -U <user> <db> > backup.sql` | Remote backup | `pg_dump -h remotehost -U admin mydb > backup.sql` |
| `psql <db> < backup.sql` | Restore from SQL file | `psql mydb < mydb_backup.sql` |
| `pg_dumpall > all.sql` | Backup all databases | `pg_dumpall > all.sql` |
| `pg_restore` | Restore from custom format (created with -Fc) | `pg_restore -d mydb backup.dump` |

---

This cheat sheet covers the most frequently used commands in Linux, Docker, Kubernetes, Minikube, and PostgreSQL. For deeper reference, use `man <command>`, `--help`, or official documentation.
