Instrukce k projektu AUDIO steganografie

Úlohou tohoto programu je vložit libovolnou textovou zprávu a schovat ho do audiosouboru formátu .waw pomocí metody LSB.
Zároveň nabízí dekódování souboru, ve kterém může být schována zpráva. Dodatkově splňuje i funkci jednoduchého
AudioPlayera přímo v konzoli.

Program je docela solidně popsán přímo v kódu vždy na začátku metod.
Proto zde budou pouze instrukce k pohybování se v konzoli a k ověření funkčnosti programu.

Stručně vnitřní logika celého programu:
	Kódování probíhá pomocí bitových operandů AND (&) a OR (|). Konkrétní byte se jakoby porovná s "maskou".
	Nejdříve vždy AND s hodnotou 254 (tedy "maskou" 1111 1110).	To nám zajistí, že původních 7 bitů zůstane jako
	původních a poslední se přepíše na nulu. Poté se provádí OR s našim bitem, který chceme zapsat (tedy 0000 000[0/1]),
	takže na poslední pozici se zapíše ta hodnota, kterou chceme. Tohle je popsané i v kódu a bude detailně
	vysvětleno v prezentaci.

	Ještě jedna věc: dohodli jsme se na jeden charakter použít ne 8, ale 16 bitů. Je to z důvodu, že některé
	znaky (např. š) mají hodnotu Unicode větší, než 255, takže je bitově lze zapsat až na 9 bitů. Díky tomu zpráva
	podporuje všelijaké speciální znaky (např. \|€Łł][Đđ#&@{}Ł$¸÷$¨˝´˙˘). Díky obrovských kapacitách, které
	průměrné zvukové soubory mají, jsme byli schopni obětovat maximální délku zprávy na polovinu.

	Veškerá chybovost programu je odchycena úplně nahoře v ConsoleMenu, kde se uživateli píše,
	co vzniklo za chybu a vrátí ho do hlavního menu.

Instrukce k programu:
    Hlavní konfigurace puštění programu padá na třídu Main.py. Ta nedělá nic jiného, než zavolá ConsoleMenu().
    Poté se nám v konzoli objeví "MAIN MENU" s možnostmi:
		1: Encode
		2: Decode
		3: Open custom AudioPlayer
		4: Exit

	Vše samozřejmě funguje zádáním čísla (té možnosti) do konzole, kde se nám otevře dodatečná nabídka.
	
	Následující možnosti:

	1:Encode
		Když zadáme číslo pro tuto nabídku tak se nám objeví seznam písniček, které máme na výběr pro zakodování
		(z projektové složky/wavSamples/*) nebo můžeme zadat vlastní soubor, ale musíme pak napsat absolutní cestu.
		Dále si zvolíme třeba píseň s číslem jedna.

		Zadáme čislo jedna a vypíše se progress otevírání. Posléze musíme zadat, do kterého bytu chceme zapisovat.
		Můžeme si zvolit jakékoliv číslo (číslo 1 reprezentuje zapisování na každý byte od začátku, číslo 2 znamená
		zápis na každý druhý byte, 3 - třetí, atd...) Pokud číslo bude větší, než je velikost samotného programu,
		program uživatele upozorní na chybu a možnost na zadání nabídne znovu.

		Následuje vybídnutí napsat zprávu, kterou chceme schovat (předtím ještě však program vypíše, kolik znaků
		se maximálně může zapsat. Ovšem pozor! Nesmí se zadat jeden speciálni znak '#',	který pomahá v algoritmu
		při de/kodování.

		Následuje dotaz, jestli chceme zbývající LSB naplnit "jakoby solí". Tato funkce je zde čistě k ověření
		funkčnosti programu a k ověření teorií (jelikož samotná zpráva bez soli	nejde v souboru vůbec slyšet).

		Po tomto kroku se dokonči kódování.
	2:Decode
		Možnost sloužící k vypsání skryté zprávy.

		Nejdříve vypíše soubory, ze kterých můžeme vybírat (stejné jako	u Encode).

		Následuje dotaz, každý kolikátý byte má program číst. Funguje to současně i jako bezpečností prvek
		protože, když útočník neví na kolikátém každem bitu je zakodovaná zpráva, tak to bude složitější exploitnout.
		Nicméně pro testovací účely je tato informace obsažena přímo v názvu už zašifrovaného souboru.

		Následuje samotný proces dekódování a jestli je úspešný, tak se zobrazí skrytá zpráva.
	3:Open custom AudioPlayer
		Tato možnost nám nabízí otevření jednoduchého audioplayeru a jeho poslechnutí (ať už zašifrovaného či nikoliv
		- vytvořeno, aby se nemuselo nonstop pouštět např. VLC pro otestování).

		Zase dostaneme na výběr z několika souborů nebo můžeme napsat vlastní cestu k audiosouboru.

		Posléze nám to napíše jestli byl soubor úspěšně	otevřen a nabídne nám to možnosti:
			1:Play/Unpause - pustí nebo odpauzuje song
			2:Pause - stopne song
			3:Start from the beginning - spustí song od začátku
			4:Increase volume - zvýší hlasitost
			5:Decrease volume - sníží hlasitost
			6:Exit - ukončí audioPlayera

	    Zase se možnosti zadávají do konzole pomocí čísel. Po zadání 10 hodnot se nabídka s možnostmi vypíše znovu,
	    protože ta původní by v konzoli už nemusela být vidět.
	4:Exit
		Tato možnost ukončí celý program.

Ověření funkčnosti:
	Bude stačit pomocí Encode vybrat nějaký soubor (pro testing máme defaultně soubory s 2 písničkami a jedním
	mluveným slovem), vybrat si možnosti a zprávu (pro tyto účely je v komentáři v souboru test.py předloha zprávy,
	která obsahuje větší množství speciálních znaků). Následně pomocí decode otevřít zašifrovaný (nově vytvořený)
	soubor ze stejné složky. Jinak konzole je celkem straight-forward, takže pro testování funkčnosti si
	v podstatě stačí chvíli s programem hrát.

Použité knihovny
	wave - Tato knihovna nám pomáhá pracovat se soubory formátu .waw. (zejména otevírání, získávání parametrů,
	    získávání framů a vytváření z framů nový soubor)
	pygame - Díky této knihovně může fungovat náš custom audioPlayer, protože funkce na spouštění audisouborů
	    se nachází v této knihovně.
	os + sys - Knihovny na práci ze složkami a soubory. (hlavně k získání absolutní cesty složky, ve kterém
	    je celý projekt uložen)

Projekt: AUDIO Steganografie
Autoři: Dzadíková Slavomíra, Janout Vladimír, Končitý Patrik, Muzikant Petr

