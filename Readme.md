## Geschäftsproblem
Ein E-Commerce-Unternehmen möchte seine Kunden besser verstehen und gezielte Marketingstrategien entwickeln.  
Ziel dieses Projekts ist es, Kunden anhand ihres Kaufverhaltens in sinnvolle Segmente zu unterteilen, um personalisierte Marketingmaßnahmen und kundenorientierte Kampagnen zu ermöglichen.

Hierfür wird eine **RFM-Analyse (Recency, Frequency, Monetary)** eingesetzt, um das Kaufverhalten datengetrieben zu bewerten und Kunden systematisch zu klassifizieren.

---

## Datensatzbeschreibung
Der verwendete Datensatz **Online Retail II** enthält Transaktionsdaten eines in Großbritannien ansässigen Online-Händlers aus dem Zeitraum **01.12.2009 bis 09.12.2011**.

Der Datensatz umfasst detaillierte Informationen zu Rechnungen, Produkten, Kunden und Verkaufszeitpunkten und eignet sich besonders für Kundenanalysen im E-Commerce-Kontext.

### Wichtige Variablen
- **InvoiceNo**: Rechnungsnummer (mit „C“ gekennzeichnete Rechnungen sind Stornierungen)
- **StockCode / Description**: Produktkennzeichnung und Produktbeschreibung
- **Quantity**: Anzahl der verkauften Produkte
- **UnitPrice**: Preis pro Produkt
- **InvoiceDate**: Datum und Uhrzeit des Kaufs
- **CustomerID**: Eindeutige Kundennummer
- **Country**: Land des Kunden

---

## Durchgeführte Schritte
### 1. Datenvorbereitung
- Zusammenführung der Datensätze aus den Jahren 2009–2010 und 2010–2011  
- Entfernen von Stornierungen und Rückgaben  
- Ausschluss negativer Verkaufszahlen  
- Behandlung fehlender Werte  
- Erstellung der Variable **TotalPrice** (Quantity × UnitPrice)

### 2. Explorative Datenanalyse (EDA)
- Analyse numerischer und kategorialer Variablen  
- Untersuchung von Verteilungen und Korrelationen  
- Analyse von Verkaufsentwicklungen nach:
  - Kunden
  - Produkten
  - Ländern
  - Jahren, Monaten, Tagen und Stunden  

### 3. RFM-Analyse
- **Recency**: Anzahl der Tage seit dem letzten Kauf  
- **Frequency**: Anzahl der getätigten Rechnungen  
- **Monetary**: Gesamtausgaben eines Kunden  
- Vergabe von RFM-Scores mittels Quantilen  
- Segmentierung der Kunden in Kategorien wie:
  - Champions  
  - Loyal Customers  
  - Potential Loyalists  
  - New Customers  
  - At Risk  
  - Can’t Lose Them  
  - Hibernating  

---

## Ergebnisse und Erkenntnisse
- Kunden konnten erfolgreich in mehrere **verhaltensbasierte Segmente** eingeteilt werden  
- Ein kleiner Teil der Kunden generiert einen großen Anteil des Umsatzes  
- Bestimmte Zeiträume (Monate, Wochentage, Uhrzeiten) zeigen deutlich höhere Verkaufsaktivitäten  
- RFM-Segmentierung ermöglicht eine klare Priorisierung von Marketingmaßnahmen  

### Beispielhafte Marketing-Implikationen
- **Champions**: Exklusive Angebote, frühzeitiger Zugang zu neuen Produkten  
- **Potential Loyalists**: Personalisierte Empfehlungen und Loyalty-Programme  
- **At Risk / Can’t Lose Them**: Reaktivierungskampagnen und gezielte Rabatte  
- **New Customers**: Willkommensangebote und Onboarding-Kampagnen  

---

## Fazit
Die RFM-Analyse erweist sich als effektive Methode zur Kundensegmentierung im E-Commerce.  
Durch die Kombination aus Datenbereinigung, explorativer Analyse und Segmentierung lassen sich **praxisnahe und umsetzbare Erkenntnisse** für datengetriebene Marketingstrategien gewinnen.
