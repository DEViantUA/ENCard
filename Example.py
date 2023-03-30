from encard import encard
import asyncio


async def generator_card(uid): 
    async with encard.ENCard(lang = "en") as enc:
        result = await enc.create_cards(uid)
        print("―"*(len(f"✦ {result.name} 〔{result.uid}〕✦")+10))
        print("―"*4 + f"✦ {result.name} 〔{result.uid}〕✦"+"―"*4)
        print("―"*(len(f"✦ {result.name} 〔{result.uid}〕✦")+10)+"\n")
        for character in result.card:
            print("―"*4 + f"✦ {character.name} 〔{character.id}〕✦"+"―"*4)
            print("―"*6 + f"✦〔{character.element}〕✦"+"―"*6)
            print(f"Image: {character.card}\n\n")

asyncio.run(generator_card(724281429))  