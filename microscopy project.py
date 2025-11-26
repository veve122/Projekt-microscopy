import pandas as pd
from datetime import datetime

# Definícia možností pre konzistentnosť dát
MOZNE_MIKROSKOPY = ["Jeol JSM6610", "Jeol 7600F", "Zeiss"]
MOZNE_ANALYZY = ["EDX", "EBSD", "WDS", "SE/BSE Imaging"]

class EM_Zaznam:
    """Reprezentuje jeden záznam o práci na elektrónovom mikroskope."""
    def __init__(self, meno, datum, mikroskop, vzorka, analyzy, dokonceny=False):
        self.meno = meno
        self.datum = datum
        self.mikroskop = mikroskop
        self.vzorka = vzorka
        self.analyzy = analyzy
        self.dokonceny = dokonceny
    
    def __str__(self):
        status = "Áno" if self.dokonceny else "Nie"
        return f"[{self.datum}] {self.meno} na {self.mikroskop} (Vzorka: {self.vzorka}, Analýzy: {', '.join(self.analyzy)}, Dokončené: {status})"

class EM_Databaza:
    """Spravuje databázu záznamov o práci na mikroskopoch pomocou Pandas DataFrame."""
    def __init__(self):
        # Inicializácia prázdneho DataFrame
        self.stlpce = ["Meno", "Dátum", "Mikroskop", "Vzorka", "Analýzy", "Dokončené"]
        self.df = pd.DataFrame(columns=self.stlpce)
    
    def pridat_zaznam(self, zaznam: EM_Zaznam):
        """Pridá nový záznam do DataFrame."""
        # Vytvoríme nový riadok ako Series (séria)
        novy_riadok = pd.Series({
            "Meno": zaznam.meno,
            "Dátum": zaznam.datum,
            "Mikroskop": zaznam.mikroskop,
            "Vzorka": zaznam.vzorka,
            # Analýzy uložíme ako reťazec oddelený čiarkou pre jednoduchšie zobrazenie
            "Analýzy": ", ".join(zaznam.analyzy),
            "Dokončené": "Áno" if zaznam.dokonceny else "Nie"
        })
        
        # Pridáme nový riadok do DataFrame
        # Používame pd.concat na pridanie riadku, resetujeme index
        self.df = pd.concat([self.df, novy_riadok.to_frame().T], ignore_index=True)
        print("✅ Záznam bol úspešne pridaný.")
    
    def zobrazit_tabulku(self):
        """Zobrazí celý DataFrame."""
        if self.df.empty:
            print("Databáza je prázdna.")
            return
        # Nastavíme možnosť zobrazenia všetkých stĺpcov/riadkov
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print("\n--- 📋 PREHĽAD VŠETKÝCH ZÁZNAMOV ---")
        print(self.df)
        print("------------------------------------\n")
    
    def filtrovat(self, **kwargs):
        """
        Filtruje DataFrame na základe zadaných kritérií (napr. meno='Peter', dokončené='Nie').
        """
        if self.df.empty:
            print("Databáza je prázdna, nie je čo filtrovať.")
            return
        
        df_filtrovany = self.df.copy()
        
        # Aplikovanie filtrov
        for stlpec, hodnota in kwargs.items():
            # Zabezpečíme, že názov stĺpca existuje v DataFrame
            if stlpec in self.df.columns:
                # Použijeme metódu .str.contains() pre filtrovanie analýz, kde je viac možností
                if stlpec == "Analýzy":
                    df_filtrovany = df_filtrovany[df_filtrovany[stlpec].str.contains(hodnota, case=False, na=False)]
                else:
                    # Štandardné filtrovanie pre iné stĺpce
                    df_filtrovany = df_filtrovany[df_filtrovany[stlpec] == hodnota]
            else:
                print(f"Upozornenie: Stĺpec '{stlpec}' neexistuje.")
        
        if df_filtrovany.empty:
            print(f"\n❌ Pre zadané kritériá ({kwargs}) neboli nájdené žiadne záznamy.")
        else:
            print(f"\n--- 🔎 VÝSLEDOK FILTROVANIA ({kwargs}) ---")
            print(df_filtrovany)
            print("-------------------------------------------\n")
            
        return df_filtrovany

def input_zaznam():
    """Získa vstupy od užívateľa a vytvorí objekt EM_Zaznam."""
    print("\n--- 📝 ZADANIE NOVÉHO ZÁZNAMU ---")
    
    # 1. Meno a Dátum
    meno = input("Meno pracovníka: ")
    datum = datetime.now().strftime("%Y-%m-%d") # Automatické nastavenie dnešného dátumu
    print(f"Dátum práce: {datum}")
    
    # 2. Výber Mikroskopu
    print("\n--- Dostupne mikroskopy ---")
    for i, m in enumerate(MOZNE_MIKROSKOPY):
        print(f"{i+1}. {m}")
    while True:
        try:
            vyber = int(input(f"Vyberte číslo mikroskopu (1-{len(MOZNE_MIKROSKOPY)}): "))
            if 1 <= vyber <= len(MOZNE_MIKROSKOPY):
                mikroskop = MOZNE_MIKROSKOPY[vyber - 1]
                break
            else:
                print("Neplatný výber.")
        except ValueError:
            print("Prosím, zadajte číslo.")
            
    # 3. Vzorka
    vzorka = input("Názov/ID vzorky: ")
    
    # 4. Výber Analýz
    vybrane_analyzy = []
    print("\n--- Dostupne analyzy (možno vybrať viac) ---")
    for i, a in enumerate(MOZNE_ANALYZY):
        print(f"{i+1}. {a}")
    
    while True:
        vstupy = input(f"Zadajte čísla analýz oddelené čiarkou (napr. 1,3,4) alebo stlačte Enter pre koniec: ")
        if not vstupy:
            if not vybrane_analyzy:
                 print("⚠️ Musíte vybrať aspoň jednu analýzu!")
                 continue
            break
            
        try:
            cisla = [int(c.strip()) for c in vstupy.split(',')]
            validne_cisla = True
            for cislo in cisla:
                if 1 <= cislo <= len(MOZNE_ANALYZY):
                    analyza = MOZNE_ANALYZY[cislo - 1]
                    if analyza not in vybrane_analyzy:
                        vybrane_analyzy.append(analyza)
                else:
                    print(f"Neplatné číslo analýzy: {cislo}")
                    validne_cisla = False
            if validne_cisla:
                break
        except ValueError:
            print("Prosím, zadajte čísla oddelené čiarkou.")
            
    # 5. Dokončenie
    while True:
        dokonceny_input = input("Bola práca dokončená? (A/N): ").upper()
        if dokonceny_input in ['A', 'ÁNO', 'YES']:
            dokonceny = True
            break
        elif dokonceny_input in ['N', 'NIE', 'NO']:
            dokonceny = False
            break
        else:
            print("Neplatný vstup. Zadajte 'A' pre Áno alebo 'N' pre Nie.")

    return EM_Zaznam(meno, datum, mikroskop, vzorka, vybrane_analyzy, dokonceny)

# --- Hlavná časť programu ---
def main():
    databaza = EM_Databaza()
    
    # 1. Pridanie počiatočných testovacích dát
    databaza.pridat_zaznam(EM_Zaznam("Peter K.", "2025-11-20", "Mikroskop A", "Vz. 101", ["EDX", "EBSD"], True))
    databaza.pridat_zaznam(EM_Zaznam("Mária V.", "2025-11-21", "Mikroskop B", "Vz. 204", ["SE/BSE Imaging"], False))
    databaza.pridat_zaznam(EM_Zaznam("Ján S.", "2025-11-21", "Mikroskop A", "Vz. 102", ["EDX", "WDS"], False))
    databaza.pridat_zaznam(EM_Zaznam("Peter K.", "2025-11-22", "Mikroskop C", "Vz. 301", ["EBSD"], True))
    
    while True:
        print("\n==================================")
        print("🔬 EM Databáza Pracoviska - MENU")
        print("==================================")
        print("1. Pridať nové meranie")
        print("2. Zobraziť všetky záznamy meraní")
        print("3. Aktualizovať/dokončiť meranie")
        print("4. Filtrovať záznamy maraní")
        print("5. Ukončiť program")
        
        vyber = input("\nZadajte číslo voľby: ").strip()
        
        if vyber == '1':
            try:
                novy_zaznam = input_zaznam()
                databaza.pridat_zaznam(novy_zaznam)
            except Exception as e:
                print(f"Nastala chyba pri zadávaní záznamu: {e}")
                
        elif vyber == '2':
            databaza.zobrazit_tabulku()
            
        elif vyber == '3':
            print("\n--- ⚙️ MOŽNOSTI FILTROVANIA (Zadajte hodnotu alebo nechajte prázdne) ---")
            
            filter_args = {}
            
            # Filter Meno
            meno = input("Filtrovať podľa Meno (napr. Peter K.): ")
            if meno:
                filter_args['Meno'] = meno
            
            # Filter Mikroskop
            mikroskop_input = input(f"Filtrovať podľa Mikroskop ({'/'.join(MOZNE_MIKROSKOPY)}): ")
            if mikroskop_input and mikroskop_input in MOZNE_MIKROSKOPY:
                filter_args['Mikroskop'] = mikroskop_input
            
            # Filter Dokončené
            dokoncenie = input("Filtrovať podľa Dokončené (Áno/Nie): ")
            if dokoncenie in ['Áno', 'Nie']:
                filter_args['Dokončené'] = dokoncenie
                
            # Filter Analýzy (ak záznam obsahuje danú analýzu)
            analyza_filter = input(f"Filtrovať podľa Analýzy (napr. EDX): ")
            if analyza_filter:
                filter_args['Analýzy'] = analyza_filter

            if filter_args:
                databaza.filtrovat(**filter_args)
            else:
                print("Neboli zadané žiadne kritériá pre filtrovanie.")

        elif vyber == '4':
            print("\nProgram bol ukončený. Dovidenia!")
            break
            
        elif vyber == '5':
            print("\nProgram bol ukončený. Dovidenia!")
            break
        
        else:
            print("Neplatná voľba. Skúste to znova.")

if __name__ == "__main__":
    main()