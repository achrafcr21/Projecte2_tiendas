# 🏪 Projecte de Digitalització de Botigues

Hola! 👋 Aquest és el nostre projecte de digitalització de botigues. L'objectiu és ajudar a petits comerciants a tenir presència online.

## 📱 Què estem fent?

Estem creant:
- Una API amb Django Rest Framework (pel backend)
- Una web pels administradors (per gestionar les botigues)
- Una app mòbil pels clients (per comprar productes)

## 🛠️ Què tenim fet fins ara?

### 1. Base de Dades
Hem creat totes les taules necessàries a MySQL:
- Usuaris (per guardar admins i clients)
- Botigues
- Productes
- Comandes
- etc...

### 2. Sistema d'Usuaris 👤
Tenim dos tipus d'usuaris:
- **Administradors**: Poden crear i gestionar botigues
- **Clients**: Poden comprar productes i fer comandes

#### Com funciona el registre i login?
1. **Registre** (`/api/registro/`):
   - Pots crear un compte nou
   - Has de posar email, contrasenya i rol (admin o client)
   - L'email ha de ser únic

2. **Login** (`/api/login/`):
   - Poses el teu email i contrasenya
   - Si són correctes, pots començar a fer servir l'API

### 3. Sistema de Botigues 🏪
Hem creat els endpoints per gestionar botigues:

#### Endpoints de Botigues:
1. **Veure totes les botigues** (`GET /api/tiendas/`):
   - Qualsevol usuari registrat pot veure la llista
   - No cal ser admin

2. **Crear botiga** (`POST /api/tiendas/`):
   - Només els admins poden crear botigues
   - La botiga es crea amb l'admin com a propietari
   - Has d'enviar: nom i descripció de la botiga

3. **Veure una botiga** (`GET /api/tiendas/{id}/`):
   - Tothom pot veure els detalls
   - Poses l'ID de la botiga a la URL

4. **Modificar botiga** (`PUT /api/tiendas/{id}/`):
   - Només el propietari (admin que la va crear) pot modificar-la
   - Pots canviar el nom i la descripció

5. **Eliminar botiga** (`DELETE /api/tiendas/{id}/`):
   - Només el propietari pot eliminar la seva botiga

## 📝 Com provar els endpoints?

### 1. Primer, registra't:
```json
POST /api/registro/
{
    "email": "el_teu_email@exemple.com",
    "password": "la_teva_contrasenya",
    "rol": "admin"  // o "cliente" si vols ser client
}
```

### 2. Fes login:
```json
POST /api/login/
{
    "email": "el_teu_email@exemple.com",
    "password": "la_teva_contrasenya"
}
```

### 3. Si ets admin, pots crear una botiga:
```json
POST /api/tiendas/
{
    "nombre": "La Meva Botiga",
    "descripcion": "Una botiga molt xula"
}
```

## 🚧 Què falta per fer?
1. Implementar el sistema de productes
2. Fer el sistema de comandes
3. Afegir el carret de la compra
4. Més coses que anirem veient! 😊

## 💡 Consells
- Fes servir Postman per provar els endpoints
- Guarda't els endpoints que més facis servir
- Si tens dubtes, pregunta! 🙋‍♂️