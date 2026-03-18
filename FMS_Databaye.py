import sqlite3

# Verbindung zur Datenbank herstellen (erstellt die Datei, falls nicht vorhanden)
conn = sqlite3.connect('fussball_manager.db')
cursor = conn.cursor()

# Fremdschlüssel-Unterstützung in SQLite aktivieren
cursor.execute("PRAGMA foreign_keys = ON;")

# --- TABELLEN ERSTELLEN (Basierend auf dem Relationalen Modell im Bild) ---

# Tabelle: Liga
cursor.execute('''
CREATE TABLE IF NOT EXISTS Liga (
    Liga_id INTEGER PRIMARY KEY,
    Name VARCHAR(100),
    Land VARCHAR(80)
)
''')

# Tabelle: Verein
cursor.execute('''
CREATE TABLE IF NOT EXISTS Verein (
    Verein_id INTEGER PRIMARY KEY,
    Liga_id INTEGER,
    Name VARCHAR(100),
    Gründungsjahr DATE,
    Stadion_Kapazität INTEGER,
    Logo TEXT,
    FOREIGN KEY (Liga_id) REFERENCES Liga(Liga_id)
)
''')

# Tabelle: Spieler
cursor.execute('''
CREATE TABLE IF NOT EXISTS Spieler (
    Spieler_id INTEGER PRIMARY KEY,
    Spieler_Nummer INTEGER,
    Vorname VARCHAR(60),
    Nachname VARCHAR(60),
    Position VARCHAR(100),
    Marktwert FLOAT
)
''')

# Tabelle: Verein_Spieler (n:m Beziehungstabelle)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Verein_Spieler (
    Verein_Spieler_id INTEGER PRIMARY KEY,
    Verein_id INTEGER,
    Spieler_ID INTEGER,
    FOREIGN KEY (Verein_id) REFERENCES Verein(Verein_id),
    FOREIGN KEY (Spieler_id) REFERENCES Spieler(Spieler_id)
)
''')

# Tabelle: Match
cursor.execute('''
CREATE TABLE IF NOT EXISTS Match (
    Match_id INTEGER PRIMARY KEY,
    Datum DATE,
    Heimmannschaft VARCHAR(100),
    Auswärtsmannschaft VARCHAR(100),
    Tore_Heim INTEGER,
    Tore_Gast INTEGER
)
''')

# Tabelle: Spieler_Statistik
cursor.execute('''
CREATE TABLE IF NOT EXISTS Spieler_Statistik (
    STATS_id INTEGER PRIMARY KEY,
    Spieler_id INTEGER,
    Match_id INTEGER,
    Tore INTEGER,
    Gelbe_Karten INTEGER,
    Rote_Karten INTEGER,
    Rating FLOAT,
    FOREIGN KEY (Spieler_id) REFERENCES Spieler(Spieler_id),
    FOREIGN KEY (Match_id) REFERENCES Match(Match_id)
)
''')

# --- DATEN EINFÜGEN (Beispieldaten) ---

import sqlite3
import random

conn = sqlite3.connect('fussball_manager.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# --- DATEN LÖSCHEN (Um Duplikate bei Neustart zu vermeiden) ---
cursor.execute("DELETE FROM Spieler_Statistik")
cursor.execute("DELETE FROM Verein_Spieler")
cursor.execute("DELETE FROM Match")
cursor.execute("DELETE FROM Spieler")
cursor.execute("DELETE FROM Verein")
cursor.execute("DELETE FROM Liga")

# --- LIGEN & VEREINE ---
# --- LIGEN & VEREINE ---
cursor.executemany('INSERT INTO Liga VALUES (?,?,?)', [
    (1, 'Bundesliga', 'Deutschland'),
    (2, 'Premier League', 'England')
])

cursor.executemany('INSERT INTO Verein VALUES (?,?,?,?,?,?)', [
    (101, 1, 'FC Bayern München', '1900-02-27', 75000, 'https://logodetimes.com/times/bayern-munchen/bayern-munchen-4096.png'),
    (102, 1, 'Borussia Dortmund', '1909-12-19', 81365, 'https://logodetimes.com/times/borussia-dortmund/logo-borussia-dortmund-4096.png'),
    (103, 2, 'Manchester City', '1880-01-01', 53400, 'https://logos-world.net/wp-content/uploads/2020/06/Manchester-City-Logo-2016-present.jpg')
])

# --- SPIELER (Exakt 11 pro Team + De Bruyne) ---
cursor.executemany('INSERT INTO Spieler VALUES (?,?,?,?,?,?)', [
    (1, 1, 'Manuel', 'Neuer', 'Torwart', 3.0),
    (2, 2, 'Dayot', 'Upamecano', 'Abwehr', 45.0),
    (3, 3, 'Minjae', 'Kim', 'Abwehr', 45.0),
    (4, 19, 'Alphonso', 'Davies', 'Abwehr', 50.0),
    (5, 6, 'Joshua', 'Kimmich', 'Mittelfeld', 50.0),
    (6, 8, 'Leon', 'Goretzka', 'Mittelfeld', 30.0),
    (7, 42, 'Jamal', 'Musiala', 'Mittelfeld', 135.0),
    (8, 10, 'Leroy', 'Sane', 'Flügel', 60.0),
    (9, 11, 'Kingsley', 'Coman', 'Flügel', 40.0),
    (10, 7, 'Serge', 'Gnabry', 'Flügel', 35.0),
    (11, 9, 'Harry', 'Kane', 'Sturm', 100.0),
    (12, 1, 'Gregor', 'Kobel', 'Torwart', 40.0),
    (13, 4, 'Nico', 'Schlotterbeck', 'Abwehr', 40.0),
    (14, 25, 'Niklas', 'Süle', 'Abwehr', 15.0),
    (15, 26, 'Julian', 'Ryerson', 'Abwehr', 20.0),
    (16, 23, 'Emre', 'Can', 'Mittelfeld', 10.0),
    (17, 20, 'Marcel', 'Sabitzer', 'Mittelfeld', 20.0),
    (18, 10, 'Julian', 'Brandt', 'Mittelfeld', 40.0),
    (19, 21, 'Donyell', 'Malen', 'Flügel', 40.0),
    (20, 27, 'Karim', 'Adeyemi', 'Flügel', 28.0),
    (21, 43, 'Jamie', 'Gittens', 'Flügel', 35.0),
    (22, 9, 'Serhou', 'Guirassy', 'Sturm', 40.0),
    (23, 17, 'Kevin', 'De Bruyne', 'Mittelfeld', 60.0)
])

# --- VEREIN_SPIELER ZUWEISUNG (Komplett händisch ausgeschrieben) ---
cursor.executemany('INSERT INTO Verein_Spieler VALUES (?,?,?)', [
    (1, 101, 1), (2, 101, 2), (3, 101, 3), (4, 101, 4), (5, 101, 5),
    (6, 101, 6), (7, 101, 7), (8, 101, 8), (9, 101, 9), (10, 101, 10), (11, 101, 11),
    (12, 102, 12), (13, 102, 13), (14, 102, 14), (15, 102, 15), (16, 102, 16),
    (17, 102, 17), (18, 102, 18), (19, 102, 19), (20, 102, 20), (21, 102, 21), (22, 102, 22),
    (23, 103, 23)
])

# --- MATCHES ---
cursor.executemany('INSERT INTO Match VALUES (?,?,?,?,?,?)', [
    (501, '2025-08-24', 'FC Bayern München', 'VfL Wolfsburg', 3, 2),
    (502, '2025-08-31', 'Borussia Dortmund', 'Eintracht Frankfurt', 2, 0),
    (503, '2025-09-14', 'Holstein Kiel', 'FC Bayern München', 1, 6),
    (504, '2025-09-22', 'VfB Stuttgart', 'Borussia Dortmund', 5, 1),
    (505, '2025-09-28', 'FC Bayern München', 'Bayer Leverkusen', 1, 1),
    (506, '2025-10-05', 'Union Berlin', 'Borussia Dortmund', 2, 1),
    (507, '2025-11-30', 'Borussia Dortmund', 'FC Bayern München', 1, 2),
    (508, '2025-12-06', 'FC Bayern München', '1. FC Heidenheim', 3, 0),
    (509, '2025-11-05', 'Manchester City', 'FC Liverpool', 1, 1)
])

# --- STATISTIKEN (Händisch, keine Schleifen, keine Karten, abwechslungsreiche Ratings) ---
# Format: (STATS_id, Spieler_id, Match_id, Tore, Gelbe_Karten, Rote_Karten, Rating)
cursor.executemany('INSERT INTO Spieler_Statistik VALUES (?,?,?,?,?,?,?)', [
    # Match 501: Bayern (3) - Wolfsburg (2) | Tore: Kane(2), Musiala(1)
    (1, 1, 501, 0, 0, 0, 6.8),
    (2, 2, 501, 0, 0, 0, 6.5),
    (3, 3, 501, 0, 1, 0, 6.7),
    (4, 4, 501, 0, 0, 0, 7.1),
    (5, 5, 501, 0, 1, 0, 7.3),
    (6, 6, 501, 0, 0, 0, 7.0),
    (7, 7, 501, 1, 0, 0, 8.2),
    (8, 8, 501, 0, 0, 0, 6.9),
    (9, 9, 501, 0, 0, 0, 6.4),
    (10, 10, 501, 0, 0, 0, 6.6),
    (11, 11, 501, 2, 1, 0, 9.1),

    # Match 502: BVB (2) - Frankfurt (0) | Tore: Guirassy(1), Brandt(1)
    (12, 12, 502, 0, 0, 0, 7.5),
    (13, 13, 502, 0, 0, 0, 7.2),
    (14, 14, 502, 0, 0, 0, 7.0),
    (15, 15, 502, 0, 0, 0, 6.8),
    (16, 16, 502, 0, 1, 0, 7.1),
    (17, 17, 502, 0, 0, 0, 7.3),
    (18, 18, 502, 1, 0, 0, 8.4),
    (19, 19, 502, 0, 0, 0, 6.9),
    (20, 20, 502, 0, 1, 0, 6.7),
    (21, 21, 502, 0, 0, 0, 7.4),
    (22, 22, 502, 1, 0, 0, 8.5),

    # Match 503: Kiel (1) - Bayern (6) | Tore: Kane(3), Sane(1), Gnabry(1), Kimmich(1)
    (23, 1, 503, 0, 0, 0, 7.0),
    (24, 2, 503, 0, 0, 0, 7.2),
    (25, 3, 503, 0, 0, 0, 7.4),
    (26, 4, 503, 0, 0, 0, 7.7),
    (27, 5, 503, 1, 0, 0, 8.6),
    (28, 6, 503, 0, 0, 0, 7.5),
    (29, 7, 503, 0, 1, 0, 7.8),
    (30, 8, 503, 1, 0, 0, 8.8),
    (31, 9, 503, 0, 0, 0, 7.1),
    (32, 10, 503, 1,1, 0, 8.5),
    (33, 11, 503, 3, 0, 0, 9.8),

    # Match 504: Stuttgart (5) - BVB (1) | Tore: Malen(1)
    (34, 12, 504, 0, 0, 0, 5.0),
    (35, 13, 504, 1, 0, 0, 4.5),
    (36, 14, 504, 1, 2, 1, 4.8),
    (37, 15, 504, 1, 0, 0, 5.2),
    (38, 16, 504, 0, 0, 0, 5.5),
    (39, 17, 504, 0, 0, 0, 5.3),
    (40, 18, 504, 0, 0, 0, 6.0),
    (41, 19, 504, 1, 0, 0, 7.2),
    (42, 20, 504, 1, 0, 0, 5.8),
    (43, 21, 504, 0, 0, 0, 6.1),
    (44, 22, 504, 0, 0, 1, 5.9),

    # Match 505: Bayern (1) - Leverkusen (1) | Tore: Musiala(1)
    (45, 1, 505, 0, 0, 0, 7.2),
    (46, 2, 505, 0, 0, 0, 6.8),
    (47, 3, 505, 0, 0, 0, 6.9),
    (48, 4, 505, 0, 0, 0, 7.4),
    (49, 5, 505, 0, 0, 0, 7.1),
    (50, 6, 505, 0, 0, 0, 6.7),
    (51, 7, 505, 1, 0, 0, 8.0),
    (52, 8, 505, 0, 1, 0, 6.5),
    (53, 9, 505, 0, 0, 0, 6.6),
    (54, 10, 505, 0, 0, 0, 6.3),
    (55, 11, 505, 0, 0, 0, 6.8),

    # Match 506: Union (2) - BVB (1) | Tore: Adeyemi(1)
    (56, 12, 506, 0, 0, 0, 6.1),
    (57, 13, 506, 0, 1, 0, 6.0),
    (58, 14, 506, 0, 1, 0, 5.8),
    (59, 15, 506, 0, 0, 0, 6.2),
    (60, 16, 506, 0, 0, 0, 6.5),
    (61, 17, 506, 0, 0, 0, 6.3),
    (62, 18, 506, 0, 0, 0, 6.7),
    (63, 19, 506, 0, 0, 0, 6.4),
    (64, 20, 506, 1, 0, 0, 7.6),
    (65, 21, 506, 0, 0, 0, 6.2),
    (66, 22, 506, 0, 0, 0, 6.5),

    # Match 507: BVB (1) - Bayern (2) | Tore: Guirassy(1), Sane(1), Kane(1)
    (67, 12, 507, 0, 0, 0, 6.5),
    (68, 13, 507, 1, 0, 0, 6.2),
    (69, 14, 507, 1, 0, 0, 6.4),
    (70, 15, 507, 0, 0, 0, 6.1),
    (71, 16, 507, 0, 0, 0, 6.7),
    (72, 17, 507, 1, 0, 0, 6.8),
    (73, 18, 507, 0, 0, 0, 7.0),
    (74, 19, 507, 0, 0, 0, 6.3),
    (75, 20, 507, 0, 0, 0, 6.6),
    (76, 21, 507, 1, 0, 0, 6.9),
    (77, 22, 507, 1, 0, 0, 7.8),
    (78, 1, 507, 0, 0, 0, 7.4),
    (79, 2, 507, 0, 0, 0, 7.1),
    (80, 3, 507, 0, 0, 0, 7.5),
    (81, 4, 507, 0, 1, 0, 7.3),
    (82, 5, 507, 0, 0, 0, 7.6),
    (83, 6, 507, 0, 0, 0, 7.2),
    (84, 7, 507, 0, 0, 0, 7.9),
    (85, 8, 507, 1, 0, 0, 8.2),
    (86, 9, 507, 0, 0, 0, 7.0),
    (87, 10, 507, 0, 0, 0, 6.8),
    (88, 11, 507, 1, 0, 0, 8.5),

    # Match 508: Bayern (3) - Heidenheim (0) | Tore: Kane(1), Musiala(1), Coman(1)
    (89, 1, 508, 0, 1, 0, 7.8),
    (90, 2, 508, 0, 1, 0, 7.5),
    (91, 3, 508, 0, 0, 0, 7.6),
    (92, 4, 508, 0, 0, 0, 7.9),
    (93, 5, 508, 0, 0, 0, 8.1),
    (94, 6, 508, 0, 0, 0, 7.4),
    (95, 7, 508, 1, 1, 0, 8.6),
    (96, 8, 508, 0, 0, 0, 7.3),
    (97, 9, 508, 1, 0, 0, 8.3),
    (98, 10, 508, 0, 1, 0, 7.2),
    (99, 11, 508, 1, 0, 0, 8.4),

    # Match 509: Man City (1) - Liverpool (1) | Tore: De Bruyne(1)
    (100, 23, 509, 1, 1, 0, 8.8)
])

conn.commit()
conn.close()

print("Fertig! Exakt 100 Statistik-Zeilen wurden händisch und ohne Schleifen in die Datenbank geschrieben.")
