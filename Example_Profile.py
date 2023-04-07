from ENCard import encard
import asyncio

async def generator_profile(uid): 
    s = time.time()
    async with encard.ENCard(lang = "en") as enc:
        result = await enc.create_profile(uid)

    print("―"*(len(f"✦ {result.name}〔{result.uid}〕✦")+10))
    print("―"*4 + f"✦ {result.name}〔{result.uid}〕✦"+"―"*4)
    print("―"*(len(f"✦ {result.name}〔{result.uid}〕✦")+10))
    print(f"✦Charter: {result.charter_name[:-2]}〔{len(result.charter)}〕✦\n")
    if result.charter != []:
        for character in result.charter:
            print("―"*4 + f"✦ {character.name}〔{character.id}〕✦"+"―"*4)
            print("―"*4 + f"✦ {character.icon}〕✦"+"―"*4)
            print("―"*6 + f"✦〔{character.element}〕✦"+"―"*6)
            print("\n\n")
    else:
        print("―"*6 + f"✦〔Make the character stand visible〕✦"+"―"*6)
    print(f"Image: {result.card}")

asyncio.run(generator_profile(724281429)) 
