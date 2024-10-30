# ComeBeck WFH Tracker 👨🏻‍💻 - IS212 G9T7

[Click here to access ComeBeck WFH Tracker!](https://comebeckwfhtracker.systems/)
```
   ____                     ____            _    
  / ___|___  _ __ ___   ___| __ )  ___  ___| | __
 | |   / _ \| '_ ` _ \ / _ \  _ \ / _ \/ __| |/ /
 | |__| (_) | | | | | |  __/ |_) |  __/ (__|   < 
  \____\___/|_| |_| |_|\___|____/ \___|\___|_|\_\
                                                 
    W F H     M A N A G E M E N T    S Y S T E M
```
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python%203-ffd343?style=for-the-badge&logo=python&logoColor=2b5b84)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

## API Documentation

The API documentation is served using *Swagger*. You may access it using:

**Hosted Environment:** <https://api.comebeckwfhtracker.systems/api/documentation>

**Local Environment:** <https://localhost:8080/api/documentation>

## Table of Contents

- [What is ComeBeck WFH Tracker?](#what-is-comebeck-wfh-tracker)
- [Getting Started](#getting-started)
- [Overview of Steps to run ComeBeck WFH Tracker Locally](#overview-of-steps-to-run-comebeck-wfh-tracker-locally)

## What is ComeBeck WFH Tracker
ComeBeck WFH Tracker is an all-in-one work-from-home management platform that enables employees to apply for, view, and manage their remote work arrangements. The platform is designed to be intuitive and efficient, providing a streamlined experience for both employees and managers to coordinate in-office and remote schedules.

Built with the `FastAPI` framework, ComeBeck WFH Tracker offers a fast and scalable backend supported by a `PostgreSQL` database to securely manage user and schedule data. A `React` front-end ensures a responsive and user-friendly interface for all users. In production, the front end is hosted on `Vercel`, while the backend operates in a Dockerized environment on an `Azure Container Apps`, providing a reliable, cloud-based solution for seamless work-from-home tracking and approval workflows.

## Getting Started

**Want to run ComeBeck WFH Tracker locally? Great!** This section guides you through setting up the development environment and describes how to run it on your machine.

**Just want to access ComeBeck WFH Tracker via the web? No problem!** You can skip the local setup and head straight to the deployed version at: [Link To Deployed Site](https://comebeckwfhtracker.systems/)

## Overview Of Steps To Run ComeBeck WFH Tracker Locally

**Required Tools:**

- **`Node.js` (v18.17.0)**: Node.js is a JavaScript runtime environment used for frontend development in this project. You can download and install it from the official website: [Node.js](https://nodejs.org/en/)
- **`Python` (3.12.3)**: Python is the programming language used for the backend development of ComeBeck WFH Tracker with FastAPI. Download and install the Python version 3.12.3 from the official website: [Python](https://www.python.org/downloads/release/python-3123/)
- **`Poetry`**: Poetry is a dependency management and packaging tool for Python. It is used to handle project dependencies and virtual environments in the backend. You can install Poetry by following the instructions on the official website: [Poetry](https://python-poetry.org/docs/)
- **`Docker` (ensure it's running)**: Docker is a containerization platform used to run the backend application. You can find installation instructions and resources on the official website: [Docker](https://www.docker.com/get-started)
- **`Docker Compose` (recommended)**: Docker Compose is a tool for managing multi-container Docker applications. It simplifies running applications with multiple interdependent services. Install instructions can be found on the official website: [Docker Compose](https://docs.docker.com/compose/install/)

**Steps**

1. Clone the repository
2. Navigate to the repository directory
3. Ensure docker is running
4. Setting Up Environment Variables
5. Start the Backend server
6. Start the Frontend server
7. Enjoy ComeBeck WFH Tracker 👨🏻‍💻

### Set Up Environment Variables

To run ComeBeck WFH Tracker locally, you need to create two `.env` files to store sensitive information (secrets).

### Overview of the `.env` files needed
- **`.env` file for Frontend:** This file stores environment variables specific to your frontend development environment.
- **`.env` file for Backend:** This file stores environment variables specific to your backend development environment

#### `.env` file for Frontend

1. **Location:** Create a file named `.env` in the root directory of your frontend project. This is the same directory that contains your `package.json` file. The image provides a visual representation of this location.

<img src="./readme_files/FrontendEnvExample.png" width="350px">

2. **Content:** The `.env` file should include environment variables specific to 
   your frontend development setup. Here’s an example configuration for <strong><em>development environment</em></strong>:
   ```
    # URL for local development, pointing to the backend server
    NEXT_PUBLIC_API_BASE_URL=http://localhost:<PORT>/api
   ```
   Replace <PORT> with the port number your backend server is running on, typically 
   8080 during development. Alternatively, for <strong><em>production environment</em></strong>:
    ```
    NEXT_PUBLIC_API_BASE_URL=https://api.comebeckwfhtracker.systems/api/
    ```
#### `.env` file for Backend
1. **Location:** Create a file named `.env` in the root directory of the entire project. This is the same directory that contains your `docker-compose.yml` file. The image provides a visual representation of this location.

<img src="./readme_files/BackendEnvExample.png" width="350px">

2. **Content:** The `.env` file should include environment variables specific to 
your backend development setup. Here’s an example configuration for the <strong><em>development environment</em></strong>:

```
# Development environment variables
CURRENT_ENV=DEV
DATABASE_DIALECT=postgresql
DATABASE_HOSTNAME=localhost
POSTGRES_DB=<POSTGRES_DB>
POSTGRES_USER=<POSTGRES_USER>
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
POSTGRES_PORT=5432
DEBUG_MODE=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=<SENDER_EMAIL> # Email to send automated notifications about WFH related events 
SENDER_PASSWORD=<SENDER_PASSWORD>
```

For the <strong><em>production</em></strong> environment, replace the database credentials and host information as follows:

```
# Production environment variables
CURRENT_ENV=PROD
PRODUCTION_DB_USER=<PRODUCTION_DB_USER>
PRODUCTION_DB_PASSWORD=<PRODUCTION_DB_PASSWORD>
PRODUCTION_DB_HOSTNAME=comebeck.postgres.database.azure.com
PRODUCTION_DB_PORT=5432
PRODUCTION_DB_NAME=<PRODUCTION_DB_NAME>
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=<SENDER_EMAIL> # Email to send automated notifications about WFH related events 
SENDER_PASSWORD=<SENDER_PASSWORD>
```

### Start the Backend server

To start the backend server locally and connect to the <strong><em>local database</em></strong> run the following commands

```
docker-compose --profile dev up
```
Alternatively, to start the backend server locally and connect to the <strong><em>production database</em></strong> run the following commands

```
docker-compose --profile prod up
```

### Running Frontend Server

To start the frontend server, run the following command:
```
cd frontend # if you are not already in the frontend directory
npm install # to install the required dependencies
npm run dev # to start the development server
```

## Login Credentials
| Role    | Email                     | Password    |
|---------|---------------------------|-------------|
| HR      | colinmok1000@gmail.com    | password123 |
| STAFF   | colinmok3@gmail.com       | password123 |
| MANAGER | colinmokhengyee@gmail.com | password123 |

For testing purposes, we have inserted all `554 employees` of All In One with the 
same password `password123`. You can use the corresponding email addresses to login. However, please note that certain pages/functionalities are restricted to specific roles.

- `Department Schedule Page` is only accessible to `HR` roles.
- `Department Schedule Tab` inside Schedule page is only accessible to `HR` roles.
- `Team Members I Manage Tab` inside Schedule page is only accessible to `MANAGER` roles.

## Tech Stack of ComeBeck WFH Tracker
<img src="./readme_files/ComeBeckWFHTrackerTechStack.png" width="600px">

## Solution Architecture of ComeBeck WFH Tracker
<img src="./readme_files/ComeBeckCloudArchitecture.png" width="600px">

## Contributors

#### G9 Team 7 (Beck)

<table>
    <tr>
        <td align="center"><img src="readme_files\mok.jpg"width="150px"/><br/><sub><b>Colin Mok</b></sub></a></td>
        <td align="center"><img src="readme_files\chester.jpg"width="150px"/><br/><sub><b>Chester Lim</b></sub></a></td>
        <td align="center"><img src="readme_files\yoon.jpg"width="150px"/><br/><sub><b>Daryl Yoon</b></sub></a></td>
        <td align="center"><img src="readme_files\nicholas.png"width="150px"/><br/><sub><b>Nicholas Goh</b></sub></a></td>
        <td align="center"><img src="readme_files\joen.jpg"width="150px"/><br/><sub><b>Joen Tan</b></sub></a></td>
    </tr>
</table>