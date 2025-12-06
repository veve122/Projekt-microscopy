🔬 Správca Databázy Elektrónových Mikroskopov (EM Manager)

Jednoduchý interaktívny Python program na správu záznamov o práci na elektrónových mikroskopoch. Dáta sú uložené v tabuľkovom formáte (Pandas DataFrame) a perzistentne ukladané do lokálneho CSV súboru.

🌟 Kľúčové Vlastnosti

    Dáta sú automaticky ukladané do súboru em_zaznamy.csv a načítané pri každom spustení programu.

    Pridávanie záznamov: Zaznamenanie mena, dátumu, mikroskopu, vzorky a vykonaných analýz.

    Aktualizácia nedokončených úloh: Možnosť označiť existujúci nedokončený záznam ako hotový alebo upraviť detaily.

    Prehľad a Filtrovanie: Zobrazenie všetkých záznamov v prehľadnej tabuľke (Pandas DataFrame) a filtrovanie podľa mena, mikroskopu, dokončenia a typu analýzy.

🚀 Požiadavky a Inštalácia

Tento program vyžaduje, aby bol v systéme nainštalovaný Python 3 a knižnica Pandas.

💻 Spustenie a Použitie

    Uložte kód do súboru (napr. em_manager.py).

    Spustite program z príkazového riadku (terminálu):
    Bash

    python em_manager.py

    Program zobrazí interaktívne menu.

Popis

1	Pridať nový záznam: Interaktívne zadávanie všetkých detailov práce.
2	Zobraziť všetky záznamy: Vypíše kompletnú tabuľku dát (DataFrame).
3	Aktualizovať/Dokončiť záznam: Umožní vybrať nedokončený záznam podľa indexu a zmeniť jeho status/detaily.
4	Filtrovať záznamy: Umožní filtrovať dáta podľa mena, mikroskopu alebo statusu dokončenia.
5	Ukončiť program: Ukončí aplikáciu a uloží aktuálny stav databázy na disk.

