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
- Sol·licituds de digitalització
- Productes
- Comandes
- etc...

### 2. Sistema d'Usuaris 👤
Tenim dos tipus d'usuaris:
- **Administradors**: Gestionen sol·licituds i botigues
- **Clients**: Poden sol·licitar digitalització i gestionar la seva botiga

#### Com funciona el registre i login?
1. **Registre** (`/api/registro/`):
   - Pots crear un compte nou
   - Has de posar email, contrasenya i rol (admin o client)
   - L'email ha de ser únic

2. **Login** (`/api/login/`):
   - Poses el teu email i contrasenya
   - Si són correctes, pots començar a fer servir l'API

[Espai per captura de pantalla del login exitós]

### 3. Sistema de Sol·licituds 📝
Hem implementat un sistema complet per gestionar sol·licituds de digitalització:

#### Com funciona?
1. Un comerciant envia una sol·licitud (no cal estar registrat)
2. Els admins reben la sol·licitud i la revisen
3. Poden acceptar-la o rebutjar-la
4. Si s'accepta, es crea un compte pel comerciant

#### Endpoints de Sol·licituds:

1. **Crear Sol·licitud** (`POST /api/solicitudes/crear/`):
   - No requereix autenticació
   - Qualsevol pot sol·licitar digitalització
   ```json
   {
       "nombre_negocio": "La Meva Botiga",
       "descripcion": "Vull vendre online",
       "email_contacto": "botiga@exemple.com",
       "telefono": "123456789"
   }
   ```
   [Espai per captura de pantalla de sol·licitud creada]

2. **Llistar Sol·licituds** (`GET /api/solicitudes/`):
   - Només accessible per admins
   - Mostra totes les sol·licituds ordenades per data
   - Inclou l'estat de cada sol·licitud

   [Espai per captura de pantalla del llistat]

3. **Veure Sol·licitud** (`GET /api/solicitudes/{id}/`):
   - Només accessible per admins
   - Mostra tots els detalls d'una sol·licitud
   - Inclou notes internes si n'hi ha

   [Espai per captura de pantalla dels detalls]

4. **Actualitzar Sol·licitud** (`PUT /api/solicitudes/{id}/`):
   - Només accessible per admins
   - Permet canviar l'estat i afegir notes
   ```json
   {
       "estado": "aceptada",  // o "rechazada"
       "notas_admin": "Client interessant"
   }
   ```
   [Espai per captura de pantalla d'actualització]

### 4. Sistema de Botigues 🏪
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

### 5. Sistema de Serveis 📈
Hem creat els endpoints per gestionar serveis:

#### Endpoints de Serveis:

1. **Llistar Serveis** (`GET /api/servicios/`):
   - Tothom pot veure els serveis actius
   - Els admins veuen tots els serveis
   ```json
   [
     {
       "nombre": "Web Bàsica",
       "descripcion": "Web responsive amb 5 seccions",
       "precio": 599.99
     }
   ]
   ```

2. **Contractar Servei** (`POST /api/tiendas/{id}/servicios/`):
   - Cal estar autenticat com a propietari de la botiga
   ```json
   {
     "servicio_id": 1,
     "notas": "Vull afegir una secció de blog"
   }
   ```

### 6. Sistema de Pagaments 💸
Hem creat els endpoints per gestionar pagaments:

#### Endpoints de Pagaments:

1. **Crear Pagament** (`POST /api/pagos/`):
   ```json
   {
     "tienda_servicio": 1,
     "metodo_pago": "tarjeta",
     "monto": 599.99
   }
   ```

### 7. Sistema de Suport 🤝
He afegit un sistema de tickets per si els clients necessiten ajuda:

#### Endpoints de Suport:

1. **Crear Ticket** (`POST /api/soporte/`):
   ```json
   {
     "asunto": "Dubte sobre la web",
     "mensaje": "Quan estarà llesta?"
   }
   ```

2. **Respondre Ticket** (`PATCH /api/soporte/{id}/`):
   - Només admins poden respondre
   ```json
   {
     "estado": "resuelto",
     "respuesta": "En unes 2 setmanes estarà llesta"
   }
   ```

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

### 3. Si ets admin, revisa les sol·licituds:
```json
GET /api/solicitudes/
```

### 4. Processa una sol·licitud:
```json
PUT /api/solicitudes/1/
{
    "estado": "aceptada",
    "notas_admin": "Bon candidat per digitalitzar"
}
```

## 🚧 Què falta per fer?
1. Implementar el frontend
2. Més coses que anirem veient! 😊

## 💡 Consells
- Fes servir Postman per provar els endpoints
- Guarda't els endpoints que més facis servir
- Si tens dubtes, pregunta! 🙋‍♂️

## 📚 Detalls Tècnics
### Model de Sol·licitud
```python
class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada')
    ]
    
    nombre_negocio = models.CharField(max_length=200)
    descripcion = models.TextField()
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(choices=ESTADO_CHOICES, default='pendiente')
    notas_admin = models.TextField(blank=True, null=True)
```

### Sistema de Permisos
- Les sol·licituds es poden crear sense autenticació
- Només els admins poden veure i gestionar sol·licituds
- Implementat amb permisos personalitzats de Django Rest Framework