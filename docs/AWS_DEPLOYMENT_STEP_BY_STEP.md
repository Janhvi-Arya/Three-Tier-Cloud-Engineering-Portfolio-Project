# AWS Deployment Guide Step By Step

This file explains how to deploy the project to AWS in very simple words.

The goal is to help a beginner understand:

- what to do
- why to do it
- how to do it step by step

This guide uses AWS EC2 because it is one of the easiest ways to deploy this project as a beginner.

## 1. What we are trying to do

We want to take the project from your laptop and run it on a cloud server.

In this guide:

- AWS gives you a virtual machine called an EC2 instance
- you install Docker on it
- you copy the project to it
- you run `docker compose up --build -d`

That is the simplest cloud path for this project.

## 2. Why EC2 is a good first choice

A beginner may ask:

> Why not use Kubernetes, ECS, EKS, or many AWS services?

Those are good later.

But EC2 is better for learning first because:

- it is easier to understand
- you control the full server
- Docker Compose already works here
- it is easier to explain in interview

You can say:

> I first deployed the project to EC2 to show I understand Linux server setup, Docker deployment, networking, and environment configuration.

## 3. AWS services used in this simple deployment

Main AWS parts:

- EC2 for the server
- Security Group for firewall rules
- Elastic IP optional, for stable public IP
- Route 53 optional, for domain

Minimum needed:

- one EC2 instance
- one security group

## 4. Architecture on AWS

Simple version:

```text
User Browser
   |
   v
EC2 Instance
   |
   +-- frontend container (nginx)
   +-- api container (FastAPI)
   +-- db container (PostgreSQL)
```

In this beginner version, PostgreSQL also runs on the same EC2 machine.
That is okay for a portfolio project.

Later, you could move the database to AWS RDS.

## 5. Before you start

Make sure you have:

- an AWS account
- permission to create EC2 instances
- an SSH client
- your project code ready

## 6. Step 1: Log in to AWS Console

What:

- open AWS Console and sign in

Why:

- you need the AWS dashboard to create infrastructure

How:

Go to:

`https://console.aws.amazon.com/`

## 7. Step 2: Open the EC2 service

In the AWS search bar:

- type `EC2`
- open the EC2 service

## 8. Step 3: Launch a new instance

Click `Launch instance`.

## 9. Step 4: Choose a name

Good example:

`cloudops-dashboard-demo`

Why:

- helps you identify it later

## 10. Step 5: Choose the operating system

Recommended:

- Ubuntu Server 24.04 LTS

Why:

- beginner friendly
- lots of tutorials
- Docker setup is straightforward

## 11. Step 6: Choose instance type

Recommended:

- `t3.small`

If you want a smaller budget and very light usage:

- `t3.micro` may work, but it is tighter

Why:

This project runs:

- Nginx
- FastAPI
- PostgreSQL

So a little extra memory is helpful.

## 12. Step 7: Create or choose a key pair

AWS needs a key pair so you can SSH into the server.

Why:

- this is how you securely log in to the EC2 instance

Save the `.pem` file carefully.

Important:

- do not lose it
- do not commit it to Git
- do not share it publicly

## 13. Step 8: Configure the network and security group

### What is a security group

A security group is like a firewall for your instance.

It controls which traffic can enter.

### Recommended inbound rules

- `SSH` on port `22` from your IP only
- `HTTP` on port `80` from `0.0.0.0/0`

Optional:

- `Custom TCP` port `8080` from your IP only during testing

Important beginner security note:

Do not open SSH to the whole internet if you can avoid it.

## 14. Step 9: Launch the instance

After you review the settings:

- click `Launch instance`

Wait until the instance is in `running` state.

## 15. Step 10: Find the public IP address

Open the instance details and copy the public IPv4 address.

You need it for:

- SSH
- opening the website in browser

## 16. Step 11: Connect to the instance by SSH

Example command:

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

Replace:

- `your-key.pem`
- `YOUR_PUBLIC_IP`

Why `chmod 400`:

- SSH wants strict file permissions for the key file

## 17. Step 12: Update package lists

Run:

```bash
sudo apt update
```

Why:

- before installing software, the system should know the latest package data

## 18. Step 13: Install Docker

Run:

```bash
sudo apt install -y docker.io docker-compose-v2
```

Why:

- the project is containerized, so the server must know how to run containers

## 19. Step 14: Start and enable Docker

Run:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Why:

- if the server restarts later, Docker should come back automatically

## 20. Step 15: Add your user to Docker group

Run:

```bash
sudo usermod -aG docker ubuntu
```

Then log out and log back in.

Why:

- this lets the `ubuntu` user run Docker commands without typing `sudo` every time

## 21. Step 16: Copy the project to the server

You have two common options.

### Option A: Use Git

If the project is in GitHub:

```bash
git clone <your-repo-url>
cd Three-Tier-Cloud-Engineering-Portfolio-Project
```

### Option B: Use `scp`

From your local machine:

```bash
scp -i your-key.pem -r Three-Tier-Cloud-Engineering-Portfolio-Project ubuntu@YOUR_PUBLIC_IP:/home/ubuntu/
```

Then SSH in and:

```bash
cd /home/ubuntu/Three-Tier-Cloud-Engineering-Portfolio-Project
```

## 22. Step 17: Prepare environment variables

Run:

```bash
cp .env.example .env
```

Then open the file:

```bash
nano .env
```

### What you should change

- `POSTGRES_PASSWORD`
- `APP_SECRET`

You can also change:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `CUSTOMER_USERNAME`
- `CUSTOMER_PASSWORD`

Default demo credentials are okay for local learning, but not for public deployment.

Use a long random `APP_SECRET`.

## 23. Step 18: Build and start the project

Run:

```bash
docker compose up --build -d
```

This is the main deployment command for this project.

What should happen:

- Postgres container starts
- API container starts
- frontend container starts

## 24. Step 19: Check the containers

Run:

```bash
docker compose ps
```

You should see:

- `db` running
- `api` healthy
- `frontend` running

## 25. Step 20: Check the logs if needed

Run:

```bash
docker compose logs api
docker compose logs frontend
docker compose logs db
```

If something fails, logs usually show the reason.

This is a very important cloud engineer habit.
Do not guess. Check logs.

## 26. Step 21: Test the deployment

From the EC2 machine:

```bash
curl http://localhost:8000/health
curl http://localhost:8080
```

If localhost works but the public IP does not, the problem is probably networking or security group.

## 27. Step 22: Open the app in your browser

Open:

`http://YOUR_PUBLIC_IP:8080`

If you later move Nginx to public port 80 directly, you may open:

`http://YOUR_PUBLIC_IP`

### Demo credentials

- Admin: `admin` / `AdminPass123!` if unchanged
- Customer: `customer` / `CustomerPass123!` if unchanged

Change them before public use.

## 28. Step 23: Optional improvement - use port 80 publicly

Right now the Compose file publishes frontend on `8080`.

That is okay for testing, but for a cleaner public demo you may want host port `80`.

You can change the frontend mapping in `docker-compose.yml` from:

```yaml
- "8080:80"
```

to:

```yaml
- "80:80"
```

Then restart:

```bash
docker compose up --build -d
```

## 29. Step 24: Optional improvement - use an Elastic IP

Elastic IP gives your EC2 instance a stable public IP.

Why:

- normal public IP may change if the instance is stopped and started again

## 30. Step 25: Optional improvement - connect a domain

If you have a domain, you can connect it using Route 53 or another DNS provider.

Why:

- a custom domain looks more professional than a raw IP address

## 31. Step 26: Optional improvement - add HTTPS

HTTPS encrypts traffic.
It also makes the project look more production-like.

Simple beginner path later:

- Nginx with Let's Encrypt
- or AWS load balancer with TLS

## 32. Step 27: How to update the app later

If you change code later:

1. copy new code to the instance
2. go into the project folder
3. run:

```bash
docker compose up --build -d
```

## 33. Step 28: How to stop the app

Run:

```bash
docker compose down
```

Why:

- stops containers but keeps data volume

If you want to remove data too:

```bash
docker compose down -v
```

Be careful with `-v`.

## 34. Step 29: Cost awareness for beginners

AWS costs money, so do not forget this part.

To reduce cost:

- stop or terminate unused EC2 instances
- remove unused Elastic IPs
- remove unused volumes if you no longer need them

Good cloud engineers think about cost too.

## 35. Common deployment problems and simple fixes

### Problem: You cannot SSH

Check:

- correct key file
- correct username (`ubuntu`)
- security group allows port `22` from your IP

### Problem: Browser cannot open the app

Check:

- frontend container is running
- security group allows the public port
- correct public IP

### Problem: API fails to start

Check:

- `.env` values
- `DATABASE_URL`
- `APP_SECRET`
- `docker compose logs api`

### Problem: Database connection fails

Check:

- Postgres container status
- credentials in `.env`
- `docker compose logs db`

### Problem: App worked before, then broke after restart

Check:

- whether IP changed
- whether Docker is enabled on boot
- whether containers restarted correctly

## 36. How to explain AWS deployment in interview

Simple answer:

> I deployed the project to a Linux EC2 instance on AWS, installed Docker and Docker Compose, configured environment variables, and ran the three-tier app as separate containers for frontend, API, and PostgreSQL. I also used security groups for network access and verified the deployment with container health checks and logs.

If they ask what you would improve next, say:

- move DB to RDS
- add HTTPS
- add CI/CD
- use Terraform
- use an ALB

## 37. What to say when showing this project to recruiters

You can say:

> I wanted to build something that shows both application understanding and cloud deployment basics. So I created a three-tier dashboard, added admin and customer roles, containerized the stack, and prepared it to run on AWS EC2 with Docker Compose.

## 38. Final summary

The easiest AWS deployment path for this project is:

1. launch EC2
2. open the right security group ports
3. SSH into the instance
4. install Docker
5. copy the project
6. create `.env`
7. run `docker compose up --build -d`
8. test the app

That is enough to turn this project into a real cloud demo.

For a beginner, that is a very good achievement.
