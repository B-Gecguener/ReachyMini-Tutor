# VT-Kapitel 4 - Domänenmodell (36 Folien)

## Folie 1: Verteilte Systeme
(Titel-/Gliederungsfolie ohne weiteren Inhalt)

## Folie 2: Das Domänenmodell
(Titel-/Gliederungsfolie ohne weiteren Inhalt)

## Folie 3: Das Domänenmodell
Thema: Definitionsfolie, die den Begriff „Domänenmodell" einführt und definiert.
Inhalt: Unter der Überschrift „Definition" wird ein Domänenmodell (Domain Model) als eine visuelle Repräsentation der problemrelevanten Konzepte einer Domäne definiert. Die Definition wird als Zitat M. Fowler zugeschrieben.

## Folie 4: Konzepte im Domänenmodell
Thema: Die Folie erklärt, dass Konzepte im Mittelpunkt des Domänenmodells stehen, und illustriert dies am Beispiel des Konzepts „Buchung".
Inhalt: Im Mittelpunkt des Domänenmodells stehen Konzepte, wobei die Symbole und Intentionen von Konzepten besonders wichtig sind. Als Beispiel wird das Konzept „Buchung" herangezogen. Zu diesem Konzept ist ein Definitionstext angegeben: „Eine Buchung beschreibt die Belegung eines Raums für eine bestimmte Zeit. Sie hat einen Titel und eine Beschreibung". Abschließend wird in einem hervorgehobenen Kasten darauf hingewiesen, dass Verantwortlichkeiten und Verhalten erst später (beim Design) festgelegt werden.
Abbildung: Ein UML-Klassendiagramm, das das Konzept „Buchung" mit seinen Attributen darstellt; es dient auf der Folie als Beispiel für ein Konzept im Domänenmodell.

## Folie 5: Erstellung eines Domänenmodell
Thema: Die Folie beschreibt das Vorgehen zur Erstellung eines Domänenmodells in vier Schritten.
Inhalt: Die Folie trägt den Titel „Erstellung eines Domänenmodell" und stellt die Leitfrage „Wie erstellt man ein Domänenmodell?". Unter der Überschrift „Vorgehen:" werden vier nummerierte Schritte aufgeführt. Schritt 1 lautet: Identifizieren von Konzept-Kandidaten. Schritt 2 lautet: Konzepte als Klassen in ein UML-Klassendiagramm eintragen. Schritt 3 lautet: Relevante Beziehungen zwischen Konzepten als Assoziationen dem Klassendiagramm hinzufügen. Schritt 4 lautet: Konzepte um die relevanten und nötigen Attribute anreichern.

## Folie 6: Wie identifiziert man die Konzepte?
Thema: Die Folie stellt Strategien vor, mit denen man Konzepte für ein Domänenmodell identifiziert.
Inhalt: Der Titel lautet „Wie identifiziert man die Konzepte?“. Darunter wird die Überschrift „Strategien zum Identifizieren von Konzepten:" gezeigt, gefolgt von einer Aufzählung mit drei Hauptpunkten. Der erste Punkt ist „Erfahrung und Intuition". Der zweite Punkt ist „Analyse bereits vorhandener Domänenmodelle". Der dritte Punkt lautet „Anwendung von Kreativtechniken, z.B.:" und enthält die Unterpunkte „Identifikation von Nominalphrasen", „Konzept-Kategorien-Liste" sowie ein Auslassungspunkt („…"). Rechts daneben befindet sich ein hervorgehobener Textkasten mit dem Namensschild „Craig Larman". Darin steht: Larman empfiehlt, immer wenn möglich auf vorhandene Modelle zurückzugreifen. Es gibt veröffentlichte, gewissenhaft erstellte Domänenmodelle und Datenmodelle (die man in Domänenmodelle umwandeln kann) für viele gebräuchliche Domänen (z.B. Inventar, Finanz, Gesundheit, …). Als Beispiele werden Bücher genannt: „Analysis Patterns" von Martin Fowler, „Data Model Patterns" von David Hay, „Data Model Resources" von Len Silverston. Am unteren Rand der Folie steht der Hinweis: „Kombinierte Anwendung der Methoden ist empfehlenswert!"

## Folie 7: Gefundene Konzepte (I)
Thema: Die Folie zeigt eine beispielhafte Liste von Konzepten, die für eine Matrixproduktion mit Fokus auf AGVs über Erfahrung und Intuition (bzw. ChatGPT) gefunden werden könnten, und leitet zur Anwendung von Kreativtechniken über.
Inhalt: Der Titel der Folie lautet "Gefundene Konzepte (I)". Es wird ausgeführt, dass Erfahrung und Intuition (ChatGPT) für die Matrixproduktion (mit Fokus auf AGVs) beispielsweise folgende Konzepte finden könnten: AGV, Produkt, Produktvariante, Fertigungsauftrag, Ladestation, Sensorik, Zielpunkt, Haltepunkt, und weitere (abgekürzt mit "…"). Anschließend wird die Frage gestellt, ob alle relevanten Konzepte gefunden wurden. Darauf folgt ein Hinweis mit Pfeil auf die "Anwendung der Kreativtechniken".

## Folie 8: Identifikation von Nominalphrasen
Thema: Die Folie stellt die Nominalphrasenmethode (nach Barbara Abbot, 1983) zur Identifikation von Nominalphrasen als Kreativtechnik vor.
Inhalt: Der Titel lautet „Identifikation von Nominalphrasen", der Untertitel „Nominalphrasenmethode (nach Barbara Abbot - 1983)". Ein Hinweis-Kasten besagt: „Detaillierte Use Cases bieten eine exzellente Grundlage für diese Technik!". Unter der Überschrift „Vorgehen:" werden zwei Schritte genannt: Erstens soll man Nomen und Nominalphrasen in Beschreibungen des Problembereichs identifizieren, etwa in Anforderungen, Anwendungsfällen oder ChatGPT-Ergebnissen. Zweitens soll man sie als Kandidaten für Konzepte und Attribute in Betracht ziehen. Unter der Überschrift „Achtung:" wird darauf hingewiesen, dass wegen der in natürlichsprachlichen Texten inhärenten Ungenauigkeit und Mehrdeutigkeit dieses Verfahren nicht automatisiert werden kann. In Konsequenz muss man die so gewonnenen Kandidaten einer sorgfältigen Prüfung unterziehen.

## Folie 9: Nominalphrasen am Beispiel
Thema: Die Folie zeigt ein konkretes Beispiel für die Anwendung der Nominalphrasenmethode auf die Domäne der Matrixproduktion mit Fokus auf AGV-Steuerung.
Inhalt: Der Titel lautet "Nominalphrasen am Beispiel" mit dem Untertitel "Matrixproduktion mit Fokus auf AGV-Steuerung". Die Folie listet in zwei Spalten verschiedene Nominalphrasen bzw. Konzepte auf. In der linken Spalte stehen: "AGV (Automated Guided Vehicle)" mit dem Unterpunkt "ID, Status, Beladungskapazität, Energiezustand"; "AGV-Typ" mit dem Unterpunkt "z. B. Hubfahrzeug, Plattform, Kettenförderer"; "Fahrroute / Route"; sowie "Fahrbefehl / Transportauftrag". In der rechten Spalte stehen: "Ladestation / Ladevorgang"; "Sensorik"; "Zielpunkt / Haltepunkt"; "Transportgut / Material"; sowie "Navigationssystem (z. B. SLAM, QR-Code, Spurführung)". Am unteren rechten Rand befindet sich ein Kasten mit der Überschrift "Hinweis", der folgenden Text enthält: "Die generierten Konzepte sind sehr Generisch! Dienen aber für weitere Prompts, wie bspw. Was ist ein Fahrbefehl, …".

## Folie 10: RBS: Ein erstes Domänenmodell
Thema: Die Folie stellt ein erstes Domänenmodell für RBS vor, das aus aus ChatGPT ausgewählten Konzepten besteht, und formuliert ein kartographisches Vorgehen für die Modellbildung.
Inhalt: Der Titel lautet „RBS: Ein erstes Domänenmodell". Darunter steht der Hinweis, dass Konzepte aus ChatGPT ausgewählt wurden. Die ausgewählten Konzepte sind: AGV, Route, Transportauftrag, Ladestation, Zielpunkt und Transportgut. Rechts unten befindet sich ein Kasten mit der Überschrift „Vorgehen wie ein Kartograph", der drei Regeln auflistet: Erstens, im Gebiet vorhandene Bezeichner nutzen. Zweitens, irrelevante oder problemfremde Dinge weglassen. Drittens, nichts hinzufügen, was es in dem Gebiet nicht gibt.

## Folie 11: Konzept vs. Attribut
Thema: Die Folie gibt einen kurzen Vorgriff auf den Unterschied zwischen Konzept und Attribut und liefert dazu eine Faustregel.
Inhalt: Der Titel lautet „Konzept vs. Attribut", gefolgt vom Untertitel „Ein kleiner Vorgriff". Darunter steht der Satz „Unterschied zwischen Konzept als Attribut als Faustregel:". Im Folgenden wird in einem hervorgehobenen Kasten die Faustregel formuliert: „Wenn X kein primitiver Typ (Text oder Zahl) ist, dann ist X wahrscheinlich ein Konzept, und kein Attribut." Am Ende der Folie steht rechts der Hinweis „… to be continued".

## Folie 12: Das Domänenmodell
(Titel-/Gliederungsfolie ohne weiteren Inhalt)

## Folie 13: Wie kommt man zu Assoziationen?
Thema: Die Folie erklärt, wie man im Domänenmodell zu Assoziationen kommt und welche Quellen dafür herangezogen werden.
Inhalt: Ins Domänenmodell gehören Assoziationen, … über deren Beziehung man eine Zeit lang Bescheid wissen muss („Need To Know“-Assoziationen), damit das System funktionieren kann. Als Quelle dienen wiederum Anforderungen und Anwendungsfälle. In einem darauf folgenden Hinweis (überschrieben mit „Achtung!") wird betont, dass Assoziationen im Domänenmodell lediglich Beziehungen aus konzeptueller Sicht sind und nichts über Datenflüsse, Datenbank-Tabellen und Fremdschlüssel sowie Attribute in der finalen Software-implementierung aussagen.

## Folie 14: Wichtige Assoziationen
Thema: Die Folie listet die besonders wichtigen Assoziations-Kategorien auf, die grundsätzlich ins Domänenmodell gehören.
Inhalt: Besonders wichtig sind folgende Assoziations-Kategorien. Erstens: A ist physischer oder logischer Teil von B. Zweitens: A ist physisch oder logisch in B enthalten. Drittens: A wird in B aufgezeichnet/protokolliert. Diese gehören grundsätzlich ins Domänenmodell.

## Folie 15: RBS: „Need To Know“-Assoziationen
Thema: Die Folie führt drei konkrete Beispiele für „Need To Know“-Assoziationen im RBS-Kontext an und erklärt jeweils, welches Wissen die Assoziation bereitstellt.
Inhalt: Unter der Überschrift „Beispiele“ werden drei Fälle aufgeführt. Erstens: Um zu wissen, wann die Buchung stattfindet, wird die Assoziation „findetStattAn“ zwischen den Konzepten Buchung und Termin verwendet. Zweitens: Um zu wissen, in welchem Raum ein Termin stattfindet und wann welcher Raum bereits belegt ist, wird die Assoziation „findetStattIn“ zwischen Termin und Raum verwendet. Drittens: Um Räume in dem gewünschten Gebäude zu finden, wird die Assoziation „enthält“ zwischen Gebäude und Raum verwendet.
Abbildung: Drei kleine Assoziationsdiagramme, die jeweils zwei Konzept-Boxen durch eine benannte Verbindungslinie verknüpfen; sie dienen als grafische Beispiele für die drei genannten „Need To Know“-Assoziationen.

## Folie 16: Relevanz der Assoziationen
Thema: Die Folie erklärt, dass gefundene Assoziationen auf ihre Relevanz geprüft und irrelevante Assoziationen weggelassen werden müssen.
Inhalt: Gefundene Assoziationen müssen auf Relevanz geprüft werden. Assoziationen sollen weggelassen werden, die weder in den Anforderungen noch für das Verständnis der Konzepte relevant sind. Als Beispiele werden zwei Fälle angeführt: Erstens indizieren die Anforderungen eine Notwendigkeit, das Inventar pro Raum zu verwalten. Zweitens indizieren die Anforderungen keine Notwendigkeit, festzuhalten, dass ein Raum benachbart ist zu einem anderen.
Abbildung: Zwei kleine UML-Assoziationsdiagramme als Beispiele: eines zeigt eine Assoziation „enthält“ zwischen den Konzepten „Raum“ und „Inventar“, das andere eine reflexive Assoziation „liegtNeben“ zwischen zwei Instanzen des Konzepts „Raum“. Sie dienen als Beispiel dafür, welche Assoziation relevant (erhalten) und welche irrelevant (weggelassen) ist.

## Folie 17: RBS: Domänenmodell mit Assoziationen
Thema: Die Folie zeigt ein UML‑Domänenmodell des Raum‑Buchungssystems (RBS) mit den beteiligten Klassen und deren Assoziationen.
Inhalt: Der Titel der Folie lautet „RBS: Domänenmodell mit Assoziationen", ergänzt um den Verweis „Aus Larman". Gegenstand der Folie ist ein Domänenmodell‑Diagramm, das die Klassen des Raum‑Buchungssystems und die Beziehungen zwischen ihnen darstellt.
Abbildung: Ein UML‑Domänenmodell‑Diagramm mit acht Klassenboxen, die nur Klassennamen tragen (keine Attribute, keine Methoden, keine Sichtbarkeiten): Raumwunsch, Buchungswunsch, Benutzer, Raum, Termin, Buchung, Inventar, Gebäude. Die Beziehungen sind jeweils eine durchgezogene Linie (Assoziation bzw. Komposition) mit einem kleinen gefüllten Dreieck als Leserichtung neben dem Assoziationsnamen; es gibt keine gestrichelten Linien, keine hohlen Dreiecke und keine offenen Pfeilspitzen. Die Beziehungen im Einzelnen: - Raumwunsch – Buchungswunsch: Assoziation; ohne Namen; Dreieck zeigt auf Raumwunsch; Multiplizität 1 / 1; Symbole an den Enden: keins / keins. - Buchungswunsch – Benutzer: Assoziation; Name „macht"; Dreieck zeigt auf Buchungswunsch (gelesen: „Benutzer macht Buchungswunsch"); Multiplizität * / 1; Symbole an den Enden: keins / keins. - Raumwunsch – Raum: Assoziation; Name „erfüllt"; Dreieck zeigt auf Raumwunsch (gelesen: „Raum erfüllt Raumwunsch"); Multiplizität * / *; Symbole an den Enden: keins / keins. - Buchungswunsch – Buchung: Assoziation; Name „erfüllt"; Dreieck zeigt auf Buchungswunsch (gelesen: „Buchung erfüllt Buchungswunsch"); Multiplizität 1 / 0..1; Symbole an den Enden: … [gekürzt]

## Folie 18: Das Domänenmodell
(Titel-/Gliederungsfolie ohne weiteren Inhalt)

## Folie 19: Attribute
Thema: Die Folie definiert, anhand welcher Kriterien und einer Faustregel Informationen als Attribute im Domänenmodell zu erkennen sind.
Inhalt: Der Titel lautet „Attribute" mit dem Untertitel „Kriterien & Faustregel". Unter „Kriterium 1" steht: Attribute sind solche Informationen, für die die Anforderungen vorschreiben, dass sie gemerkt werden müssen. Unter „Kriterium 2" steht: Als Attribut kommen nur „pure Werte" in Frage, die keine eigenständige Identität haben. In einem hervorgehobenen Kasten mit dem Titel „Faustregel:" steht: Wenn X kein primitiver Typ (Text oder Zahl) ist, dann ist X wahrscheinlich ein Konzept, und kein Attribut.

## Folie 20: Attribute
Thema: Die Folie zeigt anhand von zwei konkreten Beispielen, wie aus formulierten Anforderungen Attribute im Domänenmodell abgeleitet werden.
Inhalt: Der Titel lautet „Attribute" mit dem Untertitel „Beispiele" (im Gegensatz zur vorherigen Folie, die „Kriterien & Faustregel" als Untertitel hatte). Es folgen zwei Beispiele, jeweils eingeleitet durch einen diagonalen Pfeil und gefolgt von einer Ableitung mit einem geraden Pfeil. Im ersten Beispiel steht: „Um dem Benutzer eine Bestätigung schicken zu können, muss ich seine Mail-Adresse kennen." Daraus folgt die Ableitung: „Benutzer benötigt Attribut eMail". Im zweiten Beispiel steht: „Um passende Raumvorschläge liefern zu können, muss ich von einem Raum den Typ und die Kapazität kennen." Daraus folgt die Ableitung: „Raum benötigt Attribute kapazität, raumtyp (auch Assoziation!)".

## Folie 21: Typische Attribute
Thema: Die Folie listet typische Attribute im Domänenmodell auf und unterscheidet dabei Attribute mit primitiven von solchen mit nichtprimitiven Typen.
Inhalt: Der Titel der Folie lautet "Typische Attribute". Es wird angegeben, dass Attribute mit primitiven Typen vorkommen, und zwar Boolean, String (Text), Number und endlicher Aufzählungstyp. Als Beispiele dafür werden genannt: Anzahl, Zeitpunkt, Passnummer, Schalterposition, Postleitzahl, Beschreibungstext, Farbe, Name und so weiter. In doppelten Klammern folgt ein Hinweis auf Attribute nichtprimitiver Typen, falls nicht analysiert, mit den Beispielen Datum, Adresse, ISBN-Nummer und so weiter. Abschließend steht in einem hervorgehobenen Kasten, dass ein Domänenmodell der Kommunikation und dem Sichklarwerden dienen soll, wie die relevante Struktur (Konzepte, Beziehungen) aussieht, und dass dargestellt wird, was wichtig ist.

## Folie 22: IDs als Attribute?
Thema: Die Folie erklärt, warum IDs nicht als Attribute im Domänenmodell verwendet werden dürfen, sondern dass es sich dabei um Beziehungen handelt.
Inhalt: Der Titel lautet „IDs als Attribute?" und wird als „Typischer Fehler" eingeführt. Es wird die Frage gestellt, ob „aktuelleBenutzerKennung" als Attribut von „Buchungswunsch" geeignet ist, worauf die Antwort „NEIN!" folgt. Es wird ausgeführt, dass der Benutzer einen Buchungswunsch macht, woraus sich ergibt, dass es sich um eine Beziehung handelt. Daraus folgt eine Assoziation zwischen Benutzer und Buchungswunsch. Abschließend wird die Regel formuliert: Keine Beziehungen in IDs codieren!. In einem separaten Kasten mit der Überschrift „Reminder" steht der Hinweis, dass das Domänenmodell für Leute in der Domäne verständlich sein sollte.

## Folie 23: RBS: Domänenmodell mit Attributen
Thema: Die Folie zeigt das Domänenmodell (Klassendiagramm) eines Raum-Buchungs-Systems (RBS) mit Attributen, nach Larman.
Inhalt: Der Titel lautet „RBS: Domänenmodell mit Attributen". Darunter steht die Quellenangabe „[Larman]". Der Hauptinhalt der Folie ist ein UML-Domänenmodell, das im Abschnitt ABBILDUNGEN beschrieben wird.
Abbildung: Ein UML-Domänenmodell (Klassendiagramm) mit acht Klassen, deren Attribute und den Beziehungen zwischen ihnen. Klassen und Attribute: - Raumwunsch: zulaessigeRaumtypen, benoetigteKapazitaet, benoetigtesInventar - Buchungswunsch: benoetigteDauer, erlaubterZeitraum - Benutzer: name, email - Raum: kapazitaet, raumnummer, raumtyp - Termin: gebuchterZeitraum - Buchung: titel, beschreibung - Inventar: name, defekt - Gebäude: adresse, oeffnungszeiten Beziehungen (alle als Assoziationen mit durchgezogener Linie; ein offener Pfeil kennzeichnet die Navigierbarkeit, ein kleines gefülltes Dreieck neben dem Namen nur die Leserichtung des Namens): - Raumwunsch (1) — Buchungswunsch (1): Assoziation mit offenem Pfeil Richtung Raumwunsch. - Buchungswunsch (*) — Benutzer (1): Assoziation mit offenem Pfeil Richtung Buchungswunsch, Rollenname „macht". - Buchungswunsch (1) — Buchung (0..1): Assoziation mit offenem Pfeil Richtung Buchungswunsch, Rollenname „erfüllt". - Benutzer (1) — Buchung (*): Assoziation mit gefülltem Dreieck (Leserichtung) neben dem Rollennamen „gehört". - Raumwunsch (*) — Raum (*): Assoziation mit gefülltem Dreieck (Leserichtung) neben dem Rollennamen „erfüllt". - Raum (1) — … [gekürzt]

## Folie 24: Das Domänenmodell
(Titel-/Gliederungsfolie ohne weiteren Inhalt)

## Folie 25: RBS: Domänenmodell mit Generalisierung
Thema: Die Folie erinnert daran, wann man im Domänenmodell generalisieren darf, und zeigt ein Beispiel für eine Generalisierungsstruktur.
Inhalt: Der Titel lautet „RBS: Domänenmodell mit Generalisierung" mit der Quellenangabe [Larman]. Darunter steht die Frage „Erinnerung: Wann darf man generalisieren?". Als Antwort werden zwei Regeln aufgeführt: die „100%-Regel" und die „Ist-ein Regel".
Abbildung: Ein UML-Vererbungsdiagramm, das eine Generalisierungsstruktur mit einer Basisklasse und mehreren abgeleiteten Klassen darstellt; es dient als Beispiel für die Generalisierung im Domänenmodell.

## Folie 26: RBS: Domänenmodell mit Generalisierung
Thema: Die Folie zeigt ein vollständiges UML‑Domänenmodell als Beispiel nach Larman, das eine Generalisierungsstruktur (Inventar mit Unterarten) enthält.
Inhalt: Der Titel lautet „RBS: Domänenmodell mit Generalisierung", darunter steht die Quellenangabe „Beispiel nach Larman". Die Folie stellt damit das komplette Domänenmodell als Beispiel dar, das gegenüber der vorherigen Folie um die konkreten Klassen und Beziehungen erweitert ist; neu ist insbesondere die Generalisierungsstruktur, bei der die Klassen Beamer, Tafel und Whiteboard von der Oberklasse Inventar abgeleitet sind.
Abbildung: Ein UML‑Domänenmodell‑Diagramm mit folgenden Klassen und Attributen: - Raumwunsch: zulaessigeRaumtypen, benoetigteKapazitaet, benoetigtesInventar - Buchungswunsch: benoetigteDauer, erlaubterZeitraum - Benutzer: name, email - Raum: kapazitaet, raumnummer, raumtyp - Termin: gebuchterZeitraum - Buchung: titel, beschreibung - Gebäude: adresse, oeffnungszeiten - Inventar: defekt - Beamer (keine Attribute) - Tafel (keine Attribute) - Whiteboard (keine Attribute) Beziehungen: - Raumwunsch – Buchungswunsch: einfache Assoziation (durchgezogene Linie ohne Raute, ohne hohles Dreieck, ohne Pfeilspitze), Multiplizität 1 an Raumwunsch und 1 an Buchungswunsch, mit einem kleinen gefüllten Dreieck als Leserichtung; kein Assoziationsname. - Buchungswunsch – Benutzer: einfache Assoziation mit dem Namen „macht" und Leserichtungsdreieck zur Seite Buchungswunsch (gelesen als „Benutzer macht Buchungswunsch"); Multiplizität * an Buchungswunsch, 1 an Benutzer. - Buchungswunsch – Buchung: einfache Assoziation mit dem Namen „erfüllt" und Leserichtungsdreieck zur Seite Buchungswunsch (gelesen als „Buchung erfüllt Buchungswunsch"); Multiplizität 1 an Buchungswunsch, 0..1 an Buchung. - Raumwunsch – Raum: … [gekürzt]

## Folie 27: RBS: Weitere Iterationen
Thema: Die Folie zeigt ein UML‑Domänenmodell (Beispiel nach Larman) für ein Raum‑Buchungssystem und stellt mit drei Sprechblasen offene Fragen für weitere Iterationen des Modells.
Inhalt: Der Titel lautet „RBS: Weitere Iterationen" mit dem Untertitel „Beispiel nach Larman". Drei pinkfarbene Sprechblasen stellen Fragen, die auf bestimmte Klassen des Modells zeigen: „Lehrveranstaltungen?" (zeigt auf die Klasse Raumwunsch), „Hausmeister?" (zeigt auf die Klasse Benutzer) sowie „Multi‑Raumbuchungen und Periodische Buchungen?" (zeigt auf den Bereich der Klassen Buchung und Termin).
Abbildung: Ein UML‑Domänenmodell‑Diagramm mit folgenden Klassen und Attributen: - Raumwunsch: zulaeessigeRaumtypen, benoetigteKapazitaet, benoetigtesInventar - Buchungswunsch: benoetigteDauer, erlaubterZeitraum - Benutzer: name, email - Raum: kapazitaet, raumnummer, raumtyp - Termin: gebuchterZeitraum - Buchung: titel, beschreibung - Gebäude: adresse, oeffnungszeiten - Inventar: defekt - Beamer (ohne Attribute) - Tafel (ohne Attribute) - Whiteboard (ohne Attribute) Beziehungen: - Raumwunsch zu Buchungswunsch: Assoziation, Multiplizität 1 (Raumwunsch) zu 1 (Buchungswunsch), Navigierbarkeit (offener Pfeil) Richtung Raumwunsch. - Buchungswunsch zu Benutzer: Assoziation mit Rollename „macht", Multiplizität * (Buchungswunsch) zu 1 (Benutzer), Navigierbarkeit Richtung Buchungswunsch. - Raumwunsch zu Raum: Assoziation mit Rollename „erfüllt" (mit kleinem gefülltem Dreieck als Leserichtung), Multiplizität * (Raumwunsch) zu 1 (Raum). - Buchungswunsch zu Buchung: Assoziation mit Rollename „erfüllt", Multiplizität 1 (Buchungswunsch) zu 0..1 (Buchung), Navigierbarkeit Richtung Buchungswunsch. - Benutzer zu Buchung: Assoziation mit Rollename „gehört" (mit kleinem gefülltem Dreieck als Leserichtung), … [gekürzt]

## Folie 28: RBS: Iteriertes Domänenmodell
Thema: Die Folie zeigt das iterierte Domänenmodell (UML‑Klassendiagramm) des Raum‑Buchungssystems (RBS) als Beispiel nach Larman.
Inhalt: Der Titel lautet „RBS: Iteriertes Domänenmodell". Darunter steht der Untertitel „Beispiel nach Larman". Der Rest der Folie besteht aus dem unten beschriebenen UML‑Klassendiagramm.
Abbildung: Ein UML‑Klassendiagramm (Domänenmodell) mit folgenden Klassen und Attributen (keine Sichtbarkeitsmarker und keine Typen im Bild angegeben): Klassen: - Hausmeister (ohne Attribute) - Benutzer: email, name - Buchungswunsch: benoetigteDauer, erlaubterZeitraum, startDatum, endDatum, periode - Raumwunsch: zulaeissigeRaumtypen, benoetigteKapazitaet, benoetigtesInventar - Inventar: defekt - Gebaeude: adresse, oeffnungszeiten - Raum: kapazitaet, raumnummer, raumtyp - Beamer (ohne Attribute) - Tafel (ohne Attribute) - Whiteboard (ohne Attribute) - Lehrveranstaltung: name - PeriodischeBuchung: periode - Buchung: titel, beschreibung - Termin: gebuchterZeitraum - Multiraumbuchung (ohne Attribute) - Raumbuchung (ohne Attribute) Vererbungsbeziehungen (durchgezogene Linie mit hohlem Dreieck an der Oberklasse): - Beamer, Tafel und Whiteboard vererben jeweils von Inventar. - Multiraumbuchung und Raumbuchung vererben jeweils von Buchung. Assoziationen (durchgezogene Linie; ein kleines gefülltes Dreieck neben dem Rollennamen kennzeichnet nur die Leserichtung des Namens; ein offener Pfeil kennzeichnet die Navigierbarkeit): - Hausmeister (1..*) – Benutzer (1), mit offenem Pfeil Richtung Benutzer. - … [gekürzt]

## Folie 29: Das Domänenmodell
(Titel-/Gliederungsfolie ohne weiteren Inhalt)

## Folie 30: Strukturierung großer Domänenmodelle
Thema: Die Folie behandelt die Strukturierung großer Domänenmodelle.
Inhalt: Die Folie stellt die Frage, wie man ein großes Modell in mehrere kleine aufteilen kann. Als Lösung wird die Strukturierung mittels Pakete genannt.

## Folie 31: Strukturierung großer Domänenmodelle
Thema: Die Folie ist eine Wiederholungsfolie, die allgemeine Richtlinien zur Strukturierung großer Domänenmodelle durch Gruppierung in Pakete zusammenfasst.
Inhalt: Die Folie trägt den Titel "Strukturierung großer Domänenmodelle" und ist als "Wiederholung" gekennzeichnet. Unter der Überschrift "Allgemeine Richtlinien:" wird die Grundregel aufgestellt, dass man Elemente in ein gemeinsames Paket gruppieren soll, wenn sie bestimmte Bedingungen erfüllen. Diese Bedingungen werden in einer Aufzählung mit vier Punkten genannt: Erstens, wenn die Elemente nach Konzept oder Zweck ähnlich sind. Zweitens, wenn sie in derselben Typhierarchie liegen. Drittens, wenn sie an denselben Anwendungsfällen teilnehmen. Viertens, wenn sie sehr stark assoziiert sind. Abschließend wird die Regel formuliert, dass Paketnamen erst nach der Gruppierung festgelegt werden sollen.

## Folie 32: Pakete für Raumbuchungssystem
Thema: Die Folie zeigt ein Beispiel für die Gliederung eines Raumbuchungssystems in Pakete innerhalb einer Domain.
Inhalt: Der Titel lautet "Pakete für Raumbuchungssystem". Als Quelle wird [Larman] angegeben.
Abbildung: Ein Paket-Diagramm (dargestellt als Ordner-Symbole). Ein großes äußeres Paket trägt den Namen "Domain". Innerhalb dieses Pakets sind drei kleinere Pakete enthalten, die nebeneinander angeordnet sind und die Namen "Buchungsverwaltung", "Raumverwaltung" und "Benutzerverwaltung" tragen. Das Diagramm veranschaulicht, dass die drei Teilpakete als Unterpakete in dem übergeordneten Paket "Domain" zusammengefasst sind.

## Folie 33: Pakete für Raumbuchungssystem
Thema: Die Folie zeigt die Gliederung eines Raumbuchungssystems in UML-Pakete, wobei jedes Paket die zugehörigen Klassen mit ihren Attributen auflistet.
Inhalt: Der Titel lautet "Pakete für Raumbuchungssystem" und als Quelle wird [Larman] angegeben. Im Vergleich zur vorherigen Folie sind die drei Pakete hier nicht mehr in einem übergeordneten Paket "Domain" zusammengefasst, sondern stehen als eigenständige Ordner-Symbole nebeneinander. Neu ist, dass jedes Paket nun seine enthaltenen Klassen mit deren Attributen vollständig ausweist, statt nur die Paketnamen zu zeigen.
Abbildung: Ein UML-Paketdiagramm aus drei Ordner-Symbolen (Paketen), die jeweils Klassen (als kleine Kästen mit Namens- und Attributbereich) enthalten. Paket "Benutzerverwaltung" (oben links): enthält die Klasse "Benutzer" mit den Attributen "email" und "name" sowie die Klasse "Hausmeister" ohne aufgeführte Attribute. Paket "Raumverwaltung" (unten links): enthält die Klasse "Gebäude" mit den Attributen "adresse" und "oeffnungszeiten", die Klasse "Inventar" mit dem Attribut "defekt", die Klasse "Raum" mit den Attributen "kapazitaet", "raumnummer" und "raumtyp", sowie die Klassen "Beamer", "Tafel" und "Whiteboard" ohne aufgeführte Attribute. Paket "Buchungsverwaltung" (rechts, am größten): enthält die Klasse "Buchung" mit den Attributen "titel" und "beschreibung", die Klasse "Termin" mit dem Attribut "gebuchterZeitraum", die Klasse "Lehrveranstaltung" mit dem Attribut "name", die Klasse "Buchungswunsch" mit den Attributen "benoetigteDauer", "erlaubterZeitraum", "startDatum", "endDatum" und "periode", die Klasse "Raumwunsch" mit den Attributen "zulaessigeRaumtypen", "benoetigteKapazitaet" und "benoetigtesInventar", die Klasse "PeriodischeBuchung" mit dem Attribut "periode", sowie die Klassen … [gekürzt]

## Folie 34: SE-Prozess Artefakte: The Big Picture
Thema: Die Folie ordnet die zentralen Software-Engineering-Artefakte (Domänenmodell, Anwendungsfallmodell, Glossar) im Entwicklungsprozess ein und zeigt, wie sie miteinander zusammenhängen.
Inhalt: Der Titel lautet „SE-Prozess Artefakte: The Big Picture", gefolgt von der Leitfrage „Wo stehen wir im Entwicklungsprozess?". Die Folie gliedert die Artefakte in drei Bereiche: das „Domänenmodell", das „Anwendungsfallmodell" und das „Glossar". Das Anwendungsfallmodell besteht aus „Anwendungsfalldiagrammen" und „Anwendungsfalltexten"; ein Pfeil mit der Beschriftung „Anwendungsfallnamen" zeigt von den Diagrammen zu den Texten. Ein nach oben gerichteter Pfeil mit der Beschriftung „Domänen Konzepte" verbindet das Anwendungsfallmodell mit dem Domänenmodell, und ein nach unten rechts gerichteter Pfeil mit der Beschriftung „Begriffsdefinitionen" führt vom Domänenmodell zum Glossar. Das Glossar enthält eine Beispiel-Box mit dem Eintrag „Buchung:" sowie „Periode: ..." und weiteren Auslassungspunkten.
Abbildung: Zwei UML-Beispieldiagramme illustrieren die Artefakt-Gruppen: ein Klassendiagramm als Beispiel für das Domänenmodell und ein Use-Case-Diagramm als Beispiel für die Anwendungsfalldiagramme.

## Folie 35: Wo stehen wir im SE-Prozess?
Thema: Die Folie ordnet den aktuellen Stand im Software-Engineering-Prozess ein und erklärt, was nach der Kundenabstimmung mit dem Domänenmodell geschieht.
Inhalt: Der Titel lautet "Wo stehen wir im SE-Prozess?" mit dem Unterpunkt "Was machen wir mit dem Domänenmodell". Unter der Überschrift "Nach Absprache mit Kunden:" steht das Zitat „Haben wir die Domäne richtig verstanden?". Darauf folgen zwei mit Pfeilen markierte Aussagen: Erstens das "Freeze" des Domänenmodells. Zweitens, dass das Domänenmodell als "Grundlage" für "weitere Artefakte" dient.

## Folie 36: Zusammenfassung
Thema: Zusammenfassungsfolie zum Domänenmodell als wichtigem Bestandteil der Analyse, mit Hinweisen zur Notation und zur Identifikation von Konzepten.
Inhalt: Die Folie trägt den Titel "Zusammenfassung" und stellt fest, dass ein wichtiger Bestandteil der Analyse das Domänenmodell ist. In der linken Spalte wird unter der Überschrift "Notation mit UML Klassendiagrammen" aufgeführt: Es beschreibt statische Zusammenhänge; im Domänenmodell werden Konzepte zu Klassen; und es werden nur Attribute verwendet, keine Operationen. In der rechten Spalte wird unter der Überschrift "Identifikation von Konzepten" aufgeführt: Intuition/Erfahrung; existierende Modelle; und Kreativtechniken wie Nominalphrasen, Konzept-Kategorien-Listen und weitere. Darunter steht, dass Beziehungen zwischen Konzepten zu Assoziationen werden, und es werden "Need To Know"-Assoziationen genannt.
