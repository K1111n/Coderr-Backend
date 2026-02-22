# API Endpoints Dokumentation

Authentication
Login und Registrierung

POST

/api/registration/

Description: Erstellt einen neuen Benutzer. Dieser Benutzer kann entweder ein Customer- oder Business-User sein.
Request Body
{
"username": "exampleUsername",
"email": "example@mail.de",
"password": "examplePassword",
"repeated_password": "examplePassword",
"type": "customer"
}
Success Response
Erfolgreicher Erstellung gibt dies ein Token sowie die Benutzerinformationen zurück, inklusive die einzigartige Nutzer-ID.
{
"token": "83bf098723b08f7b23429u0fv8274",
"username": "exampleUsername",
"email": "example@mail.de",
"user_id": 123
}
Status Codes
201: Der Benutzer wurde erfolgreich erstellt.
400: Ungültige Anfragedaten.
500: Interner Serverfehler.
Rate Limits
No limit
No Permissions required

POST

/api/login/

Description: Authentifiziert einen Benutzer und liefert ein Authentifizierungs-Token zurück, das für weitere API-Anfragen genutzt wird.
Request Body
{
"username": "exampleUsername",
"password": "examplePassword"
}
Success Response
Erfolgreiche Authentifizierung gibt ein Token sowie Benutzerinformationen zurück.
{
"token": "83bf098723b08f7b23429u0fv8274",
"username": "exampleUsername",
"email": "example@mail.de",
"user_id": 123
}
Status Codes
200: Erfolgreiche Anmeldung.
400: Ungültige Anfragedaten.
500: Interner Serverfehler.
Rate Limits
No limit
No Permissions required
Profile
Alles an CRUD das für das Frontend eine Rolle spielt

GET

/api/profile/{pk}/

Description: Ruft die detaillierten Informationen eines Benutzerprofils ab (sowohl für Kunden- als auch für Geschäftsnutzer). Ermöglicht auch das Bearbeiten der Profildaten (PATCH).
URL Parameters
Name Type Description
pk - Die ID des Benutzers, dessen Profil abgerufen oder bearbeitet wird.
Success Response
Die Antwort enthält die vollständigen Profildaten eines spezifischen Benutzers. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.
{
"user": 1,
"username": "max_mustermann",
"first_name": "Max",
"last_name": "Mustermann",
"file": "profile_picture.jpg",
"location": "Berlin",
"tel": "123456789",
"description": "Business description",
"working_hours": "9-17",
"type": "business",
"email": "max@business.de",
"created_at": "2023-01-01T12:00:00Z"
}
Status Codes
200: Die Profildaten wurden erfolgreich abgerufen.
401: Benutzer ist nicht authentifiziert.
404: Das Benutzerprofil wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.

PATCH

/api/profile/{pk}/

Description: Ermöglicht es einem Benutzer, bestimmte Profilinformationen zu aktualisieren.
URL Parameters
Name Type Description
pk - Die ID des Benutzers, dessen Profil bearbeitet wird.
Request Body
{
"first_name": "Max",
"last_name": "Mustermann",
"location": "Berlin",
"tel": "987654321",
"description": "Updated business description",
"working_hours": "10-18",
"email": "new_email@business.de"
}
Success Response
Die Antwort enthält das aktualisierte Profil des Benutzers. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.
{
"user": 1,
"username": "max_mustermann",
"first_name": "Max",
"last_name": "Mustermann",
"file": "profile_picture.jpg",
"location": "Berlin",
"tel": "987654321",
"description": "Updated business description",
"working_hours": "10-18",
"type": "business",
"email": "new_email@business.de",
"created_at": "2023-01-01T12:00:00Z"
}
Status Codes
200: Das Profil wurde erfolgreich aktualisiert.
401: Benutzer ist nicht authentifiziert
403: Authentifizierter Benutzer ist nicht der Eigentümer Profils
404: Das Benutzerprofil wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer kann NUR sein eigenes Profil bearbeiten.

GET

/api/profiles/business/

Description: Gibt eine Liste aller Geschäftsnutzer auf der Plattform zurück.
Success Response
Die Antwort enthält eine Liste aller Geschäftsnutzer mit ihren Profilinformationen. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.
[
{
"user": 1,
"username": "max_business",
"first_name": "Max",
"last_name": "Mustermann",
"file": "profile_picture.jpg",
"location": "Berlin",
"tel": "123456789",
"description": "Business description",
"working_hours": "9-17",
"type": "business"
}
]
Status Codes
200: Erfolgreiche Antwort mit der Liste der Geschäftsnutzer.
401: Benutzer ist nicht authentifiziert.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.

GET

/api/profiles/customer/

Description: Gibt eine Liste aller Kundenprofile auf der Plattform zurück.
Success Response
Die Antwort enthält eine Liste aller Kunden mit ihren Profilinformationen. Die Felder first_name, last_name, location, tel, description und working_hours dürfen im Response nicht null sein, sondern müssen, falls keine Werte vorhanden sind, mit einem leeren String ('' '') belegt werden.
[
{
"user": 2,
"username": "customer_jane",
"first_name": "Jane",
"last_name": "Doe",
"file": "profile_picture_customer.jpg",
"uploaded_at": "2023-09-15T09:00:00",
"type": "customer"
}
]
Status Codes
200: Erfolgreiche Antwort mit der Liste der Kundenprofile.
401: Benutzer ist nicht authentifiziert.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.
Angebote (offers)
Alles an CRUD das für das Frontend eine Rolle spielt

GET

/api/offers/

Description: Dieser Endpunkt gibt eine Liste von Angeboten zurück. Jedes Angebot enthält eine Übersicht der Angebotsdetails, den minimalen Preis und die kürzeste Lieferzeit.
Query Parameters
Name Type Description
creator_id integer Filtert die Angebote nach dem Benutzer, der sie erstellt hat.
min_price float Filtert Angebote mit einem Mindestpreis.
max_delivery_time integer Filtert Angebote, deren Lieferzeit kürzer oder gleich dem angegebenen Wert ist.
ordering string Sortiert die Angebote nach den Feldern 'updated_at' oder 'min_price'.
search string Durchsucht die Felder 'title' und 'description' nach Übereinstimmungen.
page_size integer Gibt an, wie viele Ergebnisse pro Seite zurückgegeben werden sollen. Dies sollte mit dem Frontend abgestimmt sein.
Success Response
Die Antwort ist eine paginierte Liste von Angeboten mit den zugehörigen Details.
{
"count": 1,
"next": "http://127.0.0.1:8000/api/offers/?page=2",
"previous": null,
"results": [
{
"id": 1,
"user": 1,
"title": "Website Design",
"image": null,
"description": "Professionelles Website-Design...",
"created_at": "2024-09-25T10:00:00Z",
"updated_at": "2024-09-28T12:00:00Z",
"details": [
{
"id": 1,
"url": "/offerdetails/1/"
},
{
"id": 2,
"url": "/offerdetails/2/"
},
{
"id": 3,
"url": "/offerdetails/3/"
}
],
"min_price": 100,
"min_delivery_time": 7,
"user_details": {
"first_name": "John",
"last_name": "Doe",
"username": "jdoe"
}
}
]
}
Status Codes
200: Die Anfrage war erfolgreich und eine Liste von Angeboten wurde zurückgegeben.
400: Ungültige Anfrageparameter.
500: Interner Serverfehler.
Rate Limits
No limit
No Permissions required
Extra Information: Die Antwort verwendet PageNumberPagination.

POST

/api/offers/

Description: Dieser Endpunkt ermöglicht es, ein neues Angebot (Offer) zu erstellen. Ein Offer muss 3 Details enthalten!
Request Body
{
"title": "Grafikdesign-Paket",
"image": null,
"description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
"details": [
{
"title": "Basic Design",
"revisions": 2,
"delivery_time_in_days": 5,
"price": 100,
"features": [
"Logo Design",
"Visitenkarte"
],
"offer_type": "basic"
},
{
"title": "Standard Design",
"revisions": 5,
"delivery_time_in_days": 7,
"price": 200,
"features": [
"Logo Design",
"Visitenkarte",
"Briefpapier"
],
"offer_type": "standard"
},
{
"title": "Premium Design",
"revisions": 10,
"delivery_time_in_days": 10,
"price": 500,
"features": [
"Logo Design",
"Visitenkarte",
"Briefpapier",
"Flyer"
],
"offer_type": "premium"
}
]
}
Success Response
Bei erfolgreicher Erstellung wird das Angebot mit den zugehörigen Details zurückgegeben, einschließlich IDs für das Angebot und jedes Detail.
{
"id": 1,
"title": "Grafikdesign-Paket",
"image": null,
"description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
"details": [
{
"id": 1,
"title": "Basic Design",
"revisions": 2,
"delivery_time_in_days": 5,
"price": 100,
"features": [
"Logo Design",
"Visitenkarte"
],
"offer_type": "basic"
},
{
"id": 2,
"title": "Standard Design",
"revisions": 5,
"delivery_time_in_days": 7,
"price": 200,
"features": [
"Logo Design",
"Visitenkarte",
"Briefpapier"
],
"offer_type": "standard"
},
{
"id": 3,
"title": "Premium Design",
"revisions": 10,
"delivery_time_in_days": 10,
"price": 500,
"features": [
"Logo Design",
"Visitenkarte",
"Briefpapier",
"Flyer"
],
"offer_type": "premium"
}
]
}
Status Codes
201: Das Angebot wurde erfolgreich erstellt.
400: Ungültige Anfragedaten oder unvollständige Details.
401: Benutzer ist nicht authentifiziert.
403: Authentifizierter Benutzer ist kein 'business' Profil
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Nur User vom type 'business' dürfen Angebote erstellen

GET

/api/offers/{id}/

Description: Dieser Endpunkt gibt die Details eines spezifischen Angebots anhand der angegebenen ID zurück.
URL Parameters
Name Type Description
id - Die ID des gewünschten Angebots.
Success Response
Gibt die Details eines spezifischen Angebots, Angebotsdetails und Metadaten zurück. 'user' ist hier die ID des User der dieses Angebot erstellt hat.
{
"id": 66,
"user": 114,
"title": "Grafikdesign-Paket",
"image": null,
"description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
"created_at": "2025-01-23T07:44:15.365773Z",
"updated_at": "2025-01-23T07:44:15.365773Z",
"details": [
{
"id": 199,
"url": "http://127.0.0.1:8000/api/offerdetails/199/"
},
{
"id": 200,
"url": "http://127.0.0.1:8000/api/offerdetails/200/"
},
{
"id": 201,
"url": "http://127.0.0.1:8000/api/offerdetails/201/"
}
],
"min_price": 50,
"min_delivery_time": 5
}
Status Codes
200: Die Anfrage war erfolgreich, die Angebotsdetails wurden zurückgegeben.
401: Benutzer ist nicht authentifiziert
404: Das Angebot mit der angegebenen ID wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein
Extra Information: Die Angebotsdetails enthalten die URLs zu den einzelnen Angebotsdetail-Objekten.

PATCH

/api/offers/{id}/

Description: Aktualisiert ein spezifisches Angebot. Ein PATCH überschreibt nur die angegebenen Felder. Es müssen nicht alle Felder angegeben werden, nur die, die aktualisiert werden sollen.
URL Parameters
Name Type Description
id - Die ID des zu aktualisierenden Angebots.
Request Body
{
"title": "Updated Grafikdesign-Paket",
"details": [
{
"title": "Basic Design Updated",
"revisions": 3,
"delivery_time_in_days": 6,
"price": 120,
"features": [
"Logo Design",
"Flyer"
],
"offer_type": "basic"
}
]
}
Success Response
Gibt das aktualisierte Angebot mit allen Feldern zurück, unabhängig davon, welche Felder in der Anfrage angegeben wurden.
{
"id": 66,
"title": "Updated Grafikdesign-Paket",
"image": null,
"description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
"details": [
{
"id": 199,
"title": "Basic Design Updated",
"revisions": 3,
"delivery_time_in_days": 6,
"price": 120,
"features": [
"Logo Design",
"Flyer"
],
"offer_type": "basic"
},
{
"id": 200,
"title": "Standard Design",
"revisions": 5,
"delivery_time_in_days": 10,
"price": 120,
"features": [
"Logo Design",
"Visitenkarte",
"Briefpapier"
],
"offer_type": "standard"
},
{
"id": 201,
"title": "Premium Design",
"revisions": 10,
"delivery_time_in_days": 10,
"price": 150,
"features": [
"Logo Design",
"Visitenkarte",
"Briefpapier",
"Flyer"
],
"offer_type": "premium"
}
]
}
Status Codes
200: Das Angebot wurde erfolgreich aktualisiert.
400: Ungültige Anfragedaten oder unvollständige Details.
401: Benutzer ist nicht authentifiziert
403: Authentifizierter Benutzer ist nicht der Eigentümer des Angebots
404: Das Angebot mit der angegebenen ID wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Nur Ersteller des Angebotes können dies verändern.
Extra Information: Nur die angegebenen Felder werden aktualisiert. Alle nicht angegebenen Felder bleiben unverändert. Details können einzeln aktualisiert werden, wobei ihre IDs unverändert bleiben müssen. Desweiteren sollte der Typ (offer_type) immer mitgegeben werden, um das Detail eindeutig zu identifizieren.

DELETE

/api/offers/{id}/

Description: Löscht ein spezifisches Angebot anhand der angegebenen ID.
URL Parameters
Name Type Description
id - Die ID des zu löschenden Angebots.
Success Response
Bei Erfolg wird ein HTTP-Statuscode 204 No Content zurückgegeben, ohne Inhalt in der Antwort.
null
Status Codes
204: Das Angebot wurde erfolgreich gelöscht.
401: Benutzer ist nicht authentifiziert
403: Authentifizierter Benutzer ist nicht der Eigentümer des Angebots
404: Das Angebot mit der angegebenen ID wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Nur Ersteller des Angebotes können dies löschen.
Extra Information: Dieser Endpunkt gibt im Erfolgsfall keinen Antwortinhalt zurück, sondern nur den HTTP-Statuscode 204.

GET

/api/offerdetails/{id}/

Description: Ruft die Details eines spezifischen Angebotsdetails ab.
URL Parameters
Name Type Description
id - Die ID des Angebotsdetails, das abgerufen werden soll.
Success Response
Gibt die vollständigen Details des Angebotsdetails zurück, einschließlich Titel, Preis, Lieferzeit, Features und Angebotstyp.
{
"id": 1,
"title": "Basic Design",
"revisions": 2,
"delivery_time_in_days": 5,
"price": 100,
"features": [
"Logo Design",
"Visitenkarte"
],
"offer_type": "basic"
}
Status Codes
200: Das Angebotsdetail wurde erfolgreich abgerufen.
401: Benutzer ist nicht authentifiziert
404: Das Angebotsdetail mit der angegebenen ID wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.
Bestellungen (orders)
Alles an CRUD das für das Frontend eine Rolle spielt

GET

/api/orders/

Description: Gibt eine Liste der Bestellungen zurück, die entweder vom angemeldeten Benutzer als Kunde oder als Geschäftspartner erstellt wurden.
Success Response
Eine Liste von Bestellungen, einschließlich Details wie Kunde, Geschäftspartner, Titel, Status und Erstellungsdatum.
[
{
"id": 1,
"customer_user": 1,
"business_user": 2,
"title": "Logo Design",
"revisions": 3,
"delivery_time_in_days": 5,
"price": 150,
"features": [
"Logo Design",
"Visitenkarten"
],
"offer_type": "basic",
"status": "in_progress",
"created_at": "2024-09-29T10:00:00Z",
"updated_at": "2024-09-30T12:00:00Z"
}
]
Status Codes
200: Die Liste der Bestellungen wurde erfolgreich abgerufen.
401: Benutzer ist nicht authentifiziert.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.
Extra Information: Dieser Endpunkt gibt nur Bestellungen zurück, die mit dem angemeldeten Benutzer entweder als Kunde oder als Geschäftspartner verbunden sind.

POST

/api/orders/

Description: Erstellt eine neue Bestellung basierend auf den Details eines Angebots (OfferDetail).
Request Body
{
"offer_detail_id": 1
}
Success Response
Die erstellte Bestellung wird zurückgegeben, einschließlich Details wie ID, Kunde, Geschäftspartner, Titel, Preis und Status.
{
"id": 1,
"customer_user": 1,
"business_user": 2,
"title": "Logo Design",
"revisions": 3,
"delivery_time_in_days": 5,
"price": 150,
"features": [
"Logo Design",
"Visitenkarten"
],
"offer_type": "basic",
"status": "in_progress",
"created_at": "2024-09-29T10:00:00Z",
"updated_at": "2024-09-30T12:00:00Z"
}
Status Codes
201: Die Bestellung wurde erfolgreich erstellt.
400: Ungültige Anfragedaten (z. B. wenn 'offer_detail_id' fehlt oder ungültig ist).
401: Benutzer ist nicht authentifiziert.
403: Benutzer hat keine Berechtigung, z.B. weil nicht vom typ 'customer'.
404: Das angegebene Angebotsdetail wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein und vom typ 'customer' sein.
Extra Information: Nur Benutzer vom typ 'customer' können Bestellungen erstellen. Der Benutzer gibt eine OfferDetail ID an, und die Bestellung wird auf Grundlage dieses Angebots erstellt. Beachte, dass das Angebot sowohl den Anbieter als auch den Kunden beinhalten muss. Diese Informationen können aus der Authentifizierung und der Offer entnommen werden.

PATCH

/api/orders/{id}/

Description: Aktualisiert den Status einer spezifischen Bestellung. Mögliche Statuswerte sind z.B. 'in_progress', 'completed', oder 'cancelled'.
URL Parameters
Name Type Description
id - Die eindeutige ID der Bestellung, die aktualisiert werden soll.
Request Body
{
"status": "completed"
}
Success Response
Die aktualisierten Details der Bestellung werden zurückgegeben, einschließlich des neuen Status und aktualisierter Timestamps.
{
"id": 1,
"customer_user": 1,
"business_user": 2,
"title": "Logo Design",
"revisions": 3,
"delivery_time_in_days": 5,
"price": 150,
"features": [
"Logo Design",
"Visitenkarten"
],
"offer_type": "basic",
"status": "completed",
"created_at": "2024-09-29T10:00:00Z",
"updated_at": "2024-09-30T15:00:00Z"
}
Status Codes
200: Der Status der Bestellung wurde erfolgreich aktualisiert.
400: Ungültiger Status oder unzulässige Felder in der Anfrage.
401: Benutzer ist nicht authentifiziert.
403: Benutzer hat keine Berechtigung, diese Bestellung zu aktualisieren.
404: Die angegebene Bestellung wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Nur ein Benutzer vom typ 'business' kann den Status einer Bestellung aktualisieren.

DELETE

/api/orders/{id}/

Description: Löscht eine spezifische Bestellung. Diese Aktion ist auf Admin-Benutzer (Staff) beschränkt.
URL Parameters
Name Type Description
id - Die eindeutige ID der zu löschenden Bestellung.
Success Response
Die Antwort enthält keinen Inhalt und zeigt an, dass die Bestellung erfolgreich gelöscht wurde.
null
Status Codes
204: Die Bestellung wurde erfolgreich gelöscht. Keine weiteren Inhalte in der Antwort.
401: Benutzer ist nicht authentifiziert.
403: Benutzer hat keine Berechtigung, die Bestellung zu löschen.
404: Die angegebene Bestellung wurde nicht gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Nur Admin-Benutzer (Staff) dürfen Bestellungen löschen.

GET

/api/order-count/{business_user_id}/

Description: Dieser Endpunkt gibt die Anzahl der laufenden Bestellungen eines bestimmten Geschäftsnutzers (Business User) zurück. Laufende Bestellungen sind solche mit dem Status 'in_progress'.
URL Parameters
Name Type Description
business_user_id - Die eindeutige ID des Geschäftsnutzers, dessen laufende Bestellungen gezählt werden sollen.
Success Response
Die Antwort enthält die Anzahl der laufenden Bestellungen für den angegebenen Geschäftsnutzer.
{
"order_count": 5
}
Status Codes
200: Die Anzahl der laufenden Bestellungen wurde erfolgreich abgerufen.
401: Benutzer ist nicht authentifiziert.
404: Kein Geschäftsnutzer mit der angegebenen ID gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.

GET

/api/completed-order-count/{business_user_id}/

Description: Gibt die Anzahl der abgeschlossenen Bestellungen eines bestimmten Geschäftsnutzers zurück. Abgeschlossene Bestellungen haben den Status 'completed'.
URL Parameters
Name Type Description
business_user_id - Die eindeutige ID des Geschäftsnutzers, dessen abgeschlossene Bestellungen gezählt werden sollen.
Success Response
Die Antwort enthält die Anzahl der abgeschlossenen Bestellungen für den angegebenen Geschäftsnutzer.
{
"completed_order_count": 10
}
Status Codes
200: Die Anzahl der abgeschlossenen Bestellungen wurde erfolgreich abgerufen.
401: Benutzer ist nicht authentifiziert.
404: Kein Geschäftsnutzer mit der angegebenen ID gefunden.
500: Interner Serverfehler.
Rate Limits
No limit
Permissions required: Der Benutzer muss authentifiziert sein.
Bewertungen (reviews)
Alles an CRUD das für das Frontend eine Rolle spielt

GET

/api/reviews/

Description: Listet alle verfügbaren Bewertungen auf. Die Bewertungen können nach 'updated_at' oder 'rating' geordnet werden. Es können auch Filter-Parameter wie 'business_user_id' und 'reviewer_id' verwendet werden.
Query Parameters
Name Type Description
business_user_id integer Die ID des Geschäftsbenutzers, für den Bewertungen gefiltert werden sollen.
reviewer_id integer Die ID des Benutzers, der die Bewertungen erstellt hat.
ordering string Die Sortierreihenfolge der Bewertungen. Mögliche Werte: 'updated_at' oder 'rating'.
Success Response
Die Antwort enthält eine Liste aller Bewertungen, die gefiltert und geordnet werden können.
[
{
"id": 1,
"business_user": 2,
"reviewer": 3,
"rating": 4,
"description": "Sehr professioneller Service.",
"created_at": "2023-10-30T10:00:00Z",
"updated_at": "2023-10-31T10:00:00Z"
},
{
"id": 2,
"business_user": 5,
"reviewer": 3,
"rating": 5,
"description": "Top Qualität und schnelle Lieferung!",
"created_at": "2023-09-20T10:00:00Z",
"updated_at": "2023-09-20T12:00:00Z"
}
]
Status Codes
200: Erfolgreiche Antwort mit der Liste der Bewertungen.
401: Unauthorized. Der Benutzer muss authentifiziert sein.
500: Interner Serverfehler.
Permissions required: Jeder authentifizierte Benutzer kann Bewertungen lesen.

POST

/api/reviews/

Description: Erstellt eine neue Bewertung für einen Geschäftsbenutzer. Nur authentifizierte Benutzer mit einem Kundenprofil dürfen Bewertungen erstellen. Ein Benutzer kann pro Geschäftsprofil nur eine Bewertung abgeben.
Request Body
{
"business_user": 2,
"rating": 4,
"description": "Alles war toll!"
}
Success Response
Erfolgreiche Antwort, die die Details der neu erstellten Bewertung zurückgibt.
{
"id": 3,
"business_user": 2,
"reviewer": 3,
"rating": 4,
"description": "Alles war toll!",
"created_at": "2023-10-30T15:30:00Z",
"updated_at": "2023-10-30T15:30:00Z"
}
Status Codes
201: Erfolgreich erstellt.
400: Fehlerhafte Anfrage. Der Benutzer hat möglicherweise bereits eine Bewertung für das gleiche Geschäftsprofil abgegeben.
401: Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.
403: Forbidden. Ein Benutzer kann nur eine Bewertung pro Geschäftsprofil abgeben.
500: Interner Serverfehler.
Permissions required: Nur authentifizierte Benutzer mit einem Kundenprofil dürfen Bewertungen erstellen. Jeder authentifizierte Benutzer kann Bewertungen lesen.
Extra Information: Dieser Endpunkt erlaubt es Kunden, eine Bewertung für einen Geschäftsbenutzer zu hinterlassen. Eine Bewertung kann nur einmal pro Geschäftsbenutzer abgegeben werden.

PATCH

/api/reviews/{id}/

Description: Aktualisiert ausgewählte Felder einer bestehenden Bewertung (nur 'rating' und 'description' sind editierbar). Der Endpunkt erlaubt es dem Ersteller der Bewertung, die Bewertung zu bearbeiten.
URL Parameters
Name Type Description
id - Die ID der spezifischen Bewertung, die aktualisiert werden soll.
Request Body
{
"rating": 5,
"description": "Noch besser als erwartet!"
}
Success Response
Die Antwort enthält die aktualisierten Details der Bewertung.
{
"id": 1,
"business_user": 2,
"reviewer": 3,
"rating": 5,
"description": "Noch besser als erwartet!",
"created_at": "2023-10-30T10:00:00Z",
"updated_at": "2023-11-01T08:00:00Z"
}
Status Codes
200: Erfolgreich aktualisiert. Die aktualisierte Bewertung wird zurückgegeben.
400: Bad Request. Der Anfrage-Body enthält ungültige Daten.
401: Unauthorized. Der Benutzer muss authentifiziert sein.
403: Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu bearbeiten.
404: Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.
Permissions required: Nur der Ersteller der Bewertung darf diese Aktion durchführen.

DELETE

/api/reviews/{id}/

Description: Löscht eine spezifische Bewertung. Nur der Ersteller der Bewertung können diese Aktion ausführen.
URL Parameters
Name Type Description
id - Die ID der spezifischen Bewertung, die gelöscht werden soll.
Success Response
Die Antwort bestätigt, dass die Bewertung erfolgreich gelöscht wurde.
null
Status Codes
204: Erfolgreich gelöscht. Es wird kein Inhalt zurückgegeben.
401: Unauthorized. Der Benutzer muss authentifiziert sein.
403: Forbidden. Der Benutzer ist nicht berechtigt, diese Bewertung zu löschen.
404: Nicht gefunden. Es wurde keine Bewertung mit der angegebenen ID gefunden.
Permissions required: Nur der Ersteller der Bewertung darf diese Aktion durchführen.
Übergreifende Endpoints
Alle Endpoints die übergreifende z.B. aggregierende Funktionene haben

GET

/api/base-info/

Description: Ruft allgemeine Basisinformationen zur Plattform ab, einschließlich der Anzahl der Bewertungen, des durchschnittlichen Bewertungsergebnisses, der Anzahl der Geschäftsnutzer und der Anzahl der Angebote.
Success Response
Die Antwort enthält statistische Informationen über die Plattform.
{
"review_count": 10,
"average_rating": 4.6,
"business_profile_count": 45,
"offer_count": 150
}
Status Codes
200: Die Basisinformationen wurden erfolgreich abgerufen.
500: Interner Serverfehler.
Rate Limits
No limit
No Permissions required
Extra Information: Die durchschnittliche Bewertung ('average_rating') basiert auf allen abgegebenen Bewertungen und ist auf eine Dezimalstelle gerundet
