# Guía de Importación de Datos (Excel)

El sistema UNINPAHU Asistencia permite la migración masiva de datos académicos desde archivos institucionales de Excel, automatizando la creación de usuarios, materias, grupos y horarios.

## 📁 Archivo de Origen
- **Formato:** `.xls` (Libro de Excel 97-2003) - Formato OLE2.
- **Estructura Requerida:** El script mapea dinámicamente las columnas basándose en sus encabezados.

## 🛠️ Columnas Clave para el Mapeo
| Encabezado Excel | Destino en Sistema |
| :--- | :--- |
| `NUMERO_DOC` | **Username (Login)** |
| `NOMBRE_COMPLETO` | Nombre del Estudiante |
| `NUMERO_DOC_DOCENTE` | **Login del Docente** |
| `NOMBRE_COMPLETO_PROFESOR` | Nombre del Docente |
| `CODIGO_MATERIA` | Identificador de Asignatura |
| `DIA_SEMANA` | Mapeo automático (Lunes -> M, Martes -> T, etc.) |
| `HORA_INICIAL` / `HORA_FINAL` | Bloques de horario académico |
| `FECHA_INICIAL` / `FECHA_FINAL` | Vigencia del semestre |

## 🚀 Proceso de Ejecución
1. Coloca el archivo Excel en la raíz del proyecto.
2. Asegúrate de tener instalada la librería `xlrd`:
   ```bash
   pip install xlrd==2.0.1
   ```
3. Ejecuta el script de migración:
   ```bash
   python Backend/import_data.py
   ```

## 🔒 Reglas de Negocio en la Importación
- **Contraseña por Defecto:** Todos los usuarios creados tendrán la contraseña `123` inicialmente.
- **Detección de Duplicados:** El script utiliza sentencias `INSERT OR IGNORE`, evitando duplicar estudiantes que están matriculados en múltiples materias.
- **Normalización de Horas:** Convierte formatos de hora decimales de Excel (ej: 0.75) a formato de 24 horas (18:00).
- **Relaciones:** Crea automáticamente el vínculo entre el Estudiante -> Inscripción -> Grupo -> Materia.
