# 📈 Control de Inversiones — Depósitos a Plazo

Sistema web construido con **Django** para registrar, monitorear y visualizar depósitos a plazo (DAP) distribuidos en distintos bancos. Incluye un dashboard con gráficos interactivos de flujo de caja mensual y distribución de capital por institución financiera.

---

## ✨ Funcionalidades

- **Registro de DAPs** con banco, número de operación, capital, tasa anual, fecha de inicio y vencimiento.
- **Cálculo automático** de:
  - Días de inversión
  - Interés ganado (base 360 días)
  - Monto final a recibir
- **Dashboard visual** con:
  - Gráfico de barras del flujo de caja mensual por vencimientos
  - Gráfico de torta con la distribución porcentual del capital por banco
  - Tabla de flujo mensual agrupado
- **Indicadores clave** en tiempo real:
  - Capital total invertido
  - Interés total ganado
  - Monto a vencer en los próximos 30 días
- **Panel de administración** Django con filtros por banco y fecha de vencimiento, y búsqueda por número de operación.

---

## 🛠️ Tecnologías

| Componente | Tecnología |
|---|---|
| Backend | Django 6.0.4 |
| Base de datos | SQLite3 |
| Visualización | Matplotlib 3.10 |
| Análisis de datos | Pandas 3.0 |
| Variables de entorno | python-dotenv 1.2 |
| Lenguaje | Python 3.x |

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <https://github.com/ramirousnayo/control-inversiones-django.git>
cd control_inversiones
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
```

> Para generar una `SECRET_KEY` segura desde Python:
> ```python
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (para el panel admin)

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

---

## 🌐 URLs disponibles

| Ruta | Descripción |
|---|---|
| `http://127.0.0.1:8000/dashboard/` | Dashboard con gráficos e indicadores |
| `http://127.0.0.1:8000/admin/` | Panel de administración Django |

---

## 📁 Estructura del Proyecto

```
control_inversiones/
├── depositos/
│   ├── migrations/
│   ├── templates/
│   │   └── depositos/
│   │       └── dashboard.html
│   ├── admin.py          # Configuración del panel admin
│   ├── models.py         # Modelos Banco y DepositoPlazo
│   ├── urls.py           # Rutas de la app
│   └── views.py          # Vista dashboard con gráficos
├── inversiones/
│   ├── settings.py       # Configuración del proyecto
│   ├── urls.py           # Rutas principales
│   └── wsgi.py
├── .env                  # Variables de entorno (no incluido en Git)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 📐 Modelo de Datos

### `Banco`
| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | CharField | Nombre de la institución financiera |

### `DepositoPlazo`
| Campo | Tipo | Descripción |
|---|---|---|
| `banco` | ForeignKey | Banco asociado |
| `numero_operacion` | CharField | Identificador único del DAP |
| `fecha_inicio` | DateField | Fecha de contratación |
| `fecha_vencimiento` | DateField | Fecha de término |
| `capital` | DecimalField | Monto invertido |
| `tasa_anual` | DecimalField | Tasa de interés anual (%) |

**Métodos calculados:**
- `dias_inversion()` → días entre inicio y vencimiento
- `interes_ganado()` → `capital × (tasa / 100) × días / 360`
- `monto_final()` → `capital + interes_ganado()`

---

## 🔒 Seguridad

- La `SECRET_KEY` y el modo `DEBUG` se cargan desde el archivo `.env` mediante `python-dotenv`.
- El archivo `.env` está excluido del control de versiones vía `.gitignore`.
- **Nunca subas tu `.env` a Git.**

---

## 🌍 Localización

Configurado para Chile:
- `LANGUAGE_CODE = 'es-cl'`
- `TIME_ZONE = 'America/Santiago'`
