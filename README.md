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
3. PartDB-Account anlegen und API Key generieren
4. B7-Libs-Repo aus GitHub clonen nach `${KICAD_3RD_PARTY}`, d.h. dieses README.md liegt dann unter `${KICAD_3RD_PARTY}/B7-KiCad-Libs/README.md`
5. In `libs`: Template für `partd.kicad_httplib` kopieren und API Key aus PartDB eintragen
6. Ein Projekt öffnen, etwa `test/B7Test` oder `template/B7Template`
	- Darin sind die passenden Library-Einstellungen bereits vorgenommen:
		- in KiCad: Preferences -> Manage Symbol Libraries…:
			- Project Specific Library `B7_Symbols` als Typ `KiCad` eintragen, Pfad ist `${KICAD_3RD_PARTY}/B7-KiCad-Libs/libs/B7.kicad_sym`; Description ist `B7 symbols`
			- Project Specific Library `B7_PartDB` als Typ `HTTP` eintragen, Pfad ist `${KICAD_3RD_PARTY}/B7-KiCad-Libs/libs/B7.kicad_sym`; Description ist `B7 PartDB`
		- in KiCad: Preferences -> Manage Footprint Libraries…:
			- Project Specific Library `B7_Footprints` als Typ KiCad eintragen, Pfad ist `${KICAD_3RD_PARTY}/B7-KiCad-Libs/libs/B7.pretty`; Description ist `B7 footprints`
			- (PartDB-Anbindung gibt es hier nicht)
7. Eigene Projekte können aus dem Template-Projekt erstellt werden.
	- Wenn ein B7-Projekt als eigenes Repo gespeichert wird, müssen die Einstellungen wie beschrieben übernommen werden.


## Offene Punkte

- Aufteilung widerspricht den Default-Pfaden von KiCad (macOS: `~/Documents/KiCad/9.0/{symbols,footprints,projects}`). 
  Es sollte aber in Ordnung sein, dass Projekte (und Libs) auch außerhalb der Standardpfade liegen.
- Quer-Abhängigkeiten bei Pfaden müssen funktionieren
	- auch auf unterschiedlichen Plattformen (Linux, macOS, Windows)
	- auch mit abweichenden Speicherorten
	- → Verwendung von Environmentvariablen, wo möglich
- TBD, ob die B7-Libs global oder projektspezifisch sein sollten
	- pro projektspezifisch: kein manuelles Setup notwendig, wenn Template verwendet oder bestehendes Projekt geladen wird
	- pro global: kein Setup notwendig bei Neuerstellung eines Projekts


## Verwendung

- Projekt anlegen: Template-Projekt laden, mit File -> Save As… als neues Projekt speichern und dies als Repository anlegen
- vorhandenes B7-Bauteil verwenden: auswählen aus B7-Lib
- neues B7-Bauteil anlegen:
	- PartDB: TBD
	- KiCad: TBD

