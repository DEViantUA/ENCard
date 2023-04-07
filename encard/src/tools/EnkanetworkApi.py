from enkanetwork import EnkaNetworkAPI,Assets

assets = Assets()


async def get_full_info(agent,lang,uid):
    async with EnkaNetworkAPI(user_agent = agent, lang=lang) as client:
        info = await client.fetch_user(uid)

    return info

async def get_charters(character_id):
    character = assets.character(character_id)
    
    return character