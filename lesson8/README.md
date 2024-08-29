### Basic REST API to interact with [CVE database](https://github.com/CVEProject/cvelistV5).

## Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. Run PostgreSQL container:

	```shell
	docker run -e POSTGRES_PASSWORD=<password> -e POSTGRES_USER=<user> -e POSTGRES_DB=cve_list -p 5432:5432 -d postgres:latest
	```

3. In case you want to work with real CVE data, please refer to [lesson6](https://github.com/Karinmia/rd-async-course/blob/main/lesson6) and run the script to setup your database.


## Setup

1. Setup your virtual environment and install dependencies:

   ```shell
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create .env file in the /app folder and fill in credentials for your database, according to [env.example](https://github.com/Karinmia/rd-async-course/blob/main/lesson8/app/env.example) file.
