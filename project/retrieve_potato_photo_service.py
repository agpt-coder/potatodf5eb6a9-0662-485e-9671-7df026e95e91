from datetime import datetime, timedelta
from typing import Optional

import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class RetrievePotatoPhotoResponse(BaseModel):
    """
    The response model for the retrieval of a potato photo. It provides the necessary details about the photo fetched, including any pertinent metadata.
    """

    photo_url: str
    source: str
    is_cached: bool
    error: Optional[str] = None


async def retrieve_potato_photo(query: str) -> RetrievePotatoPhotoResponse:
    async with httpx.AsyncClient() as client:
        api_key = "your_api_key_here"
        is_cached = False
        cache = await prisma.models.Cache.prisma().find_unique(where={"key": query})
        if cache and cache.expiresAt > datetime.now():
            return RetrievePotatoPhotoResponse(
                photo_url=cache.value,
                source=cache.photoRequests[0].source,
                is_cached=True,
            )
        try:
            response = await client.get(
                f"https://api.unsplash.com/search/photos?query={query}&client_id={api_key}"
            )
            if response.status_code == 200:
                photo_data = response.json()
                photo_url = photo_data["results"][0]["urls"]["regular"]
                await prisma.models.Cache.prisma().create(
                    {
                        "key": query,
                        "value": photo_url,
                        "expiresAt": datetime.now() + timedelta(days=1),
                        "photoRequests": {
                            "create": {
                                "request": query,
                                "imageUrl": photo_url,
                                "source": "UNSPLASH",
                                "userId": "some_user_id",
                            }
                        },
                    }
                )
                return RetrievePotatoPhotoResponse(
                    photo_url=photo_url, source="Unsplash", is_cached=is_cached
                )
            else:
                return RetrievePotatoPhotoResponse(
                    photo_url="",
                    source="",
                    is_cached=False,
                    error="Failed to fetch photo from Unsplash.",
                )
        except httpx.RequestError as e:
            return RetrievePotatoPhotoResponse(
                photo_url="", source="", is_cached=False, error=f"Request Error: {e}"
            )
