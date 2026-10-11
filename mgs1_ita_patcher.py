#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metal Gear Solid - Traduzione MM Solid Crash v1.1
Applicatore della patch di traduzione italiana.

Due schede:
  - Master Collection (Steam, solo versione 3.0.0)
  - PlayStation (immagini USA Rev 1 per emulatore)

Non contiene dati del gioco: applica la differenza fra i file originali e
quelli tradotti. Serve una copia legittima del gioco.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import webbrowser
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

VERSION = "1.1"
APP_NAME = "Metal Gear Solid - Traduzione MM Solid Crash v" + VERSION
BLOCCO = 16 << 20
LINK_SUPPORTO = "https://www.paypal.com/donate/?hosted_button_id=ZAUN4MNN3SPS4"

# ===========================================================================
# Tabelle: Master Collection (Steam 3.0.0)
# ===========================================================================

MC_VERSIONE = "3.0.0"

# nome logico -> (percorso relativo a windata, dimensione, SHA-256)
MC_ORIGINALI = {
    "alldata.bin": ("alldata.bin", 11317041152,
                    "0accf9ba768e7917bcd7765ab7971a517cf0d4fef42059a541a9a3953b58d579"),
    "alldata.psb.m": ("alldata.psb.m", None,
                      "e703d2e0ecc2cdb6b1c6eaa15f329f945f56fe3af6eb6af54430faf2641fb568"),
    "dlc_usa.bin": ("dlc/dlc_usa.bin", 1930016768,
                    "30e3d0fcd86d2da473bc321639b47b98e4e4c3ac6e37a23e525f40df84101313"),
    "dlc_usa.psb.m": ("dlc/dlc_usa.psb.m", None,
                      "46e0ad04e9e05c9967b3153d0166713d85d913cc3bb358646aae8007d127cf9c"),
}
MC_TRADOTTI = {
    "alldata.bin": (11570341888,
                    "683bd8b0dbf50fab3094add5962b302dab0e71a9f974c81ec2dfbea6c1a0cbbb"),
    "alldata.psb.m": (None,
                      "902abb29f0aad4a831102e0c515b99c6c3262f45098aeb462c2a4fd4c52d558a"),
    "dlc_usa.bin": (1930016400,
                    "50d4ee7056c557910b0955deace91b0d5b5f553a1e35dbbfc68276580b3ca2af"),
    "dlc_usa.psb.m": (None,
                      "0fa9820a6dc41bacc49bbb10ff23f98eeee31b763f9fb473f7b90c4c3bae46b2"),
}
MC_PATCH = {
    "alldata.psb.m": "MC-alldata.psb.m.xdelta",
    "dlc_usa.bin": "MC-dlc_usa.bin.xdelta",
    "dlc_usa.psb.m": "MC-dlc_usa.psb.m.xdelta",
}
MC_CODA_PATCH = "MC-coda.xdelta"
MC_CODA_DIM = 253300736
MC_CODA_SHA = "c1b69c4dc2ff605df989cba642fba0b99bbb2f3e9791a510e3840f2dab9d4d09"
MC_ELENCO = "elenco_mc.json"
MC_SPAZIO = 3400 << 20          # margine sul disco del gioco

# ===========================================================================
# Tabelle: PlayStation
# ===========================================================================

# SHA-1 delle tracce dati dei dump redump USA
SORGENTI = {
    "37498e6598ce4eabf00630b6a9197b20861e55a0": {
        "disco": 1, "ok": True,
        "nome": "Metal Gear Solid (USA) (Disc 1) (Rev 1)",
    },
    "d6edfd60a375c10087eacebd709419950c8995ad": {
        "disco": 2, "ok": True,
        "nome": "Metal Gear Solid (USA) (Disc 2) (Rev 1)",
    },
    "848fcd22794526bfd093030c6d6ae6b632d87e4b": {
        "disco": 1, "ok": False,
        "nome": "Metal Gear Solid (USA) (Disc 1) — revisione originale (Rev 0)",
    },
    "48be04a1310cb53fb46e2d2865f39ed9be95be9b": {
        "disco": 2, "ok": False,
        "nome": "Metal Gear Solid (USA) (Disc 2) — revisione originale (Rev 0)",
    },
}

# SHA-256 delle immagini tradotte v1.1 (risultato atteso)
RISULTATI = {
    "2c6e23cce9c6c56027b43ccff80dcd860a64953c1f95391451ef40c08add2ad7": (1, 60),
    "0f394138471e4627b4e9566158a6034defc25d77c54973dc2beb3fa81b748f87": (1, 50),
    "7d2a35b387c364b04a42b283faec2a66f0c649ba993a60d7010bdef8287a6f4e": (2, 60),
    "e4231a351bddab616256d76773e696bdcee2d43bdee894427806e285a298f1c3": (2, 50),
}

# SHA-256 delle immagini tradotte con la v1.0
RISULTATI_V10 = {
    "3e60b0ffad3cee75eb838acbe693c0180083838fe45b3681052becf2adeebb89": (1, 60),
    "7935ae489d2a0a55842f9d2c82cbdf008a94d0cb1dc25080ccdc8cf1355d580c": (1, 50),
    "1b50298dce6d35227f540eb2c03ec5cdee0d58d7574cc87d834abf32eef128da": (2, 60),
    "c1bbe2372037738d8765bd23a9c37c341d3c4cead5793b116bac29d25159b130": (2, 50),
}

PATCH = {
    (1, 60): "MGS1-ITA-CD1-60Hz.xdelta",
    (1, 50): "MGS1-ITA-CD1-50Hz.xdelta",
    (2, 60): "MGS1-ITA-CD2-60Hz.xdelta",
    (2, 50): "MGS1-ITA-CD2-50Hz.xdelta",
}

NOME_USCITA = {1: "MGS1 ITA (Disc 1) by Solid Crash",
               2: "MGS1 ITA (Disc 2) by Solid Crash"}

SETTORE_RAW = 2352
SYNC = b"\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00"


# ===========================================================================
# Utilità
# ===========================================================================

class Rifiuto(Exception):
    """Situazione prevista: il messaggio è già pronto per l'utente."""


class Annullato(Exception):
    pass


def risorsa(nome: str) -> Path:
    """Percorso di un file incorporato, sia da sorgente sia da eseguibile."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base / "risorse" / nome


def suona(nome: str):
    """Riproduce un suono senza bloccare la finestra. Se fallisce, pazienza."""
    if os.name != "nt":
        return
    try:
        import winsound
        winsound.PlaySound(str(risorsa(nome)),
                           winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
    except Exception:
        pass


def senza_finestra():
    """Impedisce a subprocess di aprire una finestra nera su Windows."""
    if os.name == "nt":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return {"startupinfo": si, "creationflags": subprocess.CREATE_NO_WINDOW}
    return {}


def esegui(argomenti, descrizione, stop=None):
    """Lancia un programma interno; lo interrompe se l'utente annulla."""
    try:
        p = subprocess.Popen(
            [str(a) for a in argomenti],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            **senza_finestra()
        )
    except FileNotFoundError:
        raise RuntimeError(f"{descrizione}: componente interno non trovato.")
    while True:
        try:
            out, err = p.communicate(timeout=0.5)
            break
        except subprocess.TimeoutExpired:
            if stop is not None and stop.is_set():
                p.kill()
                p.communicate()
                raise Annullato()
    if p.returncode != 0:
        dettaglio = (err or out or "").strip()
        dettaglio = dettaglio.splitlines()[-1] if dettaglio else "errore sconosciuto"
        raise RuntimeError(f"{descrizione} non riuscito.\nDettaglio: {dettaglio}")


def hash_file(percorso: Path, algoritmi=("sha256",), avanzamento=None):
    """Legge il file una volta sola e ritorna gli oggetti hash."""
    oggetti = [hashlib.new(a) for a in algoritmi]
    totale = percorso.stat().st_size
    letti = 0
    with percorso.open("rb") as f:
        while True:
            b = f.read(BLOCCO)
            if not b:
                break
            for o in oggetti:
                o.update(b)
            letti += len(b)
            if avanzamento:
                avanzamento(letti * 100 // max(totale, 1))
    return oggetti


def sha256_di(percorso: Path, avanzamento=None) -> str:
    return hash_file(percorso, ("sha256",), avanzamento)[0].hexdigest()


def spazio_libero(cartella: Path) -> int:
    return shutil.disk_usage(str(cartella)).free


def scrivi_cue(percorso_cue: Path, nome_bin: str):
    percorso_cue.write_text(
        f'FILE "{nome_bin}" BINARY\n'
        f"  TRACK 01 MODE2/2352\n"
        f"    INDEX 01 00:00:00\n",
        encoding="utf-8",
    )


class Lavoro:
    """Base comune: messaggi, barra e annullamento."""

    def __init__(self, dire, passo, stop):
        self.dire = dire
        self.passo = passo
        self.stop = stop
        self.critico = False     # True mentre si scrive nei file del gioco

    def controlla(self):
        if self.stop.is_set():
            raise Annullato()

    def aggiorna(self, pct):
        self.controlla()
        self.passo(pct)


# ===========================================================================
# Master Collection: ricerca della cartella
# ===========================================================================

def _cartelle_steam():
    radici = []
    if os.name == "nt":
        try:
            import winreg
            for chiave, ramo, valore in (
                (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
            ):
                try:
                    with winreg.OpenKey(chiave, ramo) as k:
                        radici.append(Path(winreg.QueryValueEx(k, valore)[0]))
                except OSError:
                    pass
        except Exception:
            pass
    radici.append(Path(r"C:\Program Files (x86)\Steam"))
    librerie = []
    for r in radici:
        librerie.append(r)
        vdf = r / "steamapps" / "libraryfolders.vdf"
        try:
            testo = vdf.read_text(encoding="utf-8", errors="replace")
            for m in re.findall(r'"path"\s+"([^"]+)"', testo):
                librerie.append(Path(m.replace("\\\\", "\\")))
        except OSError:
            pass
    visti, uniche = set(), []
    for l in librerie:
        chiave = str(l).lower().rstrip("\\/")
        if chiave not in visti:
            visti.add(chiave)
            uniche.append(l)
    return uniche


def trova_master_collection():
    """Ritorna la cartella MGS1 di Steam se la trova, altrimenti None."""
    for lib in _cartelle_steam():
        cand = lib / "steamapps" / "common" / "MGS1"
        if (cand / "windata" / "alldata.bin").is_file():
            return cand
    return None


def cartella_windata(scelta: Path) -> Path:
    for c in (scelta / "windata", scelta):
        if (c / "alldata.bin").is_file() and (c / "dlc" / "dlc_usa.bin").is_file():
            return c
    raise Rifiuto(
        "In questa cartella non trovo i file della Master Collection.\n\n"
        "Seleziona la cartella del gioco, quella che contiene la sottocartella "
        "\"windata\". Di solito è:\n"
        "...\\steamapps\\common\\MGS1\n\n"
        "In Steam la trovi con: tasto destro sul gioco > Gestisci > "
        "Sfoglia i file locali."
    )


# ===========================================================================
# Master Collection: lavorazione
# ===========================================================================

class LavoroMC(Lavoro):
    def __init__(self, cartella: Path, dire, passo, stop):
        super().__init__(dire, passo, stop)
        self.cartella = cartella

    def esegui(self):
        windata = cartella_windata(self.cartella)
        self.file = {k: windata / v[0] for k, v in MC_ORIGINALI.items()}
        temp = windata / "_mgs1ita_temp"
        try:
            return self._esegui(windata, temp)
        finally:
            shutil.rmtree(temp, ignore_errors=True)

    # -- controlli ----------------------------------------------------------

    def _scrivibili(self):
        for nome, p in self.file.items():
            if not p.is_file():
                raise Rifiuto(
                    f"Manca il file {nome}.\n\n"
                    "L'installazione del gioco sembra incompleta: in Steam usa "
                    "Proprietà > File installati > Verifica integrità dei file "
                    "di gioco, poi riprova."
                )
            try:
                with p.open("r+b"):
                    pass
            except PermissionError:
                raise Rifiuto(
                    "Non riesco a modificare i file del gioco.\n\n"
                    "1. Chiudi il gioco e il suo launcher, se sono aperti.\n"
                    "2. Se il gioco è installato in \"Programmi\", chiudi questo "
                    "programma e riaprilo con tasto destro > Esegui come "
                    "amministratore."
                )

    def _classifica(self):
        """Ritorna {nome: 'orig'|'trad'|'altro'} e l'hash di alldata.bin."""
        stato = {}
        # prima le dimensioni dei file grandi: se non tornano è inutile leggere 11 GB
        for nome in ("alldata.bin", "dlc_usa.bin"):
            dim = self.file[nome].stat().st_size
            if dim not in (MC_ORIGINALI[nome][1], MC_TRADOTTI[nome][0]):
                stato[nome] = "altro"
        for nome in ("alldata.psb.m", "dlc_usa.psb.m"):
            h = sha256_di(self.file[nome])
            stato[nome] = ("orig" if h == MC_ORIGINALI[nome][2]
                           else "trad" if h == MC_TRADOTTI[nome][1] else "altro")
        if "altro" in stato.values():
            return stato, None

        self.dire("Verifico dlc_usa.bin (1 di 2)...")
        h = sha256_di(self.file["dlc_usa.bin"], self.aggiorna)
        stato["dlc_usa.bin"] = ("orig" if h == MC_ORIGINALI["dlc_usa.bin"][2]
                                else "trad" if h == MC_TRADOTTI["dlc_usa.bin"][1] else "altro")

        self.dire("Verifico alldata.bin (2 di 2), il file più grande: qualche minuto...")
        oggetto = hash_file(self.file["alldata.bin"], ("sha256",), self.aggiorna)[0]
        h = oggetto.hexdigest()
        stato["alldata.bin"] = ("orig" if h == MC_ORIGINALI["alldata.bin"][2]
                                else "trad" if h == MC_TRADOTTI["alldata.bin"][1] else "altro")
        return stato, oggetto

    # -- lavoro -------------------------------------------------------------

    def _esegui(self, windata: Path, temp: Path):
        self.dire("Controllo i file del gioco...")
        self.passo(None)
        self._scrivibili()

        stato, hash_alldata = self._classifica()
        self.controlla()
        valori = set(stato.values())

        if valori == {"trad"}:
            raise Rifiuto(
                "La traduzione è già installata e i file sono corretti.\n\n"
                "Non serve applicarla di nuovo."
            )
        if "altro" in valori:
            diversi = ", ".join(n for n, s in stato.items() if s == "altro")
            raise Rifiuto(
                f"I file del gioco non corrispondono alla versione Steam {MC_VERSIONE}.\n"
                f"File diversi: {diversi}\n\n"
                f"Questa traduzione funziona solo con la versione {MC_VERSIONE} "
                "(il numero si legge nel launcher, in basso a sinistra).\n\n"
                "- Se Steam ha aggiornato il gioco a una versione più recente, "
                "controlla se è uscito un aggiornamento della traduzione.\n"
                "- Se invece hai la versione giusta ma avevi modificato i file "
                "(altre mod, prove precedenti), in Steam usa Proprietà > File "
                "installati > Verifica integrità dei file di gioco e riprova."
            )
        if valori != {"orig"}:
            raise Rifiuto(
                "I file del gioco sono in parte originali e in parte tradotti: "
                "probabilmente un'installazione precedente si è interrotta.\n\n"
                "In Steam usa Proprietà > File installati > Verifica integrità "
                "dei file di gioco, poi riprova."
            )

        self.dire(f"Riconosciuto: Master Collection Steam {MC_VERSIONE}, file originali.")
        if spazio_libero(windata) < MC_SPAZIO:
            raise Rifiuto(
                "Spazio insufficiente sul disco dove è installato il gioco.\n\n"
                f"Servono circa {MC_SPAZIO >> 20} MB liberi."
            )

        shutil.rmtree(temp, ignore_errors=True)
        temp.mkdir()

        # 1. file originali da sostituire, letti dall'archivio dell'utente
        self.dire("Preparo i file da sostituire...")
        elenco = json.loads(risorsa(MC_ELENCO).read_text(encoding="utf-8"))["file"]
        sorgente = temp / "sorgente.bin"
        totale = sum(v["orig_size"] for v in elenco)
        fatti = 0
        with self.file["alldata.bin"].open("rb") as a, sorgente.open("wb") as s:
            for v in elenco:
                a.seek(v["orig_offset"])
                rimasti = v["orig_size"]
                while rimasti:
                    b = a.read(min(BLOCCO, rimasti))
                    if not b:
                        raise RuntimeError("alldata.bin è più corto del previsto.")
                    s.write(b)
                    rimasti -= len(b)
                    fatti += len(b)
                    self.aggiorna(fatti * 100 // totale)

        # 2. patch: tutto viene preparato e verificato a parte, senza toccare il gioco
        self.dire("Applico la traduzione (1 di 4)...")
        self.passo(None)
        coda = temp / "coda.bin"
        esegui([risorsa("xdelta3.exe"), "-d", "-f", "-s", sorgente,
                risorsa(MC_CODA_PATCH), coda], "Applicazione della patch", self.stop)
        if coda.stat().st_size != MC_CODA_DIM or sha256_di(coda) != MC_CODA_SHA:
            raise RuntimeError(self._msg_verifica())
        sorgente.unlink()

        nuovi = {}
        for i, nome in enumerate(("alldata.psb.m", "dlc_usa.bin", "dlc_usa.psb.m"), 2):
            self.dire(f"Applico la traduzione ({i} di 4)...")
            self.passo(None)
            uscita = temp / (nome + ".nuovo")
            esegui([risorsa("xdelta3.exe"), "-d", "-f", "-s", self.file[nome],
                    risorsa(MC_PATCH[nome]), uscita], "Applicazione della patch", self.stop)
            self.dire(f"Verifico il risultato ({i} di 4)...")
            if sha256_di(uscita, self.aggiorna) != MC_TRADOTTI[nome][1]:
                raise RuntimeError(self._msg_verifica())
            nuovi[nome] = uscita
        self.controlla()

        # 3. installazione: da qui in poi non si annulla più
        self.critico = True
        self.dire("Installo i file tradotti, non chiudere il programma...")
        self.passo(None)
        alldata = self.file["alldata.bin"]
        dim_orig = MC_ORIGINALI["alldata.bin"][1]
        try:
            with alldata.open("r+b") as f, coda.open("rb") as c:
                f.seek(dim_orig)
                while True:
                    b = c.read(BLOCCO)
                    if not b:
                        break
                    f.write(b)
                f.truncate()
                f.flush()
                os.fsync(f.fileno())
            # rilettura della parte aggiunta: deve coincidere con la coda verificata
            h = hashlib.sha256()
            completo = hash_alldata.copy()
            with alldata.open("rb") as f:
                f.seek(dim_orig)
                while True:
                    b = f.read(BLOCCO)
                    if not b:
                        break
                    h.update(b)
                    completo.update(b)
            if (alldata.stat().st_size != MC_TRADOTTI["alldata.bin"][0]
                    or h.hexdigest() != MC_CODA_SHA
                    or completo.hexdigest() != MC_TRADOTTI["alldata.bin"][1]):
                raise RuntimeError(self._msg_verifica())
        except Exception:
            # rimetto alldata.bin com'era: la parte originale non è mai stata toccata
            try:
                with alldata.open("r+b") as f:
                    f.truncate(dim_orig)
            except Exception:
                pass
            raise

        os.replace(nuovi["alldata.psb.m"], self.file["alldata.psb.m"])
        os.replace(nuovi["dlc_usa.bin"], self.file["dlc_usa.bin"])
        os.replace(nuovi["dlc_usa.psb.m"], self.file["dlc_usa.psb.m"])
        self.critico = False
        self.passo(100)
        return windata

    @staticmethod
    def _msg_verifica():
        return ("Il risultato non corrisponde a quello atteso.\n\n"
                "Può succedere se il disco si è riempito o se un antivirus è "
                "intervenuto durante la scrittura. I file del gioco non sono stati "
                "modificati: riprova. Se l'errore si ripete, segnalalo.")


# ===========================================================================
# PlayStation: riconoscimento del formato
# ===========================================================================

def bin_da_cue(percorso_cue: Path) -> Path:
    testo = percorso_cue.read_text(encoding="utf-8", errors="replace")
    file_dichiarati = re.findall(r'^\s*FILE\s+"([^"]+)"', testo, re.MULTILINE | re.IGNORECASE)
    if not file_dichiarati:
        file_dichiarati = re.findall(r"^\s*FILE\s+(\S+)", testo, re.MULTILINE | re.IGNORECASE)
    if not file_dichiarati:
        raise Rifiuto("Il file .cue non indica nessuna immagine.")
    if len(file_dichiarati) > 1:
        raise Rifiuto(
            "Questo .cue fa riferimento a più file.\n\n"
            "Metal Gear Solid ha una sola traccia dati: l'immagine non è quella giusta."
        )
    candidato = percorso_cue.parent / file_dichiarati[0]
    if not candidato.exists():
        raise Rifiuto(
            f"Il .cue punta a \"{file_dichiarati[0]}\", che non si trova "
            f"nella stessa cartella."
        )
    return candidato


def classifica(percorso: Path) -> str:
    """Ritorna: 'raw', 'chd', oppure solleva Rifiuto con la spiegazione."""
    with percorso.open("rb") as f:
        testa = f.read(16)

    if testa[:8] == b"MComprHD":
        return "chd"
    if testa[:4] == b"\x00PBP":
        raise Rifiuto(
            "Questo è un file .pbp (formato PSP / PlayStation Classic).\n\n"
            "Va prima riconvertito in .bin + .cue, per esempio con PSX2PSP "
            "in modalità inversa o con PopstationMD."
        )
    if testa[:4] == b"ECM\x00":
        raise Rifiuto(
            "Questo è un file .ecm (immagine compressa).\n\n"
            "Va prima decompresso con unecm, ottenendo il .bin."
        )
    if testa[:2] == b"PK" or testa[:6] == b"7z\xbc\xaf\x27\x1c" or testa[:5] == b"Rar!\x1a":
        raise Rifiuto(
            "Questo è un archivio compresso.\n\n"
            "Estrai prima il contenuto, poi seleziona il file .bin o .cue."
        )
    if testa[:12] == SYNC:
        return "raw"

    raise Rifiuto(
        "Questa immagine non contiene i settori grezzi del CD.\n\n"
        "Sembra un .iso da 2048 byte per settore: un formato in cui i filmati "
        "e l'audio di Metal Gear Solid sono già andati persi durante la "
        "creazione del file. Non è possibile applicarci la traduzione, e il "
        "gioco stesso non funzionerebbe correttamente.\n\n"
        "Serve un'immagine .bin + .cue oppure .chd."
    )


# ===========================================================================
# PlayStation: lavorazione
# ===========================================================================

class LavoroPSX(Lavoro):
    def __init__(self, ingresso: Path, hz: int, cartella_uscita: Path,
                 ricrea_chd: bool, dire, passo, stop):
        super().__init__(dire, passo, stop)
        self.ingresso = ingresso
        self.hz = hz
        self.cartella_uscita = cartella_uscita
        self.ricrea_chd = ricrea_chd

    def esegui(self):
        temporanea = Path(tempfile.mkdtemp(prefix="mgs1ita_"))
        try:
            return self._esegui(temporanea)
        finally:
            shutil.rmtree(temporanea, ignore_errors=True)

    def _impronte(self, percorso):
        sha1, sha256 = hash_file(percorso, ("sha1", "sha256"), self.aggiorna)
        self.passo(100)
        return sha1.hexdigest(), sha256.hexdigest()

    def _esegui(self, temporanea: Path):
        self.dire("Esamino il file...")
        self.passo(None)

        sorgente = self.ingresso
        if sorgente.suffix.lower() == ".cue":
            sorgente = bin_da_cue(sorgente)
            self.dire(f"Il .cue punta a: {sorgente.name}")

        tipo = classifica(sorgente)
        self.controlla()

        if tipo == "chd":
            necessario = sorgente.stat().st_size * 4 + (2 << 30)
            if spazio_libero(temporanea) < necessario:
                raise Rifiuto(
                    "Spazio su disco insufficiente per decomprimere il .chd.\n\n"
                    "Servono circa 3 GB liberi sul disco di sistema."
                )
            self.dire("Decomprimo il file .chd, può richiedere qualche minuto...")
            estratto_cue = temporanea / "estratto.cue"
            estratto_bin = temporanea / "estratto.bin"
            esegui(
                [risorsa("chdman.exe"), "extractcd", "-i", sorgente,
                 "-o", estratto_cue, "-ob", estratto_bin, "-f"],
                "Decompressione del file .chd", self.stop,
            )
            sorgente = estratto_bin
            self.controlla()
            if classifica(sorgente) != "raw":
                raise Rifiuto("Il contenuto del .chd non è un'immagine CD valida.")

        dimensione = sorgente.stat().st_size
        if dimensione % SETTORE_RAW != 0:
            raise Rifiuto(
                "L'immagine è incompleta o danneggiata: la sua dimensione non "
                "corrisponde a un numero intero di settori."
            )

        self.dire("Verifico l'immagine (calcolo l'impronta digitale)...")
        sha1, sha256 = self._impronte(sorgente)
        self.controlla()

        if sha256 in RISULTATI:
            disco, hz = RISULTATI[sha256]
            raise Rifiuto(
                f"Questa immagine è già tradotta con la versione {VERSION}: "
                f"è il disco {disco} nella versione {hz} Hz.\n\n"
                "Non serve applicare di nuovo la patch."
            )
        if sha256 in RISULTATI_V10:
            disco, hz = RISULTATI_V10[sha256]
            raise Rifiuto(
                f"Questa immagine è già tradotta con la versione precedente (1.0): "
                f"è il disco {disco} nella versione {hz} Hz.\n\n"
                f"Per passare alla versione {VERSION} parti dall'immagine originale "
                "americana (USA) Rev 1, non da quella già tradotta."
            )

        voce = SORGENTI.get(sha1)
        if voce is None:
            raise Rifiuto(
                "Immagine non riconosciuta.\n\n"
                "La traduzione si applica ai dump verificati della versione "
                "americana (USA), revisione 1 — le edizioni Original, Greatest "
                "Hits e The Essential Collection.\n\n"
                "Se hai un'immagine creata da te, potrebbe essere stata estratta "
                "in modo non conforme oppure già modificata."
            )
        if not voce["ok"]:
            raise Rifiuto(
                f"Questa è la {voce['nome']}.\n\n"
                "La traduzione è costruita sulla revisione 1, che è quella "
                "delle edizioni Original, Greatest Hits e The Essential "
                "Collection. Su questa revisione non può essere applicata."
            )

        disco = voce["disco"]
        self.dire(f"Riconosciuto: {voce['nome']}")
        self.controlla()

        nome_base = NOME_USCITA[disco]
        uscita_bin = self.cartella_uscita / f"{nome_base}.bin"
        uscita_cue = self.cartella_uscita / f"{nome_base}.cue"

        margine = dimensione + (256 << 20)
        if self.ricrea_chd:
            margine += dimensione
        if spazio_libero(self.cartella_uscita) < margine:
            raise Rifiuto(
                "Spazio insufficiente nella cartella di destinazione.\n\n"
                f"Servono almeno {margine // (1024*1024)} MB liberi."
            )

        self.dire(f"Applico la traduzione (disco {disco}, {self.hz} Hz)...")
        self.passo(None)
        provvisorio = temporanea / "risultato.bin"
        esegui(
            [risorsa("xdelta3.exe"), "-d", "-f",
             "-s", sorgente, risorsa(PATCH[(disco, self.hz)]), provvisorio],
            "Applicazione della patch", self.stop,
        )
        self.controlla()

        self.dire("Verifico il risultato...")
        _, sha256_finale = self._impronte(provvisorio)
        atteso = next(h for h, v in RISULTATI.items() if v == (disco, self.hz))
        if sha256_finale != atteso:
            raise RuntimeError(
                "Il file prodotto non corrisponde a quello atteso.\n\n"
                "Può succedere se il disco era pieno o se un antivirus è "
                "intervenuto durante la scrittura. Riprova; se l'errore si "
                "ripete, segnalalo."
            )
        self.controlla()

        self.dire("Salvo il risultato...")
        self.passo(None)

        if self.ricrea_chd:
            cue_provvisorio = temporanea / "risultato.cue"
            scrivi_cue(cue_provvisorio, provvisorio.name)
            uscita_chd = self.cartella_uscita / f"{nome_base}.chd"
            self.dire("Ricomprimo in .chd, può richiedere diversi minuti...")
            esegui(
                [risorsa("chdman.exe"), "createcd", "-i", cue_provvisorio,
                 "-o", uscita_chd, "-f"],
                "Creazione del file .chd", self.stop,
            )
            return [uscita_chd]

        shutil.move(str(provvisorio), str(uscita_bin))
        scrivi_cue(uscita_cue, uscita_bin.name)
        return [uscita_bin, uscita_cue]


# ===========================================================================
# Interfaccia
# ===========================================================================

class Finestra(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.resizable(False, False)
        try:
            self.iconbitmap(default=str(risorsa("icona.ico")))
        except Exception:
            pass
        self.stop = threading.Event()
        self.in_corso = False
        self.lavoro = None
        self._costruisci()
        self._argomento_iniziale()
        self.after(150, lambda: suona("suono_avvio.wav"))

    # -- costruzione ---------------------------------------------------------

    def _costruisci(self):
        cornice = ttk.Frame(self, padding=16)
        cornice.grid(sticky="nsew")
        cornice.columnconfigure(0, weight=1)

        testa = ttk.Frame(cornice)
        testa.grid(row=0, column=0, sticky="we")
        testa.columnconfigure(0, weight=1)
        ttk.Label(testa, text="Metal Gear Solid ENG/ITA",
                  font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(testa, justify="left", text=(
            "Voci inglesi originali, testo in italiano.\n"
            "Scegli la versione del gioco che possiedi.")).grid(
            row=1, column=0, sticky="nw", pady=(4, 0))
        self._ritratto(testa)

        self.schede = ttk.Notebook(cornice)
        self.schede.grid(row=1, column=0, sticky="we", pady=(12, 0))
        self.scheda_mc = ttk.Frame(self.schede, padding=12)
        self.scheda_psx = ttk.Frame(self.schede, padding=12)
        self.schede.add(self.scheda_mc, text="  Master Collection (Steam)  ")
        self.schede.add(self.scheda_psx, text="  PlayStation (ROM)  ")
        self._costruisci_mc(self.scheda_mc)
        self._costruisci_psx(self.scheda_psx)

        self.barra = ttk.Progressbar(cornice, length=480, mode="determinate")
        self.barra.grid(row=2, column=0, sticky="we", pady=(16, 4))
        self.var_stato = tk.StringVar(value="Pronto.")
        ttk.Label(cornice, textvariable=self.var_stato, foreground="#444",
                  wraplength=480, justify="left").grid(row=3, column=0, sticky="w")

        self.bottone = ttk.Button(cornice, text="Applica la traduzione", command=self._avvia)
        self.bottone.grid(row=4, column=0, sticky="we", pady=(16, 0))

        piede = ttk.Frame(cornice)
        piede.grid(row=5, column=0, sticky="we", pady=(14, 0))
        piede.columnconfigure(0, weight=1)
        ttk.Label(
            piede,
            text=("Traduzione di Mattia Moro (solidcrash) — v" + VERSION +
                  "\nQuesto programma non contiene dati del gioco. "
                  "Serve una copia legittima di Metal Gear Solid."),
            foreground="#777", justify="left", font=("Segoe UI", 8),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(piede, text="Supportami", command=self._supporta).grid(
            row=0, column=1, sticky="e", padx=(8, 0))

        self.protocol("WM_DELETE_WINDOW", self._chiudi)

    def _costruisci_mc(self, f):
        ttk.Label(f, justify="left", text=(
            f"Per METAL GEAR SOLID - Master Collection Version su Steam,\n"
            f"solo versione {MC_VERSIONE} (si legge nel launcher, in basso a sinistra).\n"
            "La traduzione viene installata direttamente nella cartella del gioco.")).grid(
            row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(f, text="Cartella del gioco:").grid(row=1, column=0, sticky="w", pady=(12, 0))
        self.var_mc = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_mc, width=56).grid(
            row=2, column=0, sticky="we", pady=(2, 0))
        ttk.Button(f, text="Sfoglia...", command=self._scegli_mc).grid(
            row=2, column=1, sticky="we", padx=(8, 0), pady=(2, 0))
        self.var_mc_nota = tk.StringVar()
        ttk.Label(f, textvariable=self.var_mc_nota, foreground="#555").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))

        ttk.Label(f, justify="left", foreground="#555", text=(
            "Per tornare alla versione originale: in Steam, tasto destro sul gioco >\n"
            "Proprietà > File installati > Verifica integrità dei file di gioco.")).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))

        trovata = trova_master_collection()
        if trovata:
            self.var_mc.set(str(trovata))
            self.var_mc_nota.set("Cartella trovata automaticamente.")
        else:
            self.var_mc_nota.set("Cartella non trovata automaticamente: selezionala con Sfoglia.")

    def _costruisci_psx(self, f):
        ttk.Label(f, justify="left", text=(
            "Per la tua copia PlayStation in versione americana (USA) Rev. 1.\n"
            "Il file originale non viene modificato: ne viene creata una copia tradotta.")).grid(
            row=0, column=0, columnspan=2, sticky="w")

        ttk.Label(f, text="Immagine del disco:").grid(row=1, column=0, sticky="w", pady=(12, 0))
        self.var_file = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_file, width=56).grid(
            row=2, column=0, sticky="we", pady=(2, 0))
        ttk.Button(f, text="Sfoglia...", command=self._scegli_file).grid(
            row=2, column=1, sticky="we", padx=(8, 0), pady=(2, 0))

        ttk.Label(f, text="Cartella di destinazione:").grid(row=3, column=0, sticky="w", pady=(12, 0))
        self.var_uscita = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_uscita, width=56).grid(
            row=4, column=0, sticky="we", pady=(2, 0))
        ttk.Button(f, text="Sfoglia...", command=self._scegli_uscita).grid(
            row=4, column=1, sticky="we", padx=(8, 0), pady=(2, 0))

        gruppo = ttk.LabelFrame(f, text="Frequenza dei sottotitoli nei filmati", padding=10)
        gruppo.grid(row=5, column=0, columnspan=2, sticky="we", pady=(14, 0))
        self.var_hz = tk.IntVar(value=60)
        ttk.Radiobutton(gruppo, text="60 Hz — NTSC",
                        variable=self.var_hz, value=60).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(gruppo, text="50 Hz — PAL",
                        variable=self.var_hz, value=50).grid(row=1, column=0, sticky="w")

        self.var_chd = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text="Salva il risultato come .chd invece di .bin + .cue",
                        variable=self.var_chd).grid(row=6, column=0, columnspan=2,
                                                    sticky="w", pady=(10, 0))

    def _ritratto(self, testa):
        try:
            self.immagine_ritratto = tk.PhotoImage(file=str(risorsa("ritratto.png")))
        except Exception:
            return
        bordo = tk.Frame(testa, background="#3a3a3a")
        bordo.grid(row=0, column=1, rowspan=2, sticky="ne", padx=(8, 0))
        tk.Label(bordo, image=self.immagine_ritratto, borderwidth=0,
                 highlightthickness=0).pack(padx=1, pady=1)

    def _argomento_iniziale(self):
        """File o cartella trascinati sull'icona del programma."""
        if len(sys.argv) < 2:
            return
        p = Path(sys.argv[1])
        if p.is_dir():
            self.var_mc.set(str(p))
            self.var_mc_nota.set("")
            self.schede.select(self.scheda_mc)
        elif p.is_file():
            self.var_file.set(str(p))
            self._aggiorna_chd()
            self.schede.select(self.scheda_psx)

    # -- eventi --------------------------------------------------------------

    def _scegli_mc(self):
        scelto = filedialog.askdirectory(title="Seleziona la cartella MGS1 del gioco")
        if scelto:
            self.var_mc.set(scelto)
            self.var_mc_nota.set("")

    def _scegli_file(self):
        scelto = filedialog.askopenfilename(
            title="Seleziona l'immagine del disco",
            filetypes=[
                ("Immagini PlayStation", "*.cue *.bin *.chd *.img *.mdf *.iso"),
                ("Tutti i file", "*.*"),
            ],
        )
        if scelto:
            self.var_file.set(scelto)
            self._aggiorna_chd()

    def _scegli_uscita(self):
        scelto = filedialog.askdirectory(title="Dove salvare il gioco tradotto")
        if scelto:
            self.var_uscita.set(scelto)

    def _aggiorna_chd(self):
        percorso = self.var_file.get().strip()
        if percorso.lower().endswith(".chd"):
            self.var_chd.set(True)
        if not self.var_uscita.get() and percorso:
            self.var_uscita.set(str(Path(percorso).parent))

    def _supporta(self):
        try:
            webbrowser.open(LINK_SUPPORTO)
        except Exception:
            messagebox.showinfo(APP_NAME, "Puoi supportarmi da questo indirizzo:\n\n" + LINK_SUPPORTO)

    def _chiudi(self):
        if self.in_corso and self.lavoro is not None and self.lavoro.critico:
            messagebox.showinfo(
                APP_NAME, "Sto scrivendo i file del gioco: attendi la fine, "
                "manca poco. Chiudere adesso danneggerebbe l'installazione.")
            return
        if self.in_corso:
            if not messagebox.askyesno(
                    APP_NAME, "Operazione in corso. Vuoi annullarla e uscire?"):
                return
            self.stop.set()
            # lascio il tempo di fermare i programmi interni e pulire i temporanei
            self.after(1500, self.destroy)
            return
        self.destroy()

    # -- esecuzione ----------------------------------------------------------

    def _avvia(self):
        if self.in_corso:
            return
        mc = self.schede.index(self.schede.select()) == 0

        if mc:
            cartella = self.var_mc.get().strip().strip('"')
            if not cartella or not Path(cartella).is_dir():
                messagebox.showwarning(APP_NAME, "Seleziona la cartella del gioco.")
                return
            lavoro = LavoroMC(Path(cartella), self._dire, self._passo, self.stop)
        else:
            percorso = self.var_file.get().strip().strip('"')
            uscita = self.var_uscita.get().strip().strip('"')
            if not percorso or not Path(percorso).is_file():
                messagebox.showwarning(APP_NAME, "Seleziona l'immagine del disco.")
                return
            if not uscita or not Path(uscita).is_dir():
                messagebox.showwarning(APP_NAME, "Seleziona una cartella di destinazione valida.")
                return
            lavoro = LavoroPSX(Path(percorso), self.var_hz.get(), Path(uscita),
                               self.var_chd.get(), self._dire, self._passo, self.stop)

        self.lavoro = lavoro
        self.in_corso = True
        self.stop.clear()
        self.bottone.configure(state="disabled")
        for i in range(2):
            self.schede.tab(i, state="disabled")
        self.barra.configure(mode="determinate", value=0)
        threading.Thread(target=self._lavora, args=(lavoro, mc), daemon=True).start()

    def _lavora(self, lavoro, mc):
        try:
            risultato = lavoro.esegui()
            self.after(0, self._finito, risultato, mc)
        except Annullato:
            self.after(0, self._concluso, "Operazione annullata.")
        except Rifiuto as e:
            self.after(0, self._problema, str(e), "Non posso procedere")
        except RuntimeError as e:
            self.after(0, self._problema, str(e), "Errore")
        except PermissionError:
            self.after(0, self._problema,
                       "Accesso negato a un file.\n\nChiudi il gioco e il launcher, "
                       "poi riprova. Se il problema resta, riapri questo programma "
                       "con tasto destro > Esegui come amministratore.", "Errore")
        except Exception:
            self.after(0, self._problema,
                       "Errore imprevisto:\n\n" + traceback.format_exc(limit=3), "Errore")

    def _dire(self, testo):
        self.after(0, self.var_stato.set, testo)

    def _passo(self, percentuale):
        def applica():
            if percentuale is None:
                self.barra.configure(mode="indeterminate")
                self.barra.start(12)
            else:
                self.barra.stop()
                self.barra.configure(mode="determinate", value=percentuale)
        self.after(0, applica)

    def _finito(self, risultato, mc):
        self._concluso("Fatto.")
        suona("suono_riuscita.wav")
        if mc:
            messagebox.showinfo(
                APP_NAME,
                "Traduzione installata correttamente.\n\n"
                "Tutti i file sono stati verificati.\n\n"
                "Avvia il gioco da Steam e nel launcher scegli:\n"
                "  - gioco: Metal Gear Solid\n"
                "    (non Special Missions, VR Missions o Integral)\n"
                "  - versione: Inglese (US)\n\n"
                "Se Steam aggiorna il gioco, la traduzione viene sovrascritta: "
                "servirà la versione della traduzione adatta al nuovo aggiornamento.\n\n"
                "Se il progetto ti è piaciuto, puoi supportarmi con il pulsante "
                "\"Supportami\" in basso. Grazie!",
            )
        else:
            elenco = "\n".join("  " + p.name for p in risultato)
            messagebox.showinfo(
                APP_NAME,
                "Traduzione applicata correttamente.\n\n"
                f"File creati in {risultato[0].parent}:\n{elenco}\n\n"
                "Il risultato è stato verificato ed è corretto.\n\n"
                "Se il progetto ti è piaciuto, puoi supportarmi con il pulsante "
                "\"Supportami\" in basso. Grazie!",
            )

    def _problema(self, testo, titolo):
        self._concluso("Pronto.")
        suona("suono_errore.wav")
        messagebox.showerror(f"{APP_NAME} — {titolo}", testo)

    def _concluso(self, stato):
        self.in_corso = False
        self.barra.stop()
        self.barra.configure(mode="determinate", value=0)
        self.bottone.configure(state="normal")
        for i in range(2):
            self.schede.tab(i, state="normal")
        self.var_stato.set(stato)


if __name__ == "__main__":
    Finestra().mainloop()
