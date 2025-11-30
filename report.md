# Rapport: The Ocean Cleanup Challenge

**Team:** [Jouw Naam / Teamnaam]  
**Datum:** 19 november 2025  
**Onderwerp:** Optimalisatie van plasticverzameling met behulp van Beam Search

## 1. Inleiding
In deze challenge is het doel om een optimale route te vinden voor een schoonmaakschip om in vijf dagen zoveel mogelijk plastic te verzamelen uit de oceaan. Het probleem is gemodelleerd als een raster van 20 bij 30 cellen, waarbij elke cel een bepaalde hoeveelheid plastic bevat. Gegeven de complexe regels omtrent beweging, dagelijkse afstanden en randvoorwaarden, is dit een combinatorisch optimalisatieprobleem.

## 2. Methode: Beam Search Algoritme

Om dit vraagstuk op te lossen, hebben we gekozen voor een **Beam Search** algoritme. Een volledige zoektocht (brute-force) is computationeel niet haalbaar gezien de exponentiële groei van het aantal mogelijke routes over vijf dagen. Beam Search biedt een efficiënte heuristische benadering die de zoekruimte beperkt houdt zonder in eenvoudige lokale optima te blijven hangen.

### 2.1 Aanpak
Het algoritme bouwt de route stap voor stap op door de "toestand" van het schip bij te houden. Een toestand wordt gedefinieerd door:
*   De huidige positie (rij, kolom).
*   De huidige richting (N, NO, O, ZO, Z, ZW, W, NW).
*   De huidige dag (1 t/m 5) en de afgelegde afstand op die dag.
*   Een set van reeds bezochte cellen (om dubbeltellingen te voorkomen).
*   De totaal verzamelde score aan plastic.

### 2.2 Het Proces
Het algoritme verloopt iteratief:
1.  **Expansie:** Bij elke stap genereren we vanuit de huidige verzameling kandidaten (de "beam") alle mogelijke vervolgstappen. Het schip kan rechtdoor gaan (0), 45° naar rechts draaien (1) of 45° naar links draaien (-1).
2.  **Validatie:** Elke mogelijke stap wordt direct getoetst aan de spelregels:
    *   **Grenzen:** Het schip mag het 20x30 raster niet verlaten.
    *   **Afstand:** De dagelijkse limiet van 50 km mag niet worden overschreden (5 km voor orthogonale stappen, 7 km voor diagonale).
    *   **Randvoorwaarde:** Op dag 1 t/m 4 mag het schip de dag niet eindigen op de rand van het raster. Op dag 5 mag dit wel.
3.  **Selectie (Pruning):** Na expansie sorteren we alle geldige nieuwe routes op basis van de totaal verzamelde hoeveelheid plastic. Alleen de beste 500 routes worden behouden voor de volgende iteratie (de "beam width").

Door een brede beam width van 500 te hanteren, kan het algoritme ver vooruitkijken en strategische keuzes maken die op korte termijn misschien minder opleveren, maar op lange termijn leiden tot rijkere plasticgebieden.

## 3. Resultaten

Met deze methode hebben we een route gevonden die resulteert in een totale plasticopbrengst van **391**.

### De Oplossing (Rotatiecodes)
Hieronder staan de bewegingscodes per dag, klaar voor indiening:

```text
1 0 1 0 1 0 1 0
1 -1 0 0 1 0 0 0
1 1 1 1 0 -1 -1 1
-1 -1 -1 -1 0 0 0 0 0
0 0 1 1 1 1 0 0 0
```

### Validatie
De oplossing voldoet aan alle gestelde eisen:
*   Startpositie is T11 in oostelijke richting.
*   De maximale afstand per dag wordt nergens overschreden.
*   Het schip blijft binnen de grenzen en eindigt de eerste vier dagen niet op de rand.

## 4. Conclusie
Door het probleem te benaderen als een graafzoekprobleem en Beam Search toe te passen, konden we efficiënt navigeren door de enorme hoeveelheid mogelijke routes. De gekozen strategie maximaliseert de score door continu de meest veelbelovende paden parallel te verkennen.

