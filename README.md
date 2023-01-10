
<div style="text-align: center;">

# A program to monitor a Linux cluster with Python

</div>


`Bachelor software project`

## Overview of the program:

![image](./img/app.png)

---

## Project description:

I first step provisioned 3 nodes with ubuntu 20.04 OS using Vagrant tool. I then clustered these 3 nodes using Corosync and Pacemaker.

There are two resources in this cluster, the first is an IP address to access the cluster ip and the second is an Apache web server to display the desired website. If for any reason the node containing the resources fails, the resources are automatically transferred to another node.

![image](./img/terminal.png)

The program I wrote and implemented monitors the status of the Pacemaker service using Socket programming. If the service stop working, it sends an email.

Service status is received as zero or one values. These values are stored in the MySQL database. And also using the Matplotlib library, its graph is drawn at the end.

![image](./img/graph.png)

---

## How to run the project:

1. clone the repository
```
git clone https://github.com/amirmohammadre/monitoring_a_linux_cluster.git
```

2. cd to directory desired and run this command
```
vagrant up
```

3. Checking the status of nodes 
```
vagrant status
```

4. ssh to node desired for example:
```
vagrant ssh node1
```

5. transfer file Client.py to node favorite
```
scp Client.py root@192.168.56.10:/home/vagrant
```

6. first run file Server.py and input ip address and port   then file Client.py run on node favorite
```
python3 Server.py

python3 Client.py
```

---

## Contact:

- Amir mohammad Rezvaninia - [LinkedIn](https://www.linkedin.com/in/amirmohammadrezvaninia/) 

- Email Address: amirmohammadrezvaninia@gmail.com

- Project Link: [https://github.com/amirmohammadre/monitoring_a_linux_cluster](https://github.com/amirmohammadre/monitoring_a_linux_cluster)

---

## :man_technologist: support project:	
If you like the project, give it a :star: ;)