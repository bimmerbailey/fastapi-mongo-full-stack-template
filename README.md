# Social Media Scrapper For Financial Data

## Current Container Setup

| Container Name | Image                | Purpose            |
|----------------|----------------------|--------------------|
| postgres       | mongo:6.0.3          | database           |
| backend        | python:3.11.0-alpine | backend (FastAPI)  |              |
| frontend       | node:18.2-alpine3.15 | vue.js application |

## Project Start

1) Open cmd/terminal in project root (where this file is)
2) run `bin/dev start --build` to build and run the docker containers
    * You might have to give exec rights to `bin/dev` file
3) Once backend and frontend containers are running, use [localhost:3000](http://localhost:3000) to display the frontend

## Project Commands

1) To stop Docker containers run `bin/dev stop`
    1) To stop and delete volumes run `bin/dev dump`
2) Create development data for testing run `bin/dev dev_data`
3) To create a shell into a container run `bin/dev shell {container_name}`
    1) example: `bin/dev shell mongo` to shell into mongo container
4) To run backend tests `bin/test {extra_pytest_args}`

## Interactive API Documentation

Use [localhost:8000/docs](http://localhost:8000/docs) to interact with API from the browser