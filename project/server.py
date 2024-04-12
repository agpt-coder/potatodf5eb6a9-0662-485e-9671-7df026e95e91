import logging
from contextlib import asynccontextmanager

import project.retrieve_potato_photo_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="potato",
    lifespan=lifespan,
    description="The task involves creating an API that accepts any input/api call and returns a photo of a potato. Based on the discussion and information gathered: \n1. The photo can be fetched from the web, without a preference for a specific database or online resource. \n2. For sourcing potato photos, the Unsplash API or the Pexels API can be utilized. Both platforms offer free APIs to search for and retrieve high-quality images, including photos of potatoes.\n\nFor the tech stack, considering the requirement and available options:\n- **Programming Language:** Python\n- **API Framework:** FastAPI\n- **Database:** PostgreSQL\n- **ORM:** Prisma\n\nThis stack is suitable for building a performant and scalable API. Python and FastAPI will enable rapid development and easy integration with external APIs like Unsplash or Pexels for fetching potato photos. PostgreSQL, along with Prisma, provides a powerful and flexible back-end storage solution.\n\n**Implementation Overview:**\nThe API will be designed to accept any input through a predefined endpoint. Upon receiving a request, it will interact with either Unsplash or Pexels API to retrieve a potato photo. The image URL or the image itself can be returned as the response to the client.\n\n**Considerations:**\n- Ensuring API key security for Unsplash or Pexels.\n- Handling rate limits and usage quotas of the external APIs.\n- Implementing caching strategies to improve response times and reduce API calls.\n- Providing error handling for scenarios where potato photos cannot be retrieved.",
)


@app.get(
    "/potato-photo",
    response_model=project.retrieve_potato_photo_service.RetrievePotatoPhotoResponse,
)
async def api_get_retrieve_potato_photo(
    query: str,
) -> project.retrieve_potato_photo_service.RetrievePotatoPhotoResponse | Response:
    """
    Endpoint to retrieve a potato photo based on any user input.
    """
    try:
        res = await project.retrieve_potato_photo_service.retrieve_potato_photo(query)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
