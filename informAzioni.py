from types import NoneType

import yfinance as yf
import finplot as fplt
import os, sys
from datetime import datetime


# Funzione per mostrare il logo in ASCII art
def mostra_logo():
    """
    Stampa il logo del programma in ASCII art.
    """
    logo = r"""
   _____ _   _ ______ ____  _____  __  __                   
 |_   _| \ | |  ____/ __ \|  __ \|  \/  |                  
   | | |  \| | |__ | |  | | |__) | \  / |                  
   | | | . ` |  __|| |  | |  _  /| |\/| |                  
  _| |_| |\  | |   | |__| | | \ \| |  | |                  
 |_____|_| \_|_|    \____/|_|__\_\_|__|_|____  _   _ _____ 
                      /\    |___  /_   _/ __ \| \ | |_   _|
                     /  \      / /  | || |  | |  \| | | |  
                    / /\ \    / /   | || |  | | . ` | | |  
                   / ____ \  / /__ _| || |__| | |\  |_| |_ 
                  /_/    \_\/_____|_____\____/|_| \_|_____|
                                                                        
    """
    print(logo)

# Funzione per pulire lo schermo
def pulisci_schermo():
    """
    Pulisce lo schermo del terminale.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Funzione per riavviare lo script
def restart_program():
    """
    Riavvia l'intero script.
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Funzione per visualizzare il grafico a candela
def plot_candlestick(df):
    """
    Visualizza un grafico a candela per i dati forniti.

    Args:
        df (pandas.DataFrame): DataFrame contenente i dati di borsa.
    """
    if df.empty:
        print("Nessun dato disponibile per il periodo selezionato.")
        return
    fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
    fplt.show()

# Funzione per visualizzare il menu
def visualizza_menu(titolo_azionario, nome_azienda):
    """
    Visualizza un menu per selezionare i dati da visualizzare per una specifica azienda.

    Args:
        titolo_azionario (str): Il simbolo dell'azione dell'azienda.
        nome_azienda (str): Il nome dell'azienda.
    """
    while True:
        print("\nQuali dati vuoi visualizzare per l'azienda \033[1m" + format(nome_azienda) + "\033[0m (" + format(
            titolo_azionario).upper() + ")?")
        print("1. Dettagli azienda")
        print("2. Prezzo attuale")
        print("3. Dettagli ultimi 5 giorni")
        print("4. Dettagli ultima giornata")
        print("5. Valore massimo mai raggiunto")
        print("6. Dividendi")
        print("7. Split")
        print("8. Quote Azionarie Dirigenti")
        print("9. Dati Analisti")
        print("10. Grafici")
        print("11. News")
        print("12. Cambia azienda")
        print("13. Esci")

        scelta = input("\nScelta: ")

        if scelta == "13":
            print("Arrivederci!")
            break
        elif scelta == "1":
            pulisci_schermo()
            print("\033[1mDESCRIZIONE AZIENDA\033[0m\n")
            print("\033[1mNome azienda: \033[0m" + nome_azienda)
            print("\033[1mSettore: \033[0m" + str(yf.Ticker(titolo_azionario).info.get('industry', 'N/A')))
            print(
                "\033[1mIndirizzo: \033[0m" + str(yf.Ticker(titolo_azionario).info.get('address1', 'N/A')) + ", " + str(
                    yf.Ticker(titolo_azionario).info.get('city', 'N/A')) + " (" + str(
                    yf.Ticker(titolo_azionario).info.get('state', 'N/A')).upper() + "), " + str(
                    yf.Ticker(titolo_azionario).info.get('country', 'N/A')))
            print("\033[1mSito Web: \033[0m" + str(yf.Ticker(titolo_azionario).info.get('website', 'N/A')))
        elif scelta == "2":
            pulisci_schermo()
            print("\033[1mPREZZO ATTUALE: \033[0m" + str(
                yf.Ticker(titolo_azionario).info.get('currentPrice', 'N/A')) + " USD")
        elif scelta == "3":
            pulisci_schermo()
            print("\033[1mDETTAGLI ULTIMI 5 GIORNI\033[0m")
            recent_data = yf.download(titolo_azionario, period="5d", progress=False)
            print(recent_data)
        elif scelta == "4":
            pulisci_schermo()
            print("\033[1mDETTAGLI ULTIMA GIORNATA\033[0m")
            dati = yf.download(titolo_azionario, period="1d", progress=False)
            print(dati)
        elif scelta == "5":
            pulisci_schermo()
            print("\033[1mVALORE MASSIMO MAI RAGGIUNTO\033[0m")

            end_date = datetime.now().strftime('%Y-%m-%d')
            data = yf.download(titolo_azionario, start='2000-01-01', end=end_date, progress=False)

            # Trova il valore massimo del prezzo massimo giornaliero (High)
            max_high = data['High'].max()

            # Trova la data in cui è stato raggiunto il valore massimo giornaliero
            max_high_date = data['High'].idxmax().strftime('%d-%m-%Y')

            print(
                f"Il prezzo massimo mai raggiunto da \033[1m{titolo_azionario.upper()}\033[0m è stato \033[1m{round(max_high, 2)} USD\033[0m il giorno \033[1m{max_high_date}\033[0m")
        elif scelta == "6":
            pulisci_schermo()
            print("\033[1mDIVIDENDI\033[0m\n")
            print(yf.Ticker(titolo_azionario).dividends)
        elif scelta == "7":
            pulisci_schermo()
            print("\033[1mSPLIT\033[0m\n")
            print(yf.Ticker(titolo_azionario).splits)
        elif scelta == "8":
            pulisci_schermo()
            print("\033[1mQUOTE AZIONARIE DIRIGENTI\033[0m\n")
            insider_roster = yf.Ticker(titolo_azionario).insider_roster_holders
            if insider_roster is not None:
                print(insider_roster[['Name', 'Position', 'Shares Owned Directly', 'Shares Owned Indirectly']])
            else:
                print("Nessuna informazione disponibile sui dirigenti.")
        elif scelta == "9":
            pulisci_schermo()
            print("\033[1mDATI ANALISTI\033[0m\n")
            print("\033[1mTARGET DI PREZZO \033[0m")
            analyst_data = yf.Ticker(titolo_azionario).analyst_price_targets
            if analyst_data is not None:
                print("\033[1mValore Attuale: \033[0m" + str(analyst_data.get('current', 'N/A')) + " USD")
                print("\033[1mPrezzo Obiettivo Alto: \033[0m" + str(analyst_data.get('high', 'N/A')) + " USD")
                print("\033[1mPrezzo Obiettivo Medio: \033[0m" + str(analyst_data.get('mean', 'N/A')) + " USD")
                print("\033[1mPrezzo Obiettivo Basso: \033[0m" + str(analyst_data.get('low', 'N/A')) + " USD")
            else:
                print("Nessuna informazione disponibile sugli analisti.")
            print("\n\033[1mCHI CONSIGLIA DI ACQUISTARE? \033[0m")
            print(yf.Ticker(titolo_azionario).upgrades_downgrades.head(10))
        elif scelta == "10":
            pulisci_schermo()
            print("\033[1mGRAFICI\033[0m\n")
            print("1. Grafico Prezzi ultime 24 ore")
            print("2. Grafico Prezzi ultimi 5 giorni")
            print("3. Grafico Prezzi ultimi 3 mesi")
            print("4. Grafico Prezzi ultimi 6 mesi")
            print("5. Grafico Prezzi ultimi 1 anno")
            print("6. Grafico Prezzi ultimi 5 anni")
            print("7. Torna al menu principale")

            while True:
                scelta_grafico = input("\nScelta grafico: ")
                if scelta_grafico == "1":
                    df = yf.Ticker(titolo_azionario).history(interval='1h', period='1d')
                    plot_candlestick(df)
                elif scelta_grafico == "2":
                    df = yf.Ticker(titolo_azionario).history(interval='1d', period='5d')
                    plot_candlestick(df)
                elif scelta_grafico == "3":
                    df = yf.Ticker(titolo_azionario).history(interval='1d', period='3mo')
                    plot_candlestick(df)
                elif scelta_grafico == "4":
                    df = yf.Ticker(titolo_azionario).history(interval='1d', period='6mo')
                    plot_candlestick(df)
                elif scelta_grafico == "5":
                    df = yf.Ticker(titolo_azionario).history(interval='1d', period='1y')
                    plot_candlestick(df)
                elif scelta_grafico == "6":
                    df = yf.Ticker(titolo_azionario).history(interval='1d', period='5y')
                    plot_candlestick(df)
                elif scelta_grafico == "7":
                    break  # Esci dal loop dei grafici e torna al menu principale
                else:
                    print("Scelta non valida")
        elif scelta == "11":
            pulisci_schermo()
            print(f"\033[1mNEWS su {nome_azienda}\033[0m")
            news = yf.Ticker(titolo_azionario).news
            for i in range(min(len(news), 5)):  # Stampa solo i primi 5 articoli disponibili
                print("\n\033[1mTitolo: \033[0m" + news[i]['title'])
                print("\033[1mPublisher: \033[0m" + news[i]['publisher'])
                print("\033[1mLink: \033[0m" + news[i]['link'])
        elif scelta == "12":
            restart_program()
        else:
            print("Scelta non valida")

# Funzione principale
def main():
    """
    Funzione principale che avvia il programma. Richiede all'utente di inserire il titolo dell'azione e visualizza il menu.
    """
    try:
        pulisci_schermo()
        mostra_logo()
        print("\n\033[1mBENVENUTO/A IN INFORM-AZIONI\033[0m")
        print("Questo programma ti permette di visualizzare informazioni dettagliate su un'azienda quotata in borsa.")
        print("\033[3mDati forniti da Yahoo Finance\033[0m\n")
        while True:
            titolo_azionario = input("Inserisci il titolo dell'azione: ")
            try:
                ticker = yf.Ticker(titolo_azionario)
                nome_azienda = ticker.info.get('longName')

                if nome_azienda is None:
                    print("Il titolo inserito non esiste. Riprova.")
                    restart_program()
                else:
                    pulisci_schermo()
                    mostra_logo()
                    nome_azienda = nome_azienda.upper()
                    print("\nAzienda: \033[1m{}\033[0m".format(nome_azienda))
                    visualizza_menu(titolo_azionario, nome_azienda)
                    break  # Esci dal ciclo se il titolo è valido

            except Exception as e:
                print(f"Si è verificato un errore: {e}")
                print("Riprova inserendo un titolo valido.")
                restart_program()

    except KeyboardInterrupt:
        print("\n\nProgramma interrotto dall'utente.")
        print("Chiusura in corso...")

if __name__ == '__main__':
    main()