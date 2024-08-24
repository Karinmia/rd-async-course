### Read [CVE database](https://github.com/CVEProject/cvelistV5) as JSON files and load its data into a database.

## Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. Run PostgreSQL container:

	```shell
	docker run -e POSTGRES_PASSWORD=<password> -e POSTGRES_USER=<user> -e POSTGRES_DB=cve_list -p 5432:5432 -d postgres:latest
	```

3. Download CVE files using Github:
	```shell
	git clone https://github.com/CVEProject/cvelistV5 --depth=1
	```

	--depth=1 helps to not clone all the history of repository

## Setup

1. Setup your virtual environment and install dependencies:

   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create .env file in the /app folder and fill in credentials for your database, according to [env.example](https://github.com/Karinmia/rd-async-course/blob/main/lesson6/app/env.example) file.

3. Apply alembic migrations on your database:

   ```shell
   alembic upgrade head
   ```

4. Run the script:

   ```shell
   python main.py
   ```
