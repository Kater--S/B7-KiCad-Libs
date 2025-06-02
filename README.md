# B7-KiCad-Libs

Basis-Repository für die B7-Elektronikentwicklung


## Komponenten:

1. **KiCad** als Entwicklungsplattform für Elektronik
	* Projekte jeweils als GitHub-Repo
	* aktuelle Version 9 wird vorausgesetzt
	* JLCPCB Fabrication Toolkit soll verwendet werden
2. **eigene Libs** für Symbole und Footprints
	* je 1 Lib, keine Unteraufteilung
	* beide zusammen als gemeinsames GitHub-Repo
	* = dieses Repository
3. **PartDB** zur Verwaltung der eingesetzten Bauelemente
	* PartDB aktuell von Mike gehostet, später auf B7-Server
	* Anbindung an DigiKey, LCSC und andere Supplier
	* Symbole und Footprints als textueller(!) Verweis in B7-Libs
	* TBD: _immer_ eigenes Symbol und Footprint, KiCad-Libs werden nicht genutzt


## Einrichtung:

1. KiCad installieren (für alle Benutzer auf dem Computer)
2. JLCPCB Fabrication Toolkit installieren (pro Benutzer)
3. gepatchte Datei `process.py` aus dem Repo unter `${KICAD_3RD_PARTY}/plugins/com_github_bennymeg_JLC-Plugin-for-KiCad` kopieren (bezieht sich auf den Stand der Datei vom 2025-04-30, enthalten im Release v5.1.0 des Plugins)
4. PartDB-Account anlegen und API Key generieren
5. B7-Libs-Repo aus GitHub clonen nach `${KICAD_3RD_PARTY}`, d.h. dieses README.md liegt dann unter `${KICAD_3RD_PARTY}/B7-KiCad-Libs/README.md`
6. In `libs`: Template für `partd.kicad_httplib` kopieren und API Key aus PartDB eintragen
7. Ein Projekt öffnen, etwa `test/B7Test` oder `template/B7Template`
	- Darin sind die passenden Library-Einstellungen bereits vorgenommen:
		- in KiCad: Preferences → Manage Symbol Libraries…:
			- Project Specific Library `B7_Symbols` als Typ `KiCad` eintragen, Pfad ist `${KICAD_3RD_PARTY}/B7-KiCad-Libs/libs/B7.kicad_sym`; Description ist `B7 symbols`
			- Project Specific Library `B7_PartDB` als Typ `HTTP` eintragen, Pfad ist `${KICAD_3RD_PARTY}/B7-KiCad-Libs/libs/B7.kicad_sym`; Description ist `B7 PartDB`
		- in KiCad: Preferences → Manage Footprint Libraries…:
			- Project Specific Library `B7_Footprints` als Typ KiCad eintragen, Pfad ist `${KICAD_3RD_PARTY}/B7-KiCad-Libs/libs/B7.pretty`; Description ist `B7 footprints`
			- (PartDB-Anbindung gibt es hier nicht)
8. Eigene Projekte können aus dem Template-Projekt erstellt werden.
	- Wenn ein B7-Projekt als eigenes Repo gespeichert wird, müssen die Einstellungen wie beschrieben sein.


## Offene Punkte

- Aufteilung entspricht nicht den Default-Pfaden von KiCad (z.B. macOS: `~/Documents/KiCad/9.0/{symbols,footprints,projects}`). 
  Es sollte aber in Ordnung sein, dass Projekte (und Libs) auch außerhalb der Standardpfade liegen.
- Quer-Abhängigkeiten bei Pfaden müssen funktionieren
	- auch auf unterschiedlichen Plattformen (Linux, macOS, Windows)
	- auch mit abweichenden Speicherorten
	- → Verwendung von Environmentvariablen, wo möglich
	- Dies ist derzeit durch Verwendung von `${KICAD_3RD_PARTY}/`… gegeben
- TBD, ob die B7-Libs global oder projektspezifisch sein sollten
	- pro projektspezifisch: kein manuelles Setup notwendig, wenn Template verwendet oder bestehendes Projekt geladen wird
	- pro global: kein Setup notwendig bei Neuerstellung eines Projekts
	- aktuell implementiert: projektspezifisch
- Mechanismus zur Übernahme der LCSC-/JLCPCB-Teilenummer → PartDB und weiter von PartDB → KiCad – so, dass das Fabrication Toolkit sie erkennt und nutzt 
  → derzeit im ersten Schritt manueller Eintrag und im zweiten Schritt durch Patch des Plugins.
- Noch zu klären: Wie funktioniert die Definition von Array-Bauteilen, also bspw. Widerstandsarrays oder Mehrfachgattern?

## Verwendung

- Projekt anlegen: Template-Projekt laden, mit File → Save As… als neues Projekt speichern und dies als Repository anlegen
- vorhandenes B7-Bauteil verwenden: auswählen aus B7-Lib
- neues B7-Bauteil anlegen:
	- PartDB: TBD
	- KiCad: TBD


## Neues Bauteil anlegen

Vorausgesetzt wird eine Liste der einzupflegenden Bauteile. Darin könnten Einträge wie folgt aussehen:

|**lfd. Nr.**|**Hersteller- Typbezeichnung**|**Hersteller**|**Kurzbeschreibung**|**Kategorie**|**PartDB**|**Symbol**|**Footprint**|**LCSC Part#**|**Datenblatt**|
|---|---|---|---|---|---|---|---|---|---|
|10|CPDT6-5V0UPC-HF|Comchip|4 fach ESD Schutzarray 5V Dioden mit Sammelschiene|Halbleiter||||C2443674|CPDT6-5V0UPC-HF RevB242302.pdf|
|11|TMUX1204DQAR|Texas Instruments|4:1 Multiplexer 5V, 5Ohm|Halbleiter||||C1849379|TMUX1204.pdf|
|12|PI6ULS5V9617AUEX|Diodes Inc.|I2C Bus Repeater|Halbleiter||||C526728|PI6ULS5V9617C.pdf|

Exemplarisch soll das ESD-Schutzarray aus Zeile 10 ( = lfd.Nr.) eingepflegt werden. Dies ist nicht die interne PartDB-ID, denn diese wird von PartDB eigenständig fortlaufend vergeben und kann daher nicht vorab festgelegt werden! Diese lfd. Nr. wird nicht weiter verwendet, denn es gibt ohnehin schon die interne ID, die LCSC Part# sowie die Hersteller-Typbezeichnung.

**Vorschläge:** 
- Die Spalte mit der lfd. Nr. kann im Prinzip entfallen, da im Rechenblatt die Zeilen ohnehin nummeriert sind. 
- Es sollte zusätzlich eine Spalte *Prefix* geben, in der der Präfix-Buchstabe für das Bauelement aufgeführt ist (R für Widerstände, U für ICs, D für Dioden usw.), da es nicht immer eindeutig ist, wie der Buchstabe lauten sollte.

### PartDB

In der Oberfläche von PartDB wird jetzt aus der linken Seitenleiste *Tools → Create parts from info provider* geklickt. 

Im entsprechenden Formular wird jetzt unter *Keyword* die LCSC-Teilenummer `C2443674` eingetragen und unter *Providers* `LCSC`. Ein Klick auf den Button *Search* listet als Resultat das gewünschte Bauteil.

Mit dem Button *+* am rechten Ende der Zeile wird ein Dialog *Create new part* aufgelegt, bei dem das Formular mit den Informationen der LCSC-Website gefüllt wurde. Die einzelnen Felder können jetzt auf Plausibilität/Korrektheit geprüft werden.

Als interne PartDB-ID werde hier beispielsweise die 7 zugeteilt. Im Webformular steht diese Nummer dann oben rechts in der Titelzeile des blauen Bereichs, in Klammern gefolgt von der noch einzutragenen IPN (siehe unten). In der Listenansicht über die Kategorien können mit dem Zahnrad-Aufklappmenü die Felder *ID* und *IPN* aktiviert werden, wenn gewünscht.

Unter *Category* muss die Bauteil-Kategorie angegeben werden. Vorgeschlagen wird der Wert, den der Provider LCSC verwendet: `Circuit Protection -> ESD and Surge Protection (TVS -> ESD)` – wenn dieser String in das Feld kopiert wird, wird in einem Popup vorgeschlagen, die Kategorie anzulegen. Im vorliegenden Fall gibt es ein kleines Problem, weil der Pfeil `->` von PartDB als Ebenentrenner aufgefasst wird, hier kommt er aber beim zweiten Auftreten in den Klammern als Text vor. Dies könnte durch Ändern in `→` umgangen werden, der Eintrag lautet damit also `Circuit Protection -> ESD and Surge Protection (TVS → ESD)`. Allerdings gibt es mit Unicode-Sonderzeichen teilweise Probleme, insofern wäre es sicherer, anstelle `→` hier einfach `/` zu verwenden: `Circuit Protection -> ESD and Surge Protection (TVS / ESD)`. Es wird damit also eine Hauptkategorie `Circiot Protection` angelegt und darunter eine Subkategorie `ESD and Surge Protection (TVS / ESD)`. Darin wird das neue Bauteil insortiert.

Unter *Internal Part Number (IPN)* wird noch die `C2443674`, also die LCSC-Teilenummer aus unserer Tabelle, eingetragen. Das gepatchte Fabrication Toolkit übernimmt dieses Feld, das in KiCad als *Part-DB IPB* erscheint, später als *LCSC Part #* in die BOM (Datei `bom.csv`).

Unter *Attachments* kann als *Preview Image* ein Foto ausgewählt werden, falls vorhanden (hier gibt es keins). Unter *EDA Information* kann noch als *Reference prefix* z.B. `U` (oder `D`??) eingetragen werden, ein *Value* wird hier nicht benötigt. Es fehlen nun noch das *KiCad schematic symbol* und der *KiCad footprint*.

### KiCad

In den von LCSC importierten Information (und auch im verlinkten Datenblatt) findet sich als Footprint das Gehäuse `SOT-23-6`. 

KiCad wird nun beispielsweise mit dem Test-Projekt geöffnet, so dass die B7-Libs konfiguriert sind. 

Im Symbol Editor muss nun nach Möglichkeit ein passendes Schaltplansymbol gefunden werden. Mit den Informationen aus dem Datenblatt erscheint eine Suche nach `diode` hilfreich. Wenn man mit dem Mauscursor über einem Listeneintrag stehenbleibt, erscheint nach einer Weile ein Vorschaubild des entsprechenden Symbols. Wenn die Liste unter dem Mauscursor durchgescrollt wird, wechselt das Vorschaubild entsprechend, und man kann schnell eine größere Anzahl von Einträgen durchsehen. Im Falle des gesuchten Bauteils findet sich ein passendes Symbol in der Standardbibliothek `Power_Protection` unter dem Namen `NUP4202`; dieses wird nun geöffnet und mittels *File* → *Save As…* wird dieser Footprint mit dem Namen `CPDT6-5V0UPC-HF` in die Bibliothek `B7_Footprints` gespeichert. **Achtung:** Mit diesem Symbol ist bereits ein Standard-Footprint assoziiert. Dieser wird bei der Bauteildefinition in PartDB aber durch einen eigenen aus der B7-Footprint-Library ersetzt (der durchaus identisch aussehen kann).

Im Footprint Editor wird daher nun nach `SOT-23-6` gesucht, ein passender Eintrag findet sich in der Standardbibliothek `Package_TO_SOT_SMD` und kann mit Doppelklick geöffnet werden. Unter *File* → *Save As…* wird dieser Footprint nun in die Bibliothek `B7_Footprints` gespeichert.

### PartDB

Im PartDB-Formular wird entsprechend nun unter *KiCad schematic symbol* `B7_Symbols:CPDT6-5V0UPC-HF` eingetragen.

Unter *KiCad footprint* wird analog `B7_Footprints:SOT-23-6` eingetragen.

**Wichtig:** *Diese Einträge sind case-sensitive, d.h. wenn irrtümlich etwa `B7_footprints` angegeben wird, findet KiCad den Footprint nicht.*

**Problem:**
Es fehlt noch die LCSC-Teilenummer. Diese ist in PartDB bekannt, wird aber offenbar nicht über das API in KiCad übernommen. Manuell kann sie auf KiCad-Seite auch nicht eingetragen werden, weil die B7_PartDB-Library read-only ist, d.h. Änderungen können nur auf PartDB-Seite vorgenommen werden.

Aus diesem Grund wird jetzt manuell aus der Gruppe *Purchase information* unter *Supplier* `LCSC` der Wert des Feldes *Supplier part number*, hier im Beispiel also `C2443674`, kopiert und in der Gruppe *Advanced* in das Feld *Internal Part Number (IPN)* eingetragen.

**Achtung:** *Diese Verwendung des Feldes IPN kollidiert mit der für die PartDB-ID*

Mit dem Button *Save changes* wird die Transaktion abgeschlossen.

### KiCad

Im Testprojekt kann in KiCad nun geprüft werden, ob das Bauteil korrekt angelegt wurde:

Im Schaltplaneditor wird *Place Symbols* (Taste A) aufgerufen und in der Suchmaske `CPDT` eingegeben. Als Fundstelle wird – neben der reinen Symbol-Bibliothek `B7_Symbols` – die PartDB-Bibliothek `B7_PartDB - Circuit Protection` angegeben, also mit der Unterkategorie der ersten Stufe. Darin gibt es den Eintrag `CPDT6-5V0UPC-HF` mit passendem Symbol und Footprint in der Vorschau. Nach Bestätigen mit *OK* kann das Bauteil im Schaltplan platziert werden.

Ein Doppelklick auf das Symbol öffnet den Dialog *Symbol Properties*. Dort können die verschiedenen Parameter überprüft werden. Die LCSC-Teilenummer wird unter *Part-DB IPN* angezeigt.

Nach dem Wechseln auf den Platineneditor und einem *Update PCB from Schematic* (Taste F8) und dem entsprechenden Dialog erscheint der Footprint und kann platziert werden.

### Fabrication Toolkit

**Achtung:** Fabrication Toolkit findet in der offiziellen Version lediglich die MPN, also im Beispiel `CPDT6-5V0UPC-HF` als vermeintliche LCSC Part Number. Hier ist die oben erwähnte Softwareanpassung des Plugins notwendig, damit stattdessen die IPN verwendet wird. Nach dem Patch wird nun zuerst das Feld *IPN* geprüft, erst danach die anderen.

Wenn es für das Plugin eine neue Version (> v5.1.0) gibt, muss der Patch nach einem Update mindestens erneut installiert werden, eventuell ist auch eine Anpassung notwendig.

Für PartDB wurde ein Issue eingestellt, das eine Funktion vorschlägt, um weitere Felder ins API zu übernehmen. Wenn dies implementiert wird, werden sowohl das manuelle Eintragen der Teilenummer als auch der Patch voraussichtlich überflüssig.

Im PCB-Editor von KiCad kann das Fabrication Toolkit über das entsprechende Icon aufgerufen werden. Es erscheint ein Dialog mit weiteren Optionen (siehe Dokumentation zum Toolkit) und einem Button *Generate*, über den die Erzeugung der Produktionsdateien gestartet wird.