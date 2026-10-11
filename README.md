# Metal Gear Solid ENG/ITA

**Traduzione italiana su audio inglese — v1.1**
di Mattia Moro (solidcrash)

**Download ufficiale:** https://github.com/solidcrash/MGS1-ENG-ITA/releases

**Copia di riserva (Google Drive):** https://drive.google.com/file/d/1Yl5EwAn5Y1c1h_wzGx8Z_Z6inVUq5o7F/view?usp=sharing

**Video di presentazione:** https://youtu.be/P3YFF5PDRuE

---

## Che cos'è

Metal Gear Solid è uscito in Italia solo con il doppiaggio italiano. Chi voleva
sentire le voci originali inglesi doveva rinunciare ai sottotitoli nella propria
lingua.

Questa mod mette il testo italiano sulla versione americana del gioco: **voci
inglesi originali, tutto il testo in italiano**. Sottotitoli dei filmati,
chiamate Codec, briefing, VR Training, Mission Log, descrizioni di armi e
oggetti, scritte a schermo, titoli di testa e di coda.

Il testo italiano è quello ufficiale dell'edizione PAL, ridistribuito battuta
per battuta sui tempi dell'audio inglese — che sono diversi, perché l'edizione
italiana era doppiata. Dove il PAL sbagliava accenti o grammatica, è stato
corretto.

Inoltre è stato fatto un lavoro di adattamento aggiuntivo, per correggere
e migliorare le lacune della traduzione originale.

È disponibile per due versioni del gioco:

- **METAL GEAR SOLID – Master Collection Version** su Steam
- **PlayStation** ROM USA REV 1

La mod non contiene alcun dato del gioco. Senza la tua copia non funziona
niente.

---

## Novità della versione 1.1

- Nuova scheda per la **Master Collection** su Steam.
- Nuove correzioni al testo, anche per la versione PlayStation.

Le immagini PlayStation tradotte con la v1.0 non si aggiornano: rifai la
procedura partendo dall'immagine originale americana.

---

## Master Collection (Steam)

### Che cosa ti serve

Il gioco installato da Steam nella **versione 3.0.0**. Il numero di versione si
legge nel launcher, in basso a sinistra.

La traduzione funziona **solo con questa versione**, né precedente né
successiva. Se Steam aggiorna il gioco, la traduzione viene sovrascritta e
serve una nuova versione della mod adatta all'aggiornamento.

Servono circa **3,5 GB liberi** sul disco dove è installato il gioco, solo
durante l'installazione.

### Come si usa

1. Chiudi il gioco e il suo launcher.
2. Avvia **MGS1 ENG-ITA by Solid Crash.exe**.
3. Nella scheda **Master Collection** il programma cerca da solo la cartella del
   gioco. Se non la trova, selezionala con *Sfoglia*: in Steam la apri con
   tasto destro sul gioco → *Gestisci* → *Sfoglia i file locali*.
4. Premi **Applica la traduzione** e aspetta qualche minuto.
5. Avvia il gioco da Steam. Nel launcher scegli come gioco **Metal Gear
   Solid** (non *Special Missions*, *VR Missions* o *Metal Gear Solid
   Integral*) e come versione **Inglese (US)**.

Il programma controlla prima che i file siano proprio quelli originali della
3.0.0, prepara e verifica tutto a parte, e solo alla fine li installa. Al
termine verifica di nuovo il risultato, byte per byte.

### Tornare alla versione originale

In Steam: tasto destro sul gioco → *Proprietà* → *File installati* →
*Verifica integrità dei file di gioco*. Steam rimette i file originali.

### Uso insieme a MGSM2Fix

La traduzione è compatibile con MGSM2Fix e con le altre mod che non
modificano i file del gioco: puoi installarle prima o dopo, nell'ordine che
preferisci.

Attenzione però: fino alla versione 3.x, MGSM2Fix ha un difetto che sfasa i
sottotitoli dei filmati con riprese reali (quelli in stile documentario). Il
problema è stato individuato durante lo sviluppo di questa traduzione e
segnalato all'autore, insieme alla correzione. La correzione sarà inclusa in
MGSM2Fix 4.0.

Finché non esce la 4.0, se usi MGSM2Fix quei filmati avranno i sottotitoli
fuori sincrono. Senza MGSM2Fix, oppure con la 4.0 o successive, sono
sincronizzati correttamente.

---

## PlayStation (ROM)

### Che cosa ti serve

La tua copia del gioco in **versione americana (USA), revisione 1**. È quella
delle edizioni Original, Greatest Hits e The Essential Collection: la più
diffusa in assoluto.

Formati accettati: `.bin` + `.cue`, `.chd`, e in genere qualsiasi immagine
grezza del CD anche con estensione diversa (`.img`, `.mdf`). Il programma
riconosce il formato dal contenuto, non dal nome.

**Non funziona con i file `.iso` da 2048 byte per settore**: in quel formato i
filmati e l'audio del gioco sono già andati persi durante la creazione
dell'immagine. Non è un limite di questa mod — con un file così il gioco non
funziona bene nemmeno senza traduzione.

Se hai un `.pbp` o un `.ecm`, va prima riconvertito in `.bin` + `.cue`.

### Come si usa

1. Avvia **MGS1 ENG-ITA by Solid Crash.exe** e passa alla scheda
   **PlayStation (ROM)**.
2. Seleziona l'immagine del **disco 1**. Il programma riconosce da solo di
   quale disco si tratta.
3. Scegli la cartella dove salvare il risultato.
4. Scegli **60 Hz** o **50 Hz** (vedi sotto).
5. Premi **Applica la traduzione** e aspetta qualche minuto.
6. Ripeti tutto per il **disco 2**, con la stessa scelta di frequenza.

Il file originale non viene modificato: ne viene creata una copia tradotta
accanto. Puoi anche trascinare l'immagine del disco direttamente sopra l'icona
del programma.

Al termine il programma verifica da solo che il risultato sia corretto, byte
per byte.

### 60 Hz o 50 Hz?

Riguarda solo la sincronia dei sottotitoli nei **filmati con riprese reali**
(quelli in stile documentario). Il video scorre alla velocità del lettore CD,
ma i sottotitoli contano i fotogrammi della console: 60 al secondo in NTSC, 50
in PAL. Con l'impostazione sbagliata le battute accumulano ritardo e le ultime
non compaiono.

- **60 Hz — NTSC**: scegli questo se non hai mai toccato le impostazioni del
  tuo emulatore. È il caso della grande maggioranza delle persone.
- **50 Hz — PAL**: scegli questo solo se hai impostato apposta il tuo emulatore
  a 50 Hz.

Nel dubbio, 60 Hz. Se poi noti i sottotitoli dei filmati fuori sincrono, rifai
la procedura con l'altra opzione.

La Master Collection non ha questa scelta: lì i filmati sono già sincronizzati.

---

## Versione ufficiale e sicurezza

L'unica fonte ufficiale di questa mod è la pagina GitHub:
https://github.com/solidcrash/MGS1-ENG-ITA

Eventuali copie su altri siti sono elencate lì. Se trovi la mod altrove, con
un'impronta diversa da quella qui sotto, non è la versione originale.

### Impronta del programma ufficiale (v1.1)

| file | SHA-256 |
|---|---|
| MGS1 ENG-ITA by Solid Crash.exe | 28cc1606948f3726f157875ee0973471a54cb1e684defe703bbec0496e398073 |

Per controllarla: `certutil -hashfile "MGS1 ENG-ITA by Solid Crash.exe" SHA256`

### Antivirus

Analisi VirusTotal del programma ufficiale:
https://www.virustotal.com/gui/file/28cc1606948f3726f157875ee0973471a54cb1e684defe703bbec0496e398073

Al momento della pubblicazione riporta 3 segnalazioni su 69 (Bkav Pro, McAfee
Scanner, Zillya); Windows Defender e tutti i principali antivirus non segnalano
nulla. Sono falsi positivi tipici dei programmi Python distribuiti in un unico
eseguibile: all'avvio il programma si scompatta in una cartella temporanea e
lancia i due strumenti incorporati, xdelta3 e chdman. È lo stesso comportamento
dei *dropper*, da cui l'etichetta. Il codice sorgente del programma è
pubblicato sulla pagina GitHub, chiunque può controllarlo.

### Avviso di Windows

Al primo avvio Windows potrebbe mostrare «Windows ha protetto il PC», perché il
programma è nuovo e non ha una firma digitale a pagamento. Premi *Ulteriori
informazioni* → *Esegui comunque*.

### Supporto

L'unico modo per supportarmi è il pulsante **Supportami** del programma
ufficiale, che apre la mia pagina di donazione PayPal:
https://www.paypal.com/donate/?hosted_button_id=ZAUN4MNN3SPS4

La donazione è facoltativa e non sblocca nulla.

### Codice sorgente

Il codice del programma è pubblicato per trasparenza. Tutti i diritti
riservati: non è consentito ridistribuire versioni modificate del programma.

---

## Crediti

**Traduzione, adattamento e romhacking**: Mattia Moro (solidcrash)

Il testo italiano di base proviene dall'edizione PAL italiana pubblicata da
Konami.

Strumenti e ricerca che hanno reso possibile il lavoro:

- **DoktorDeSparkle** — `mgs1-scripts`, strumenti di estrazione per RADIO, VOX,
  DEMO, ZMOVIE e i formati degli archivi
- **FoxdieTeam** — `mgs_reversing`, codice decompilato del gioco, indispensabile
  per capire i formati interni, il font e l'impaginazione
- **xdelta3** di Joshua MacDonald — formato e motore delle patch
- **chdman**, dal progetto MAME — gestione dei file `.chd`

---

## Verifica dei file

Il programma controlla tutto da solo. Se vuoi farlo anche tu, su Windows le
impronte si calcolano dal Prompt dei comandi con:

    certutil -hashfile "percorso\del\file" SHA256

(per le immagini PlayStation originali usa `SHA1` al posto di `SHA256`).

### Master Collection 3.0.0 — file originali (SHA-256)

| file | dimensione | SHA-256 |
|---|---:|---|
| windata\alldata.bin | 11.317.041.152 | 0accf9ba768e7917bcd7765ab7971a517cf0d4fef42059a541a9a3953b58d579 |
| windata\alldata.psb.m | 249.554 | e703d2e0ecc2cdb6b1c6eaa15f329f945f56fe3af6eb6af54430faf2641fb568 |
| windata\dlc\dlc_usa.bin | 1.930.016.768 | 30e3d0fcd86d2da473bc321639b47b98e4e4c3ac6e37a23e525f40df84101313 |
| windata\dlc\dlc_usa.psb.m | 416 | 46e0ad04e9e05c9967b3153d0166713d85d913cc3bb358646aae8007d127cf9c |

### Master Collection 3.0.0 — dopo la traduzione (SHA-256)

| file | SHA-256 |
|---|---|
| windata\alldata.bin | 683bd8b0dbf50fab3094add5962b302dab0e71a9f974c81ec2dfbea6c1a0cbbb |
| windata\alldata.psb.m | 902abb29f0aad4a831102e0c515b99c6c3262f45098aeb462c2a4fd4c52d558a |
| windata\dlc\dlc_usa.bin | 50d4ee7056c557910b0955deace91b0d5b5f553a1e35dbbfc68276580b3ca2af |
| windata\dlc\dlc_usa.psb.m | 0fa9820a6dc41bacc49bbb10ff23f98eeee31b763f9fb473f7b90c4c3bae46b2 |

### PlayStation — immagini originali richieste (SHA-1)

| disco | dimensione | SHA-1 |
|---|---:|---|
| Disc 1 (Rev 1) | 705.614.112 | 37498e6598ce4eabf00630b6a9197b20861e55a0 |
| Disc 2 (Rev 1) | 731.911.824 | d6edfd60a375c10087eacebd709419950c8995ad |

Attenzione: la revisione originale (Rev 0) ha **esattamente la stessa
dimensione**, quindi il peso del file non basta a distinguerle. Serve l'hash.

### PlayStation — risultati attesi v1.1 (SHA-256)

| file | SHA-256 |
|---|---|
| Disc 1 — 60 Hz | 2c6e23cce9c6c56027b43ccff80dcd860a64953c1f95391451ef40c08add2ad7 |
| Disc 1 — 50 Hz | 0f394138471e4627b4e9566158a6034defc25d77c54973dc2beb3fa81b748f87 |
| Disc 2 — 60 Hz | 7d2a35b387c364b04a42b283faec2a66f0c649ba993a60d7010bdef8287a6f4e |
| Disc 2 — 50 Hz | e4231a351bddab616256d76773e696bdcee2d43bdee894427806e285a298f1c3 |

---

## Se qualcosa non va

### Master Collection

**"I file del gioco non corrispondono alla versione Steam 3.0.0"** — il gioco è
stato aggiornato a un'altra versione, oppure i file erano già modificati da
altre mod. Nel secondo caso usa *Verifica integrità dei file di gioco* in Steam
e riprova.

**"In parte originali e in parte tradotti"** — un'installazione precedente si è
interrotta. Usa *Verifica integrità dei file di gioco* in Steam e riprova.

**"Non riesco a modificare i file del gioco"** — chiudi il gioco e il launcher.
Se il gioco è installato dentro *Programmi*, riapri questo programma con tasto
destro → *Esegui come amministratore*.

### PlayStation

**"Immagine non riconosciuta"** — non stai partendo da un dump verificato della
versione americana Rev 1. Può succedere anche se l'immagine l'hai creata tu
estraendola in un formato non conforme.

**"Questa è la revisione originale (Rev 0)"** — hai la prima stampa. La
traduzione è costruita sulla Rev 1 e non può essere applicata su questa.

**"Già tradotta con la versione precedente (1.0)"** — riparti dall'immagine
originale americana.

**"Questa immagine non contiene i settori grezzi del CD"** — è un `.iso` da
2048 byte per settore. Vedi la sezione sui formati qui sopra.

**Il programma si chiude o non parte** — controlla di avere spazio libero
sufficiente: servono circa 1,5 GB per disco, e circa 3 GB se parti da un
`.chd`.

---

## Nota

Questa è una mod amatoriale senza scopo di lucro, non affiliata né autorizzata
da Konami. Non contiene dati del gioco e non ne sostituisce l'acquisto: si
applica esclusivamente a una copia che possiedi già.

Metal Gear Solid è un marchio di Konami.
