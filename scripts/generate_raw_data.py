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

# --- Generators ---
def gen_id(lang):
    if lang == "he": return "".join([str(random.randint(0, 9)) for _ in range(9)])
    elif lang == "en": return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
    elif lang == "de": return f"T{random.randint(10000000, 99999999)}"

def gen_phone(lang):
    if lang == "he": return random.choice([f"05{random.randint(0, 9)}-{random.randint(1000000, 9999999)}", f"05{random.randint(0, 9)} {random.randint(100,999)} {random.randint(1000,9999)}"])
    elif lang == "en": return random.choice([f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}", f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"])
    elif lang == "de": return random.choice([f"+49 151 {random.randint(1000000, 9999999)}", f"0151 {random.randint(1000000, 9999999)}"])

def gen_part_num(): return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"
def gen_part_num_he(): return "".join([str(random.randint(0, 9)) for _ in range(9)])
def gen_dob(): return f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1950, 2010)}"
def gen_ip(): return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
def gen_mac(): return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
def gen_iban(lang):
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

def generate_record(lang, mode="normal"):
    firsts = he_first_names if lang == "he" else en_first_names if lang == "en" else de_first_names
    lasts = he_last_names if lang == "he" else en_last_names if lang == "en" else de_last_names
    cities = he_cities if lang == "he" else en_cities if lang == "en" else de_cities
    streets = he_streets if lang == "he" else en_streets if lang == "en" else de_streets
    
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
        template_list = he_implicit if lang == "he" else en_implicit if lang == "en" else de_implicit
    elif mode == "edge_case":
        template_list = he_edge_cases if lang == "he" else en_edge_cases if lang == "en" else de_edge_cases
    elif mode == "longform":
        template_list = he_longform if lang == "he" else en_longform if lang == "en" else de_longform
    elif mode == "new_domains":
        template_list = he_new_domains if lang == "he" else en_new_domains if lang == "en" else de_new_domains
    else:
        template_list = he_templates if lang == "he" else en_templates if lang == "en" else de_templates
        
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
    data_dir = '/home/yehoshua_sus/Projects/owltable/owlmask-maskbench/data'
    os.makedirs(data_dir, exist_ok=True)
    
    langs = ["he", "en", "de"]
    
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
    # Hebrew ISO-8859-8
    out_file_he_iso = os.path.join(data_dir, 'texts-to-mask-he-iso8859-8.txt')
    with open(out_file_he_iso, 'w', encoding='iso8859-8', errors='replace') as f:
        for i in range(100): f.write(generate_record("he", mode="normal") + "\n\n---\n\n")
    print(f"Generated 100 records for he (ISO-8859-8) in {out_file_he_iso}")

    # German ISO-8859-1 (Latin-1)
    out_file_de_iso = os.path.join(data_dir, 'texts-to-mask-de-iso8859-1.txt')
    with open(out_file_de_iso, 'w', encoding='iso8859-1', errors='replace') as f:
        for i in range(100): f.write(generate_record("de", mode="normal") + "\n\n---\n\n")
    print(f"Generated 100 records for de (ISO-8859-1) in {out_file_de_iso}")
