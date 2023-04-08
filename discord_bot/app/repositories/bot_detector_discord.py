import aiohttp


class BotDetectorAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def _get(self, endpoint, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}{endpoint}", headers=self.headers, params=params
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise ValueError(
                        f"Failed to fetch {endpoint} with status code {resp.status}"
                    )

    async def _post(self, endpoint, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}{endpoint}", headers=self.headers, json=data
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise ValueError(
                        f"Failed to post to {endpoint} with status code {resp.status}"
                    )

    async def _put(self, endpoint, data):
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.base_url}{endpoint}", headers=self.headers, json=data
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise ValueError(
                        f"Failed to put to {endpoint} with status code {resp.status}"
                    )

    async def _delete(self, endpoint, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.base_url}{endpoint}", headers=self.headers, params=params
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise ValueError(
                        f"Failed to delete {endpoint} with status code {resp.status}"
                    )

    async def health(self):
        return await self._get("/v1/monitoring/health/")

    async def read_discord_verification(self, verification_id, player_id):
        params = {"verification_id": verification_id, "player_id": player_id}
        return await self._get("/v1/verifications/", params=params)

    async def update_discord_verification(self, verification_id, verified_status):
        params = {"verification_id": verification_id}
        data = {"verified_status": verified_status}
        return await self._put("/v1/verifications/", data=data, params=params)

    async def create_discord_verification(self, data):
        return await self._post("/v1/verifications/", data=data)

    async def delete_discord_verification(self, verification_id):
        params = {"verification_id": verification_id}
        return await self._delete("/v1/verifications/", params=params)

    async def get_discord_event(self, event_id, event_name):
        params = {"event_id": event_id, "event_name": event_name}
        return await self._get("/v1/discord-events/", params=params)

    async def update_discord_event(self, data):
        return await self._put("/v1/discord-events/", data=data)

    async def create_discord_event(self, event_name):
        data = {"title": event_name}
        return await self._post("/v1/discord-events/", data=data)

    async def delete_discord_event(self, event_id):
        params = {"event_id": event_id}
        return await self._delete("/v1/discord-events/", params=params)

    async def list_discord_events(self, status=None):
        params = {}
        if status:
            params["status"] = status
        return await self._get("/v1/discord-events/", params=params)

    async def get_discord_event_attendees(self, event_id):
        params = {"event_id": event_id}
        return await self._get("/v1/discord-events/attendees/", params=params)

    async def update_discord_event_attendee(self, data):
        return await self._put("/v1/discord-events/attendees/", data=data)

    async def create_discord_event_attendee(self, data):
        return await self._post("/v1/discord-events/attendees/", data=data)

    async def delete_discord_event_attendee(self, attendee_id):
        params = {"attendee_id": attendee_id}
        return await self._delete("/v1/discord-events/attendees/", params=params)
