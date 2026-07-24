import random
import os

# --- Hebrew Data ---
he_first_names = ["דוד", "משה", "יעקב", "יצחק", "אברהם", "רחל", "שרה", "רבקה", "לאה", "מיכל", "יעל", "נועה", "תמר", "אבי", "יוסי", "חיים", "רועי", "דניאל", "עומר", "עידו"]
he_last_names = ["כהן", "לוי", "מזרחי", "פרץ", "ביטון", "דהן", "אגמון", "פרידמן", "מלכה", "אזולאי", "כץ", "יוסף", "דוד", "עמר", "אוחיון", "חדד", "גבאי", "בן דוד", "קדם", "אשכנזי"]
he_cities = ["תל אביב", "ירושלים", "חיפה", "ראשון לציון", "פתח תקווה", "אשדוד", "נתניה", "באר שבע", "חולון", "בני ברק"]
he_streets = ["הרצל", "דיזנגוף", "בן יהודה", "אלנבי", "הירקון", "זבוטינסקי", "העצמאות", "רוטשילד", "אבן גבירול", "הנשיא"]

# --- English Data ---
en_first_names = ["John", "Michael", "David", "James", "Robert", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "William", "Richard", "Joseph", "Thomas", "Charles"]
en_last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
en_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
en_streets = ["Main St", "High St", "Park Ave", "Oak St", "Pine St", "Maple Ave", "Cedar Ln", "Elm St", "Washington St", "Lake St"]

# --- German Data ---
de_first_names = ["Lukas", "Leon", "Maximilian", "Paul", "Felix", "Emma", "Mia", "Hannah", "Emilia", "Sofia", "Jonas", "Klaus", "Hans", "Julia", "Anna"]
de_last_names = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann", "Koch", "Bauer", "Richter", "Klein", "Wolf"]
de_cities = ["Berlin", "München", "Hamburg", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf", "Leipzig", "Dortmund", "Essen"]
de_streets = ["Hauptstraße", "Schulstraße", "Gartenstraße", "Bahnhofstraße", "Dorfstraße", "Goethestraße", "Schillerstraße", "Lindenstraße", "Berliner Straße", "Ringstraße"]

# --- Spanish Data ---
es_first_names = ["José", "Antonio", "Manuel", "Francisco", "David", "Juan", "Javier", "Carlos", "Miguel", "Rafael", "María", "Carmen", "Ana", "Isabel", "Laura", "Marta", "Lucía", "Elena", "Sara", "Paula"]
es_last_names = ["García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno"]
es_cities = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia", "Palma", "Bilbao", "Alicante"]
es_streets = ["Calle Mayor", "Gran Vía", "Calle Alcalá", "Paseo de la Castellana", "Calle Serrano", "Avenida Diagonal", "Calle Toledo", "Rambla de Catalunya", "Calle Princesa", "Paseo del Prado"]

# --- French Data ---
fr_first_names = ["Jean", "Pierre", "Michel", "Philippe", "Alain", "Nicolas", "Julien", "Thomas", "Marie", "Nathalie", "Isabelle", "Sophie", "Catherine", "Camille", "Julie", "Claire", "Lucas", "Hugo", "Léa", "Emma"]
fr_last_names = ["Martin", "Bernard", "Dubois", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "Garnier", "Rousseau"]
fr_cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"]
fr_streets = ["rue de la Paix", "avenue des Champs-Élysées", "rue Victor Hugo", "boulevard Saint-Germain", "rue de Rivoli", "avenue de la République", "rue Nationale", "place de la Bastille", "rue du Commerce", "boulevard Voltaire"]

# --- Italian Data ---
it_first_names = ["Luca", "Giulia", "Marco", "Sofia", "Alessandro", "Aurora", "Lorenzo", "Martina", "Matteo", "Chiara", "Andrea", "Francesca", "Davide", "Alice", "Simone", "Elena", "Federico", "Sara", "Giovanni", "Valentina"]
it_last_names = ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca", "Mancini"]
it_cities = ["Roma", "Milano", "Napoli", "Torino", "Palermo", "Genova", "Bologna", "Firenze", "Bari", "Venezia"]
it_streets = ["Via Roma", "Corso Italia", "Via Garibaldi", "Piazza Dante", "Via Verdi", "Viale Europa", "Via Manzoni", "Corso Vittorio Emanuele", "Via Nazionale", "Via Milano"]

# --- Generators ---
# NOTE (2026-07-24): the es/fr/it national IDs and IBANs are generated
# checksum-VALID on purpose. A checksum-validating engine correctly refuses
# invalid look-alikes, so invalid "IDs" in test data produce false leak flags
# in residual scans (observed with the he Teudat-Zehut values in this dataset).

def _es_dni():
    n = random.randint(10000000, 99999999)
    return f"{n}{'TRWAGMYFPDXBNJZSQVHLCKE'[n % 23]}"

def _fr_insee():
    body = (f"{random.choice([1, 2])}{random.randint(50, 99)}{random.randint(1, 12):02d}"
            f"{random.randint(1, 95):02d}{random.randint(1, 990):03d}{random.randint(1, 999):03d}")
    key = 97 - int(body) % 97
    return f"{body}{key:02d}"

def _it_cf():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ("".join(random.choice(letters) for _ in range(6))
            + f"{random.randint(50, 99)}" + random.choice("ABCDEHLMPRST")
            + f"{random.randint(1, 28):02d}" + random.choice(letters)
            + f"{random.randint(100, 999)}" + random.choice(letters))

def _iban_checked(country, bban):
    num = "".join(str(int(c, 36)) for c in (bban + country + "00"))
    return f"{country}{98 - int(num) % 97:02d}{bban}"

def gen_id(lang):
    if lang == "he": return "".join([str(random.randint(0, 9)) for _ in range(9)])
    elif lang == "en": return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
    elif lang == "de": return f"T{random.randint(10000000, 99999999)}"
    elif lang == "es": return _es_dni()
    elif lang == "fr": return _fr_insee()
    elif lang == "it": return _it_cf()

def gen_phone(lang):
    if lang == "he": return random.choice([f"05{random.randint(0, 9)}-{random.randint(1000000, 9999999)}", f"05{random.randint(0, 9)} {random.randint(100,999)} {random.randint(1000,9999)}"])
    elif lang == "en": return random.choice([f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}", f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"])
    elif lang == "de": return random.choice([f"+49 151 {random.randint(1000000, 9999999)}", f"0151 {random.randint(1000000, 9999999)}"])
    elif lang == "es": return random.choice([f"+34 6{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)}", f"6{random.randint(10000000, 99999999)}"])
    elif lang == "fr": return random.choice([f"+33 6 {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}", f"06 {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"])
    elif lang == "it": return random.choice([f"+39 3{random.randint(20, 99)} {random.randint(1000000, 9999999)}", f"3{random.randint(20, 99)} {random.randint(1000000, 9999999)}"])

def gen_part_num(): return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
def gen_part_num_he(): return "".join([str(random.randint(0, 9)) for _ in range(9)])
def gen_dob(): return f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1950, 2010)}"
def gen_ip(): return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
def gen_mac(): return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
def gen_iban(lang):
    if lang == "es":
        return _iban_checked("ES", f"{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(10, 99)}{random.randint(0, 9999999999):010d}")
    if lang == "fr":
        return _iban_checked("FR", f"{random.randint(10000, 99999)}{random.randint(10000, 99999)}{random.randint(0, 99999999999):011d}{random.randint(10, 99)}")
    if lang == "it":
        return _iban_checked("IT", random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + f"{random.randint(10000, 99999)}{random.randint(10000, 99999)}{random.randint(0, 999999999999):012d}")
    prefix = "IL" if lang == "he" else "DE" if lang == "de" else "US"
    return f"{prefix}{random.randint(10, 99)}{random.randint(100, 999)}{random.randint(100000, 999999)}{random.randint(10, 99)}"

# --- Edge Cases (Multi-line, emojis, HTML/URL, punctuation hugging) ---
he_edge_cases = [
    "פרטי התקשרות:\nשם: {first} {last}\nטלפון: {phone}\nת\"ז: {id}", # Multi-line
    "נא לחזור אלי לטלפון 📞{phone} או למייל {first}.{last}@example.com 📧.", # Emojis
    "<div>שם הלקוח: <strong>{first} {last}</strong></div><p>מספר מזהה: <span>{id}</span></p>", # HTML wrapped
    "https://api.example.com/update?user={first}%20{last}&tz={id}&phone={phone}", # URL encoded
    "[{first} {last}], ({id}), '{phone}' - פרטים שעודכנו הרגע במערכת.", # Punctuation hugging
    "העובד\t{first} {last}\tעם המספר\t{id}\tמבקש אישור.", # Tabs
    "שם: {FIRST} {LAST}!!! מספר: {ID}???", # UPPERCASE and punctuation
]

en_edge_cases = [
    "Contact Info:\nName: {first} {last}\nPhone: {phone}\nSSN: {id}", # Multi-line
    "Please call me back at 📞{phone} or email {first}.{last}@example.com 📧.", # Emojis
    "<div>Customer Name: <strong>{first} {last}</strong></div><p>Identifier: <span>{id}</span></p>", # HTML wrapped
    "https://api.example.com/update?user={first}%20{last}&ssn={id}&phone={phone}", # URL encoded
    "[{first} {last}], ({id}), '{phone}' - details just updated in the system.", # Punctuation hugging
    "Employee\t{first} {last}\twith SSN\t{id}\trequests approval.", # Tabs
    "NAME: {FIRST} {LAST}!!! NUMBER: {ID}???", # UPPERCASE and punctuation
]

de_edge_cases = [
    "Kontaktinfo:\nName: {first} {last}\nTelefon: {phone}\nAusweis: {id}", # Multi-line
    "Bitte rufen Sie mich zurück unter 📞{phone} oder per E-Mail an {first}.{last}@example.de 📧.", # Emojis
    "<div>Kundenname: <strong>{first} {last}</strong></div><p>Kennung: <span>{id}</span></p>", # HTML wrapped
    "https://api.example.de/update?user={first}%20{last}&id={id}&phone={phone}", # URL encoded
    "[{first} {last}], ({id}), '{phone}' - Details soeben im System aktualisiert.", # Punctuation hugging
    "Mitarbeiter\t{first} {last}\tmit Ausweis\t{id}\tbittet um Freigabe.", # Tabs
    "NAME: {FIRST} {LAST}!!! NUMMER: {ID}???", # UPPERCASE and punctuation
]


# --- Hebrew Templates ---
he_implicit = [
    "דיברתי עם {first} {last} והוא אמר שנעביר את זה ל-{city}. אמר שאפשר להתקשר ל-{phone}.",
    "תמסור ל-{first} את המספר {id} כדי שיוכל להיכנס לבניין.",
    "היי, הנה מה שביקשת: {first} {last}, {id}, {phone}, {dob}. נדבר מחר.",
    "העברתי את התיק לטיפולו של {first} {last}. אפשר להשיג אותו ב-{phone} או במשרד ב-{city}.",
    "פגשתי את {first} ליד {street} {num}. הוא ביקש שאשלח לו הודעה ל-{phone}.",
    "הקוד המזהה שלו במערכת הוא {id}. נא לא להעביר ל-{first2}.",
    "נפגשנו ב-{city} עם {first}. {phone} לתיאום."
]

he_templates = [
    "פוליסת ביטוח חיים של {first} {last}, ת\"ז {id}. מתגורר ברחוב {street} {num}, {city}. טלפון: {phone}. תאריך לידה: {dob}.",
    "הודעה על תאונת דרכים. הנהג הפוגע: {first} {last}, ת\"ז {id}, תושב {city}. רכב מ.רישוי {num}{num}{num}.",
    "מבוטח {first} {last} פנה אלינו לקבלת הצעת מחיר לביטוח רכב. רכב מאזדה 3. תעודת זהות: {id}.",
    "לקוח {first} {last}, אימייל {first}.{last}@example.co.il ביצע העברה בנקאית מכתובת IP {ip}.",
    "מטופל בשם {first} {last}, הגיע למרפאה. מספר ת\"ז: {id}. דופק: 80, לחץ דם: 120/80.",
    "התובע {first} {last} הגיש תביעה נגד חברת ביטוח. מספר תיק: {num}{num}-{num}.",
    "פסק דין בת\"א {num} - {first} {last} נגד בנק הפועלים. הוחלט כי הנתבע ישלם לתובע סך של 50,000 ש\"ח.",
    "כרטיס אשראי מסתיים ב-{num}{num} נשלח לכתובת {street} {num}, {city} עבור {first} {last}.",
    "סיכום אשפוז - החולה {first} {last} שוחרר לביתו. כתובת למכתב שחרור: {street} {num} {city}.",
    "מרשם לתרופות כרוניות נמסר למטופלת {first} {last} בעלת תעודת זהות {id}.",
    "על פי תקנון החברה, העישון מותר בפינות המיועדות לכך בלבד.",
    "חוק הגנת הצרכן מחייב עסקים להציג מחירים כולל מע\"מ. אי עמידה בחוק תגרור קנס.",
    "הזמנו ציוד שמחה לאירוע של החברה בסוף השנה.", 
    "צריך להביא יותר אור לחדר הישיבות.", 
    "התקבל משלוח מסין, מק\"ט המוצר הוא {part_he} במערכת המלאי.", 
    "מחר צפוי מזג אוויר סוער ברחבי הארץ. יש להימנע מנסיעות.",
    "The customer {en_first} {en_last} called about his account. He lives in {en_city}.",
    "פרויקט Alpha הובל על ידי {en_first} {en_last} מהסניף שלנו ב-{en_city}.",
    "כתובת ה-MAC של המחשב של {first} היא {mac} והוא מתחבר דרך {ip}.",
    "העברה של {num},000 דולר לחשבון IBAN {iban} בוצעה על ידי {first}."
]

# --- English Templates ---
en_implicit = [
    "I left the package with {first} {last} at {num} {street}. Call {phone} if there are issues.",
    "Here is the code you need: {id}. Don't share it with {first}.",
    "Hey, the details are: {first} {last}, {id}, {dob}. Thanks.",
    "I talked to {first} today. He said to forward it to {city} and reach him at {phone}.",
    "Please send the documents to {first} {last}, {num} {street}, {city}.",
    "Met up with {first} near {num} {street}. Reached out to {first2} at {phone}."
]

en_templates = [
    "Life insurance policy for {first} {last}, SSN {id}. Resides at {num} {street}, {city}. Phone: {phone}. DOB: {dob}.",
    "Car accident report. At-fault driver: {first} {last}, License Plate {num}XYZ{num}. Driver lives in {city}.",
    "Client {first} {last} requested a quote for comprehensive auto insurance. SSN: {id}. Phone: {phone}.",
    "Client {first} {last}, email {first}.{last}@example.com initiated a wire transfer from IP {ip}.",
    "Patient {first} {last} arrived at the clinic. SSN: {id}. Heart rate: 80, Blood pressure: 120/80.",
    "Plaintiff {first} {last} filed a lawsuit against StateFarm for personal injury. Case ID: {num}{num}-{num}.",
    "Court ruling in case {num} - {first} {last} vs. Bank of America. Defendant ordered to pay $50,000.",
    "New credit card ending in {num}{num} was mailed to {num} {street}, {city} for {first} {last}.",
    "Discharge summary - Patient {first} {last} was discharged. Send documents to: {num} {street} {city}.",
    "Prescription for chronic medication handed to patient {first} {last}, SSN {id}.",
    "According to company policy, smoking is allowed only in designated areas.",
    "The consumer protection act requires businesses to display prices including tax.",
    "The grace period ends in May.", 
    "Our hope is to finish the project on time and within budget.", 
    "Part number {part_en} is currently out of stock.", 
    "Severe weather expected tomorrow across the state. Please avoid non-essential travel.",
    "Project Alpha was led by {first} {last} from our {city} branch.",
    "{first}'s device MAC address is {mac} connecting from IP {ip}.",
    "Wire transfer to IBAN {iban} was initiated by {first}."
]

# --- German Templates ---
de_implicit = [
    "Ich habe das Paket bei {first} {last} in der {street} {num} hinterlassen. Rufen Sie {phone} an, wenn es Probleme gibt.",
    "Hier ist der Code, den Sie brauchen: {id}. Teilen Sie ihn nicht mit {first}.",
    "Hey, die Details sind: {first} {last}, {id}, {dob}. Danke.",
    "Ich habe heute mit {first} gesprochen. Er sagte, wir sollen es nach {city} weiterleiten und ihn unter {phone} erreichen.",
    "Bitte senden Sie die Dokumente an {first} {last}, {street} {num}, {city}.",
    "Habe mich mit {first} in der Nähe der {street} {num} getroffen. Habe {first2} unter {phone} erreicht."
]

de_templates = [
    "Lebensversicherungspolice für {first} {last}, Ausweisnummer {id}. Wohnhaft in der {street} {num}, {city}. Telefon: {phone}. Geburtsdatum: {dob}.",
    "Unfallbericht. Verursacher: {first} {last}, Kennzeichen {num}XYZ{num}. Wohnhaft in {city}.",
    "Kunde {first} {last} hat ein Angebot für eine Kfz-Versicherung angefordert. Ausweisnummer: {id}. Telefon: {phone}.",
    "Kunde {first} {last}, E-Mail {first}.{last}@example.de, hat eine Überweisung von der IP-Adresse {ip} veranlasst.",
    "Patient {first} {last} ist in der Klinik eingetroffen. Ausweisnummer: {id}. Puls: 80, Blutdruck: 120/80.",
    "Kläger {first} {last} hat eine Klage gegen die Allianz wegen Personenschadens eingereicht. Aktenzeichen: {num}{num}-{num}.",
    "Gerichtsurteil im Fall {num} - {first} {last} gegen die Deutsche Bank. Der Beklagte wird zur Zahlung von 50.000 € verurteilt.",
    "Neue Kreditkarte mit der Endziffer {num}{num} wurde an {street} {num}, {city} für {first} {last} gesendet.",
    "Entlassungsbericht - Patient {first} {last} wurde entlassen. Dokumente senden an: {street} {num}, {city}.",
    "Rezept für chronische Medikamente an Patient {first} {last}, Ausweisnummer {id}, ausgehändigt.",
    "Laut Unternehmensrichtlinie ist das Rauchen nur in den dafür vorgesehenen Bereichen gestattet.",
    "Das Verbraucherschutzgesetz verlangt von Unternehmen, Preise inklusive Steuern anzugeben.",
    "Die Schonfrist endet im Mai.",
    "Unsere Hoffnung ist es, das Projekt pünktlich abzuschließen.",
    "Die Teilenummer {part_en} ist derzeit nicht auf Lager.",
    "Schweres Wetter morgen im ganzen Land erwartet. Bitte vermeiden Sie nicht zwingend notwendige Fahrten.",
    "Die MAC-Adresse des Geräts von {first} lautet {mac} und ist über die IP {ip} verbunden.",
    "Eine Überweisung auf die IBAN {iban} wurde von {en_first} veranlasst."
]

# --- Longform / Real-World Internet Texts (Needle in a Haystack) ---
he_longform = [
    "הואיל והמשכיר הינו הבעלים הרשום והמחזיק הבלעדי של דירת המגורים המצויה ברחוב {street} {num} בעיר {city}; והואיל והשוכר {first} {last}, בעל תעודת זהות {id}, מעוניין לשכור את הדירה לתקופה של 12 חודשים; לפיכך הוסכם בין הצדדים כדלקמן: דמי השכירות יעמדו על סך 5,000 ש\"ח בחודש. לבירורים ניתן ליצור קשר בטלפון {phone}.",
    "סוכרת סוג 2 היא מחלה מטבולית המתאפיינת בריכוז גבוה של גלוקוז בדם. בבדיקה שגרתית שנערכה במרפאת {city}, המטופל {first} {last} (ת\"ז: {id}) הציג מדדים חריגים. המטופל, אשר מתגורר ברחוב {street}, עודכן בתוצאות ויקבל הפניה במייל. לפרטים נוספים: {phone}.",
    "תקנון האתר ותנאי שימוש: ברוכים הבאים לאתר הסחר האלקטרוני. כל המבצע פעולת רכישה באתר מצהיר כי קרא את התקנון. במידה והלקוח {first} {last} יבצע רכישה, הקבלה תשלח לכתובת ה-IP המזוהה ({ip}). ניתן לשלם באמצעות העברה בנקאית לחשבון {iban}. בכל בעיה טכנית, נציגנו יצרו קשר במספר {phone}.",
    "פוליסת ביטוח מקיף לרכב: הפוליסה מכסה נזק תאונתי, גניבה ושריפה בהתאם לתנאים הכלליים המפורטים בחוברת הפוליסה. מבוטח הרשום בפוליסה, {first} {last} (מספר זהות: {id}), רשאי להגיש תביעה בקרות מקרה ביטוח. הרכב המבוטח רשום בכתובת {street} {num}, {city}. בכל מקרה של תביעה, יש לפנות למוקד שירות הלקוחות במספר {phone}."
]

en_longform = [
    "According to the Centers for Disease Control and Prevention (CDC), Type 2 diabetes is a chronic condition that affects the way the body processes blood sugar. During a routine checkup at our {city} facility, patient {first} {last} (SSN: {id}) exhibited elevated HbA1c levels. The patient, who resides at {num} {street}, was advised to begin a modified diet and can be reached at {phone}.",
    "TERMS OF SERVICE: This Agreement is a legal document between you and the Company. By accessing the service from IP address {ip}, you agree to be bound by these terms. If the user {first} {last} violates section 3.4, the account associated with SSN {id} will be suspended pending investigation. Direct inquiries to our legal team or call {phone}.",
    "Historical records indicate that the town of {city} was founded in the late 19th century. Local archives contain a deed belonging to {first} {last}, transferring the property located at {num} {street}. The modern descendant can be contacted at {phone} or via bank transfer to IBAN {iban} for historical foundation donations.",
    "Comprehensive Auto Insurance Policy Document: This policy provides coverage for accidental damage, theft, and fire, subject to the exclusions and conditions outlined in Section IV. The primary policyholder, {first} {last} (SSN: {id}), is authorized to file a claim. The insured vehicle is garaged at {num} {street}, {city}. In the event of a claim, contact your designated agent at {phone}."
]

de_longform = [
    "Allgemeine Geschäftsbedingungen der Bank. § 1 Geltungsbereich: Diese Bedingungen gelten für die gesamte Geschäftsverbindung zwischen dem Kunden und der Bank. Wenn der Kunde {first} {last}, wohnhaft in {city}, {street} {num}, eine Transaktion über das Online-Banking-Portal von der IP-Adresse {ip} initiiert, wird eine SMS an {phone} gesendet. Bei Fragen (IBAN: {iban}) wenden Sie sich an den Support.",
    "Typ-2-Diabetes ist eine Stoffwechselerkrankung, die zu erhöhten Blutzuckerwerten führt. Bei einer Routineuntersuchung in unserer Klinik in {city} wies der Patient {first} {last} (Ausweis: {id}) auffällige Werte auf. Der Patient wurde umgehend informiert und ist für Rückfragen unter {phone} erreichbar. Die Krankenakte wurde aktualisiert.",
    "Datenschutzerklärung: Wir nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wenn der Benutzer {first} {last} unsere Website besucht, protokollieren wir standardmäßig die IP-Adresse {ip} sowie das Datum des Zugriffs ({dob}). Wir geben Ihre Daten, einschließlich der Adresse in der {street} {num}, nicht an Dritte weiter. Kontakt: {phone}.",
    "Vollkaskoversicherung für Kraftfahrzeuge: Diese Police deckt Unfallschäden, Diebstahl und Brand gemäß den Allgemeinen Versicherungsbedingungen (AKB) ab. Der Hauptversicherungsnehmer, {first} {last} (Ausweisnummer: {id}), ist berechtigt, im Schadensfall Ansprüche geltend zu machen. Das versicherte Fahrzeug ist an der Adresse {street} {num} in {city} gemeldet. Im Schadensfall kontaktieren Sie bitte die Hotline unter {phone}."
]

# --- New Domains (HR, IT, Retail, Edu, Gov, Travel) ---
he_new_domains = [
    "קורות חיים: המועמד {first} {last}, בוגר אוניברסיטת {city}. עבד בעבר בחברת הייטק. ממליצים: {first2} {last2}, טלפון: {phone}.", # HR
    "שגיאת שרת: 500 Internal Server Error. כתובת IP של הבקשה: {ip}. משתמש מחובר: {first}.{last}. Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.", # IT
    "הזמנה מספר {num}{num}{num} נשלחה בהצלחה. כתובת למשלוח: {street} {num}, {city}. שם המקבל: {first} {last}. טלפון לשליח: {phone}.", # E-commerce
    "תעודת הערכה לתלמיד {first} {last} (ת\"ז: {id}). הורי התלמיד מתבקשים להגיע לאסיפת הורים. הכתובת במערכת: {street} {num}, {city}.", # Education
    "רשות המיסים: הודעה על שומת מס לשנת 2025. נישום: {first} {last}. מספר תעודת זהות: {id}. נא לשלם עד {dob}.", # Government
    "אישור הזמנת טיסה: נוסע {first} {last}, דרכון מספר {part_he}. טיסה ל-{en_city}. תאריך יציאה: {dob}. טלפון חירום: {phone}." # Travel
]

en_new_domains = [
    "Resume: Candidate {first} {last}, graduated from state university. Former employee at TechCorp. References: {first2} {last2}, Phone: {phone}.", # HR
    "Server Error: 500 Internal Server Error. Request IP: {ip}. Logged in user: {first}.{last}. Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.", # IT
    "Order #{num}{num}{num} has been shipped. Shipping address: {num} {street}, {city}. Recipient: {first} {last}. Courier contact: {phone}.", # E-commerce
    "Student Evaluation for {first} {last} (ID: {id}). Parents are requested to attend the meeting. Address on file: {num} {street}, {city}.", # Education
    "Department of Revenue: Notice of Tax Assessment for 2025. Taxpayer: {first} {last}. SSN: {id}. Please pay the balance by {dob}.", # Government
    "Flight Confirmation: Passenger {first} {last}, Passport #{part_en}. Flight to {city}. Departure Date: {dob}. Emergency contact: {phone}." # Travel
]

de_new_domains = [
    "Lebenslauf: Kandidat {first} {last}, Absolvent der Universität. Ehemaliger Mitarbeiter bei TechCorp. Referenzen: {first2} {last2}, Telefon: {phone}.", # HR
    "Serverfehler: 500 Internal Server Error. Anfrage-IP: {ip}. Angemeldeter Benutzer: {first}.{last}. Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.", # IT
    "Bestellung #{num}{num}{num} wurde versandt. Lieferadresse: {street} {num}, {city}. Empfänger: {first} {last}. Kurierkontakt: {phone}.", # E-commerce
    "Schülerbewertung für {first} {last} (ID: {id}). Die Eltern werden gebeten, am Elternabend teilzunehmen. Adresse: {street} {num}, {city}.", # Education
    "Finanzamt: Bescheid über die Steuerfestsetzung für 2025. Steuerzahler: {first} {last}. Steuernummer: {id}. Bitte zahlen Sie bis {dob}.", # Government
    "Flugbestätigung: Passagier {first} {last}, Reisepass #{part_en}. Flug nach {city}. Abflugdatum: {dob}. Notfallkontakt: {phone}." # Travel
]

# --- Spanish Templates ---
es_edge_cases = [
    "Datos de contacto:\nNombre: {first} {last}\nTeléfono: {phone}\nDNI: {id}",
    "Por favor llámame al 📞{phone} o escribe a {first}.{last}@example.es 📧.",
    "<div>Nombre del cliente: <strong>{first} {last}</strong></div><p>Identificador: <span>{id}</span></p>",
    "https://api.example.es/update?user={first}%20{last}&dni={id}&phone={phone}",
    "[{first} {last}], ({id}), '{phone}' - datos actualizados en el sistema.",
    "Empleado\t{first} {last}\tcon DNI\t{id}\tsolicita aprobación.",
    "NOMBRE: {FIRST} {LAST}!!! NÚMERO: {ID}???",
]

es_implicit = [
    "Dejé el paquete con {first} {last} en {street} {num}. Llama al {phone} si hay problemas.",
    "Aquí está el código que necesitas: {id}. No lo compartas con {first}.",
    "Oye, los datos son: {first} {last}, {id}, {dob}. Gracias.",
    "Hablé hoy con {first}. Dijo que lo enviemos a {city} y que le llamemos al {phone}.",
    "Por favor envía los documentos a {first} {last}, {street} {num}, {city}.",
    "Quedé con {first} cerca de {street} {num}. Contacté con {first2} en el {phone}.",
]

es_templates = [
    "Póliza de seguro de vida de {first} {last}, DNI {id}. Reside en {street} {num}, {city}. Teléfono: {phone}. Fecha de nacimiento: {dob}.",
    "Parte de accidente. Conductor responsable: {first} {last}, matrícula {num}XYZ{num}. Reside en {city}.",
    "El cliente {first} {last} solicitó un presupuesto para el seguro del coche. DNI: {id}. Teléfono: {phone}.",
    "Cliente {first} {last}, correo {first}.{last}@example.es, inició una transferencia desde la IP {ip}.",
    "El paciente {first} {last} llegó a la clínica. DNI: {id}. Pulso: 80, tensión: 120/80.",
    "El demandante {first} {last} presentó una demanda contra Mapfre. Número de caso: {num}{num}-{num}.",
    "Sentencia en el caso {num} - {first} {last} contra el Banco Santander. Se condena al pago de 50.000 €.",
    "La nueva tarjeta terminada en {num}{num} fue enviada a {street} {num}, {city} a nombre de {first} {last}.",
    "Informe de alta - El paciente {first} {last} fue dado de alta. Enviar documentos a: {street} {num}, {city}.",
    "Receta de medicación crónica entregada a la paciente {first} {last} con DNI {id}.",
    "Según la política de la empresa, solo se permite fumar en las zonas habilitadas.",
    "La ley de protección al consumidor obliga a mostrar los precios con IVA incluido.",
    "El plazo de gracia termina en mayo.",
    "Esperamos terminar el proyecto a tiempo y dentro del presupuesto.",
    "La referencia {part_en} está agotada actualmente.",
    "Se espera mal tiempo mañana en toda la península. Eviten desplazamientos.",
    "The customer {en_first} {en_last} called about his account. He lives in {en_city}.",
    "La dirección MAC del equipo de {first} es {mac} y se conecta desde la IP {ip}.",
    "Se realizó una transferencia al IBAN {iban} por parte de {first}.",
]

es_longform = [
    "CONDICIONES GENERALES DEL CONTRATO DE ARRENDAMIENTO: Reunidos de una parte el arrendador, propietario registral de la vivienda situada en {street} {num}, {city}; y de otra el arrendatario {first} {last}, con DNI {id}, interesado en arrendar la vivienda por un período de 12 meses. La renta mensual se fija en 900 €. Para consultas, contactar en el teléfono {phone}.",
    "La diabetes tipo 2 es una enfermedad metabólica caracterizada por niveles elevados de glucosa en sangre. En una revisión rutinaria en nuestro centro de {city}, el paciente {first} {last} (DNI: {id}) presentó valores anómalos. El paciente, con domicilio en {street} {num}, fue informado de los resultados. Más información: {phone}.",
    "POLÍTICA DE PRIVACIDAD: Nos tomamos muy en serio la protección de sus datos personales conforme al RGPD. Cuando el usuario {first} {last} visita nuestro sitio web, registramos la dirección IP {ip} y la fecha de acceso. No cedemos sus datos, incluida la dirección de {street} {num}, a terceros. Los pagos pueden realizarse a la cuenta IBAN {iban}. Contacto: {phone}.",
    "Póliza de seguro a todo riesgo del automóvil: la presente póliza cubre daños accidentales, robo e incendio según las condiciones generales. El tomador del seguro, {first} {last} (DNI: {id}), está autorizado a presentar reclamaciones. El vehículo asegurado está domiciliado en {street} {num}, {city}. En caso de siniestro, llame a atención al cliente: {phone}.",
]

es_new_domains = [
    "Currículum: Candidato {first} {last}, graduado por la universidad. Antiguo empleado de TechCorp. Referencias: {first2} {last2}, teléfono: {phone}.",
    "Error del servidor: 500 Internal Server Error. IP de la petición: {ip}. Usuario conectado: {first}.{last}. Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
    "El pedido #{num}{num}{num} ha sido enviado. Dirección de entrega: {street} {num}, {city}. Destinatario: {first} {last}. Teléfono del mensajero: {phone}.",
    "Evaluación del alumno {first} {last} (DNI: {id}). Se ruega a los padres asistir a la reunión. Dirección registrada: {street} {num}, {city}.",
    "Agencia Tributaria: notificación de liquidación del ejercicio 2025. Contribuyente: {first} {last}. NIF: {id}. Plazo de pago hasta el {dob}.",
    "Confirmación de vuelo: pasajero {first} {last}, pasaporte n.º {part_en}. Vuelo a {en_city}. Fecha de salida: {dob}. Contacto de emergencia: {phone}.",
]

# --- French Templates ---
fr_edge_cases = [
    "Coordonnées :\nNom : {first} {last}\nTéléphone : {phone}\nNIR : {id}",
    "Merci de me rappeler au 📞{phone} ou par mail à {first}.{last}@example.fr 📧.",
    "<div>Nom du client : <strong>{first} {last}</strong></div><p>Identifiant : <span>{id}</span></p>",
    "https://api.example.fr/update?user={first}%20{last}&nir={id}&phone={phone}",
    "[{first} {last}], ({id}), '{phone}' - informations mises à jour dans le système.",
    "Employé\t{first} {last}\tavec le NIR\t{id}\tdemande une validation.",
    "NOM : {FIRST} {LAST}!!! NUMÉRO : {ID}???",
]

fr_implicit = [
    "J'ai laissé le colis chez {first} {last}, {num} {street}. Appelez le {phone} en cas de problème.",
    "Voici le code dont tu as besoin : {id}. Ne le partage pas avec {first}.",
    "Salut, les infos sont : {first} {last}, {id}, {dob}. Merci.",
    "J'ai parlé à {first} aujourd'hui. Il a dit de transmettre à {city} et de le joindre au {phone}.",
    "Merci d'envoyer les documents à {first} {last}, {num} {street}, {city}.",
    "J'ai retrouvé {first} près du {num} {street}. J'ai joint {first2} au {phone}.",
]

fr_templates = [
    "Contrat d'assurance-vie de {first} {last}, NIR {id}. Domicilié au {num} {street}, {city}. Téléphone : {phone}. Date de naissance : {dob}.",
    "Constat d'accident. Conducteur responsable : {first} {last}, immatriculation {num}XYZ{num}. Domicilié à {city}.",
    "Le client {first} {last} a demandé un devis d'assurance auto. NIR : {id}. Téléphone : {phone}.",
    "Client {first} {last}, e-mail {first}.{last}@example.fr, a initié un virement depuis l'IP {ip}.",
    "Le patient {first} {last} est arrivé à la clinique. NIR : {id}. Pouls : 80, tension : 120/80.",
    "Le demandeur {first} {last} a déposé plainte contre AXA. Numéro de dossier : {num}{num}-{num}.",
    "Jugement dans l'affaire {num} - {first} {last} contre BNP Paribas. Le défendeur est condamné à verser 50 000 €.",
    "La nouvelle carte se terminant par {num}{num} a été envoyée au {num} {street}, {city} pour {first} {last}.",
    "Compte rendu de sortie - Le patient {first} {last} est sorti. Envoyer les documents au : {num} {street}, {city}.",
    "Ordonnance de médicaments chroniques remise à la patiente {first} {last}, NIR {id}.",
    "Selon le règlement intérieur, il est interdit de fumer en dehors des zones prévues.",
    "Le code de la consommation impose l'affichage des prix TTC.",
    "Le délai de grâce se termine en mai.",
    "Nous espérons terminer le projet dans les délais et le budget.",
    "La référence {part_en} est actuellement en rupture de stock.",
    "Fortes intempéries attendues demain dans tout le pays. Évitez les déplacements.",
    "The customer {en_first} {en_last} called about his account. He lives in {en_city}.",
    "L'adresse MAC du poste de {first} est {mac}, connecté depuis l'IP {ip}.",
    "Un virement vers l'IBAN {iban} a été initié par {first}.",
]

fr_longform = [
    "CONDITIONS GÉNÉRALES DE LOCATION : Entre les soussignés, le bailleur, propriétaire du logement situé au {num} {street}, {city} ; et le locataire {first} {last}, NIR {id}, souhaitant louer le logement pour une durée de 12 mois. Le loyer mensuel est fixé à 900 €. Pour toute question, contacter le {phone}.",
    "Le diabète de type 2 est une maladie métabolique caractérisée par une glycémie élevée. Lors d'un contrôle de routine dans notre centre de {city}, le patient {first} {last} (NIR : {id}) a présenté des valeurs anormales. Le patient, domicilié au {num} {street}, a été informé des résultats. Renseignements : {phone}.",
    "POLITIQUE DE CONFIDENTIALITÉ : Conformément au RGPD, nous protégeons vos données personnelles. Lorsque l'utilisateur {first} {last} visite notre site, nous enregistrons l'adresse IP {ip} ainsi que la date d'accès. Nous ne transmettons pas vos données, y compris l'adresse au {num} {street}, à des tiers. Les paiements peuvent être effectués sur l'IBAN {iban}. Contact : {phone}.",
    "Contrat d'assurance automobile tous risques : la présente police couvre les dommages accidentels, le vol et l'incendie selon les conditions générales. Le souscripteur, {first} {last} (NIR : {id}), est habilité à déclarer un sinistre. Le véhicule assuré est stationné au {num} {street}, {city}. En cas de sinistre, contactez votre agent au {phone}.",
]

fr_new_domains = [
    "CV : Candidat {first} {last}, diplômé de l'université. Ancien salarié de TechCorp. Références : {first2} {last2}, téléphone : {phone}.",
    "Erreur serveur : 500 Internal Server Error. IP de la requête : {ip}. Utilisateur connecté : {first}.{last}. Token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
    "La commande n°{num}{num}{num} a été expédiée. Adresse de livraison : {num} {street}, {city}. Destinataire : {first} {last}. Téléphone du livreur : {phone}.",
    "Bulletin de l'élève {first} {last} (NIR : {id}). Les parents sont priés d'assister à la réunion. Adresse enregistrée : {num} {street}, {city}.",
    "Direction générale des Finances publiques : avis d'imposition 2025. Contribuable : {first} {last}. NIR : {id}. À régler avant le {dob}.",
    "Confirmation de vol : passager {first} {last}, passeport n°{part_en}. Vol vers {en_city}. Départ : {dob}. Contact d'urgence : {phone}.",
]

# --- Italian Templates ---
it_edge_cases = [
    "Dati di contatto:\nNome: {first} {last}\nTelefono: {phone}\nCodice fiscale: {id}",
    "Per favore richiamami al 📞{phone} o scrivi a {first}.{last}@example.it 📧.",
    "<div>Nome cliente: <strong>{first} {last}</strong></div><p>Identificativo: <span>{id}</span></p>",
    "https://api.example.it/update?user={first}%20{last}&cf={id}&phone={phone}",
    "[{first} {last}], ({id}), '{phone}' - dati appena aggiornati nel sistema.",
    "Dipendente\t{first} {last}\tcon CF\t{id}\trichiede approvazione.",
    "NOME: {FIRST} {LAST}!!! NUMERO: {ID}???",
]

it_implicit = [
    "Ho lasciato il pacco a {first} {last} in {street} {num}. Chiama il {phone} in caso di problemi.",
    "Ecco il codice che ti serve: {id}. Non condividerlo con {first}.",
    "Ciao, i dati sono: {first} {last}, {id}, {dob}. Grazie.",
    "Ho parlato oggi con {first}. Ha detto di inoltrare a {city} e di chiamarlo al {phone}.",
    "Per favore invia i documenti a {first} {last}, {street} {num}, {city}.",
    "Ho incontrato {first} vicino a {street} {num}. Ho contattato {first2} al {phone}.",
]

it_templates = [
    "Polizza vita di {first} {last}, codice fiscale {id}. Residente in {street} {num}, {city}. Telefono: {phone}. Data di nascita: {dob}.",
    "Verbale di incidente. Conducente responsabile: {first} {last}, targa {num}XYZ{num}. Residente a {city}.",
    "Il cliente {first} {last} ha richiesto un preventivo per l'assicurazione auto. CF: {id}. Telefono: {phone}.",
    "Cliente {first} {last}, email {first}.{last}@example.it, ha avviato un bonifico dall'IP {ip}.",
    "Il paziente {first} {last} è arrivato in clinica. CF: {id}. Battito: 80, pressione: 120/80.",
    "L'attore {first} {last} ha citato in giudizio Generali. Numero pratica: {num}{num}-{num}.",
    "Sentenza nella causa {num} - {first} {last} contro UniCredit. Il convenuto è condannato a pagare 50.000 €.",
    "La nuova carta che termina con {num}{num} è stata spedita in {street} {num}, {city} per {first} {last}.",
    "Lettera di dimissioni - Il paziente {first} {last} è stato dimesso. Inviare i documenti a: {street} {num}, {city}.",
    "Ricetta per farmaci cronici consegnata alla paziente {first} {last} con codice fiscale {id}.",
    "Secondo il regolamento aziendale, è consentito fumare solo nelle aree dedicate.",
    "Il codice del consumo impone di esporre i prezzi IVA inclusa.",
    "Il periodo di prova termina a maggio.",
    "Speriamo di concludere il progetto nei tempi e nel budget previsti.",
    "Il codice articolo {part_en} è attualmente esaurito.",
    "Previsto maltempo domani su tutto il paese. Evitare spostamenti non necessari.",
    "The customer {en_first} {en_last} called about his account. He lives in {en_city}.",
    "L'indirizzo MAC del dispositivo di {first} è {mac}, connesso dall'IP {ip}.",
    "Un bonifico verso l'IBAN {iban} è stato disposto da {first}.",
]

it_longform = [
    "CONDIZIONI GENERALI DEL CONTRATTO DI LOCAZIONE: tra il locatore, proprietario dell'immobile sito in {street} {num}, {city}; e il conduttore {first} {last}, codice fiscale {id}, interessato a locare l'immobile per 12 mesi. Il canone mensile è fissato in 900 €. Per informazioni contattare il numero {phone}.",
    "Il diabete di tipo 2 è una malattia metabolica caratterizzata da glicemia elevata. Durante un controllo di routine presso il nostro centro di {city}, il paziente {first} {last} (CF: {id}) ha presentato valori anomali. Il paziente, residente in {street} {num}, è stato informato dei risultati. Per informazioni: {phone}.",
    "INFORMATIVA PRIVACY: ai sensi del GDPR proteggiamo i suoi dati personali. Quando l'utente {first} {last} visita il nostro sito, registriamo l'indirizzo IP {ip} e la data di accesso. Non cediamo i suoi dati, compreso l'indirizzo in {street} {num}, a terzi. I pagamenti possono essere effettuati sull'IBAN {iban}. Contatto: {phone}.",
    "Polizza kasko per autoveicoli: la presente polizza copre danni accidentali, furto e incendio secondo le condizioni generali. Il contraente, {first} {last} (CF: {id}), è autorizzato a presentare denuncia di sinistro. Il veicolo assicurato è custodito in {street} {num}, {city}. In caso di sinistro contattare il numero {phone}.",
]

it_new_domains = [
    "Curriculum: candidato {first} {last}, laureato all'università. Ex dipendente di TechCorp. Referenze: {first2} {last2}, telefono: {phone}.",
    "Errore server: 500 Internal Server Error. IP della richiesta: {ip}. Utente connesso: {first}.{last}. Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.",
    "L'ordine n.{num}{num}{num} è stato spedito. Indirizzo di consegna: {street} {num}, {city}. Destinatario: {first} {last}. Telefono del corriere: {phone}.",
    "Valutazione dello studente {first} {last} (CF: {id}). I genitori sono pregati di partecipare al colloquio. Indirizzo registrato: {street} {num}, {city}.",
    "Agenzia delle Entrate: avviso di accertamento 2025. Contribuente: {first} {last}. Codice fiscale: {id}. Pagare entro il {dob}.",
    "Conferma volo: passeggero {first} {last}, passaporto n. {part_en}. Volo per {en_city}. Data di partenza: {dob}. Contatto di emergenza: {phone}.",
]

# --- Language lookup tables (added with es/fr/it; templates unchanged) ---
LANG_DATA = {
    "he": (he_first_names, he_last_names, he_cities, he_streets, he_implicit, he_edge_cases, he_longform, he_new_domains, he_templates),
    "en": (en_first_names, en_last_names, en_cities, en_streets, en_implicit, en_edge_cases, en_longform, en_new_domains, en_templates),
    "de": (de_first_names, de_last_names, de_cities, de_streets, de_implicit, de_edge_cases, de_longform, de_new_domains, de_templates),
    "es": (es_first_names, es_last_names, es_cities, es_streets, es_implicit, es_edge_cases, es_longform, es_new_domains, es_templates),
    "fr": (fr_first_names, fr_last_names, fr_cities, fr_streets, fr_implicit, fr_edge_cases, fr_longform, fr_new_domains, fr_templates),
    "it": (it_first_names, it_last_names, it_cities, it_streets, it_implicit, it_edge_cases, it_longform, it_new_domains, it_templates),
}


def generate_record(lang, mode="normal"):
    firsts, lasts, cities, streets, _implicit, _edge, _long, _domains, _normal = LANG_DATA[lang]
    
    first = random.choice(firsts)
    last = random.choice(lasts)
    first2 = random.choice(firsts)
    last2 = random.choice(lasts)
    
    en_first = random.choice(en_first_names)
    en_last = random.choice(en_last_names)
    en_city_val = random.choice(en_cities)
    
    city = random.choice(cities)
    street = random.choice(streets)
    num = random.randint(1, 99)
    id_val = gen_id(lang)
    phone = gen_phone(lang)
    
    if mode == "implicit":
        template_list = _implicit
    elif mode == "edge_case":
        template_list = _edge
    elif mode == "longform":
        template_list = _long
    elif mode == "new_domains":
        template_list = _domains
    else:
        template_list = _normal
        
    template = random.choice(template_list)
    
    text = template.format(
        first=first,
        last=last,
        FIRST=first.upper(),
        LAST=last.upper(),
        first2=first2,
        last2=last2,
        en_first=en_first,
        en_last=en_last,
        en_city=en_city_val,
        city=city,
        street=street,
        num=num,
        id=id_val,
        ID=id_val,
        phone=phone,
        dob=gen_dob(),
        ip=gen_ip(),
        mac=gen_mac(),
        iban=gen_iban(lang),
        part_he=gen_part_num_he(),
        part_en=gen_part_num()
    )
    return text

if __name__ == '__main__':
    import sys
    data_dir = '/home/yehoshua_sus/Projects/owltable/owlmask-maskbench/data'
    os.makedirs(data_dir, exist_ok=True)

    # Pass languages as args to (re)generate selectively, e.g.
    # `python generate_raw_data.py es fr it` — avoids overwriting the
    # existing he/en/de files unless explicitly requested.
    langs = sys.argv[1:] or ["he", "en", "de", "es", "fr", "it"]

    for lang in langs:
        out_file_utf8 = os.path.join(data_dir, f'texts-to-mask-{lang}.txt')
        
        # Write UTF-8 version
        with open(out_file_utf8, 'w', encoding='utf-8') as f:
            for i in range(2000): f.write(generate_record(lang, mode="normal") + "\n\n---\n\n")
            for i in range(1000): f.write(generate_record(lang, mode="implicit") + "\n\n---\n\n")
            for i in range(3000): f.write(generate_record(lang, mode="edge_case") + "\n\n---\n\n")
            for i in range(1000): f.write(generate_record(lang, mode="longform") + "\n\n---\n\n")
            # 6 new domains * 500 records each = 3000 total records
            for i in range(3000): f.write(generate_record(lang, mode="new_domains") + "\n\n---\n\n")
            
        print(f"Generated 10000 records for {lang} (UTF-8) in {out_file_utf8}")

    # Generate additional encodings for Hebrew and German to test encoding support
    if "he" in langs:
        out_file_he_iso = os.path.join(data_dir, 'texts-to-mask-he-iso8859-8.txt')
        with open(out_file_he_iso, 'w', encoding='iso8859-8', errors='replace') as f:
            for i in range(100): f.write(generate_record("he", mode="normal") + "\n\n---\n\n")
        print(f"Generated 100 records for he (ISO-8859-8) in {out_file_he_iso}")

    if "de" in langs:
        out_file_de_iso = os.path.join(data_dir, 'texts-to-mask-de-iso8859-1.txt')
        with open(out_file_de_iso, 'w', encoding='iso8859-1', errors='replace') as f:
            for i in range(100): f.write(generate_record("de", mode="normal") + "\n\n---\n\n")
        print(f"Generated 100 records for de (ISO-8859-1) in {out_file_de_iso}")

    # Spanish/French/Italian ISO-8859-1 (Latin-1) legacy-encoding variants
    for iso_lang in [l for l in ("es", "fr", "it") if l in langs]:
        out_file_iso = os.path.join(data_dir, f'texts-to-mask-{iso_lang}-iso8859-1.txt')
        with open(out_file_iso, 'w', encoding='iso8859-1', errors='replace') as f:
            for i in range(100): f.write(generate_record(iso_lang, mode="normal") + "\n\n---\n\n")
        print(f"Generated 100 records for {iso_lang} (ISO-8859-1) in {out_file_iso}")
