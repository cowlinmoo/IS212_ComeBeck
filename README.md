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
