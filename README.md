---
date: 2024-04-12T17:05:46.982838
author: AutoGPT <info@agpt.co>
---

# potato

The task involves creating an API that accepts any input/api call and returns a photo of a potato. Based on the discussion and information gathered: 
1. The photo can be fetched from the web, without a preference for a specific database or online resource. 
2. For sourcing potato photos, the Unsplash API or the Pexels API can be utilized. Both platforms offer free APIs to search for and retrieve high-quality images, including photos of potatoes.

For the tech stack, considering the requirement and available options:
- **Programming Language:** Python
- **API Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** Prisma

This stack is suitable for building a performant and scalable API. Python and FastAPI will enable rapid development and easy integration with external APIs like Unsplash or Pexels for fetching potato photos. PostgreSQL, along with Prisma, provides a powerful and flexible back-end storage solution.

**Implementation Overview:**
The API will be designed to accept any input through a predefined endpoint. Upon receiving a request, it will interact with either Unsplash or Pexels API to retrieve a potato photo. The image URL or the image itself can be returned as the response to the client.

**Considerations:**
- Ensuring API key security for Unsplash or Pexels.
- Handling rate limits and usage quotas of the external APIs.
- Implementing caching strategies to improve response times and reduce API calls.
- Providing error handling for scenarios where potato photos cannot be retrieved.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'potato'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
