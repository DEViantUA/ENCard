# ENCard

ENCard - Add-on for module: https://github.com/DEViantUA/EnkaCard 

Example run is in the file: ``Example.py``

To run: Download the folder: ``encard`` and put it together with the file ``Example.py`` in the same directory, then run the code through the file: ``Example.py``



```py
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

```


# Result:

<p align="center">
 <img src="https://github.com/DEViantUA/ENCard/blob/main/%D0%A1%D0%B0%D0%B9%D0%BD%D0%BE_30_03_2023%2016_43.png" alt="Баннер"/>
</p>
