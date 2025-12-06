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
    
    NAZOV_SUBORU = 'em_zaznamy.csv'
    
    def __init__(self):
        # Inicializácia prázdneho DataFrame
        self.stlpce = ["Meno", "Dátum", "Mikroskop", "Vzorka", "Analýzy", "Dokončené"]
        self.df = pd.DataFrame(columns=self.stlpce)
        self.nacitat_data()
        
    def nacitat_data(self):
        """Načíta dáta z CSV súboru, ak existuje."""
        try:
            # Pandas funkcia na čítanie CSV
            self.df = pd.read_csv(self.NAZOV_SUBORU)
            print(f"✅ Dáta úspešne načítané zo súboru '{self.NAZOV_SUBORU}'.")
            
            # Pri načítaní musíme zabezpečiť správne typy dát (ak by boli stratené)
            if 'Dátum' in self.df.columns:
                self.df['Dátum'] = pd.to_datetime(self.df['Dátum']).dt.strftime('%Y-%m-%d')
                
        except FileNotFoundError:
            # Ak súbor neexistuje, vytvorí sa prázdny DataFrame
            print(f"ℹ️ Súbor '{self.NAZOV_SUBORU}' nebol nájdený. Vytvára sa nová prázdna databáza.")
        except Exception as e:
            print(f"❌ Chyba pri načítaní dát: {e}. Vytvára sa nová prázdna databáza.")

    def ulozit_data(self):
        """Uloží aktuálny DataFrame do CSV súboru."""
        if not self.df.empty:
            # Pandas funkcia na uloženie do CSV. index=False zabráni uloženiu riadkových čísel
            self.df.to_csv(self.NAZOV_SUBORU, index=False)
            print(f"💾 Dáta úspešne uložené do súboru '{self.NAZOV_SUBORU}'.")
        else:
            print("💾 Databáza je prázdna.")
    
    def pridat_zaznam(self, zaznam: EM_Zaznam):
        """Pridá nový záznam do DataFrame a uloží ho."""
        # Vytvoríme nový riadok ako Series 
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
        self.df = pd.concat([self.df, novy_riadok.to_frame().T], ignore_index=True)
        print("✅ Záznam bol úspešne pridaný.")
        # Uložíme po každej zmene
        self.ulozit_data()
    
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
    
    def aktualizovat_zaznam(self):
        """Umožní užívateľovi vybrať nedokončený záznam a aktualizovať ho."""
        
        # 1. Nájdeme VŠETKY nedokončené záznamy
        nedokoncene_df = self.df[self.df['Dokončené'] == 'Nie'].copy()
        
        if nedokoncene_df.empty:
            print("\n✅ Všetky záznamy sú aktuálne dokončené, nie je čo aktualizovať.")
            return

        print("\n--- 🔄 NEDOKONČENÉ ZÁZNAMY NA AKTUALIZÁCIU ---")
        # Zobrazíme nedokončené záznamy s ich Pandas Indexom
        print(nedokoncene_df.to_string(index=True)) 
        print("--------------------------------------------------")

        while True:
            try:
                # Získame od užívateľa index (číslo riadku) záznamu
                index_na_aktualizaciu = int(input("Zadajte číslo indexu (riadku) záznamu, ktorý chcete aktualizovať, alebo -1 pre návrat: "))
                
                if index_na_aktualizaciu == -1:
                    return
                
                # Zistíme, či zadaný index existuje v pôvodnom DataFrame
                if index_na_aktualizaciu in self.df.index:
                    # Zistíme, či je záznam naozaj NEDOKONČENÝ
                    if self.df.loc[index_na_aktualizaciu, 'Dokončené'] == 'Nie':
                        break
                    else:
                        print("⚠️ Zadaný index už patrí dokončenému záznamu. Vyberte iný.")
                else:
                    print("❌ Zadaný index sa nenašiel v databáze.")
            except ValueError:
                print("Prosím, zadajte platné číslo indexu.")
                
        # 2. Aktualizácia záznamu
        
        # Vzorka
        stara_vzorka = self.df.loc[index_na_aktualizaciu, 'Vzorka']
        nova_vzorka = input(f"Vzorka (pôvodná: {stara_vzorka}). Nová hodnota (Enter pre zachovanie pôvodnej): ")
        if nova_vzorka:
            self.df.loc[index_na_aktualizaciu, 'Vzorka'] = nova_vzorka
            
        # Analýzy (jednoduchá aktualizácia: buď zmena alebo pridanie)
        stare_analyzy = self.df.loc[index_na_aktualizaciu, 'Analýzy']
        nove_analyzy = input(f"Analýzy (pôvodné: {stare_analyzy}). Nové pridané analýzy (napr. EBSD,WDS) alebo Enter: ")
        if nove_analyzy:
            # Nové analyzy pripojíme k existujúcim a odstránime duplikáty
            vsetky_analyzy = set(stare_analyzy.split(', ') + [a.strip() for a in nove_analyzy.split(',')])
            self.df.loc[index_na_aktualizaciu, 'Analýzy'] = ", ".join(sorted(list(vsetky_analyzy)))

        # Dokončenie
        while True:
            dokonceny_input = input("Označte záznam ako dokončený? (A/N): ").upper()
            if dokonceny_input in ['A', 'ÁNO', 'YES']:
                self.df.loc[index_na_aktualizaciu, 'Dokončené'] = 'Áno'
                print(f"✅ Záznam {index_na_aktualizaciu} bol označený ako dokončený.")
                break
            elif dokonceny_input in ['N', 'NIE', 'NO']:
                self.df.loc[index_na_aktualizaciu, 'Dokončené'] = 'Nie'
                print(f"🔄 Záznam {index_na_aktualizaciu} bol aktualizovaný, ale ostáva nedokončený.")
                break
            else:
                print("Neplatný vstup.")
        
        self.ulozit_data() # Uložíme zmeny na disk
        print(f"Aktualizovaný záznam:\n{self.df.loc[index_na_aktualizaciu]}")


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
    
    while True:
        print("\n==================================")
        print("🔬 EM Databáza Pracoviska - MENU")
        print("==================================")
        print("1. Pridať nové meranie")
        print("2. Zobraziť všetky záznamy meraní")
        print("3. Aktualizovať/dokončiť meranie")
        print("4. Filtrovať záznamy meraní")
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
            databaza.aktualizovat_zaznam()
            
        elif vyber == '4':
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

        elif vyber == '5':
            print("\nProgram bol ukončený. Dovidenia!")
            databaza.ulozit_data() # Uloženie dát pred ukončením
            break
            
        else:
            print("Neplatná voľba. Skúste to znova.")

if __name__ == "__main__":
    main()