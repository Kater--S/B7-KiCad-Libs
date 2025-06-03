# PartDB Helper - Benutzerhandbuch

Ein Hilfsprogramm zur Verwaltung von Bauteilinformationen in PartDB, das dir hilft, LCSC-Teilenummern in die IPN-Felder deiner Bauteile zu übertragen.

## Was kann das Programm?

- Gruppiert deine Bauteile nach ihrem Status für bessere Übersicht
- Zeigt dir alle deine Bauteile mit ihren aktuellen IPN- und LCSC-Teilenummern an
- Kopiert automatisch LCSC-Anbieter-IDs in leere IPN-Felder
- Erlaubt dir das Überschreiben bestehender IPN-Felder mit der LCSC-Teilenummer

## Erste Schritte

1. Rufe die Website auf
2. Prüfe, ob der PartDB-URL korrekt hinterlegt ist
3. Klicke auf "Mit PartDB verbinden"
4. Warte, bis alle Bauteile geladen sind. Es gibt eine Übersichtstabelle mit allen Bauteilen. Diese sind je nach Status unterschiedlich farbig gekennzeichnet (siehe unten). Darunter werden jeweils die Bauteile mit gleichem Status zusammen angezeigt.

## Die Bauteilliste

Die Bauteilliste ist in vier Abschnitte unterteilt:

1. **Bauteile mit korrekter IPN** (grün markiert)
   - Diese Bauteile haben bereits die richtige LCSC-Teilenummer als IPN
   - Du musst hier nichts weiter tun
   - Um Platz zu sparen, erscheint hier lediglich die Anzahl der betreffenden Bauteile, keine Tabelle

2. **Bauteile ohne IPN** (gelb markiert)
   - Diese Bauteile haben eine LCSC-Teilenummer, aber keine IPN
   - Klicke auf "In IPN kopieren", um die LCSC-ID automatisch als IPN zu übernehmen

3. **Bauteile mit abweichender IPN** (orange markiert)
   - Diese Bauteile haben sowohl eine LCSC-Teilenummer als auch eine bereits eingetragene IPN, die aber nicht übereinstimmen, d.h. die IPN ist nicht die LCSC-Teilenummer
   - Wähle die gewünschten Bauteile mit den Checkboxen aus
   - Klicke auf "Ausgewählte überschreiben", um die IPN-Felder zu aktualisieren. Der alte Inhalt wird dabei überschrieben.

4. **Bauteile ohne LCSC-Information** (rot markiert)
   - Diese Bauteile haben keine LCSC-Anbieter-ID
   - Hier ist keine automatische Aktualisierung möglich, vielmehr muss zunächst in PartDB der Lieferant LCSC für dieses Bauteil eingepflegt werden. Danach kannst du die Bauteile in PartDB Helper neu laden. Die betreffenden Bauteile sollten dann in der "gelben Liste" erscheinen.
   

## Schritt-für-Schritt-Anleitung

### LCSC-ID als IPN übernehmen (für Bauteile ohne IPN)
1. Scrolle zum Abschnitt "Bauteile ohne IPN"
2. Klicke auf den "In IPN kopieren" Button
3. Warte, bis die Aktualisierung abgeschlossen ist

### IPN aktualisieren (für Bauteile mit abweichender IPN)
1. Scrolle zum Abschnitt "Bauteile mit abweichender IPN"
2. Aktiviere die Checkboxen neben den Bauteilen, die du aktualisieren möchtest
3. Klicke auf "Ausgewählte überschreiben"
4. Warte, bis die Aktualisierung abgeschlossen ist

## Was du wissen solltest

- Das Programm aktualisiert die Bauteile direkt in deiner PartDB-Datenbank
- Alle Änderungen werden sofort wirksam
- Du kannst die Aktualisierung jederzeit durch Aktualisieren der Seite überprüfen

## Bei Problemen

### Die Seite lädt nicht?
- Prüfe deine Internetverbindung
- Stelle sicher, dass PartDB erreichbar ist
- Versuche, die Seite neu zu laden

### Keine Aktualisierung sichtbar?
- Warte, bis der Ladevorgang abgeschlossen ist
- Aktualisiere die Seite manuell
- Prüfe, ob du die richtigen Bauteile ausgewählt hast

### Checkboxen fehlen?
- Stelle sicher, dass du dich im Abschnitt "Bauteile mit abweichender IPN" befindest
- Prüfe, ob die Bauteile tatsächlich unterschiedliche IPN- und LCSC-IDs haben

## Tipps

- Aktualisiere die Seite regelmäßig, um den aktuellen Stand zu sehen
- Überprüfe die Änderungen nach jeder Aktualisierung auch in PartDB
- Bei sehr vielen Bauteilen kann das Laden ein wenig dauern - hab bitte etwas Geduld 
