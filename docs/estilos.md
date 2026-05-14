# Guía de Estilos UNINPAHU (Premium)

La interfaz utiliza el lenguaje visual **Soft Peach**, caracterizado por tonos cálidos, superficies traslúcidas y retroalimentación sensorial.

## 🎨 Paleta de Colores
- **Naranja Principal (`--orange-main`):** `#FF7043` - Identidad institucional activa.
- **Crema Melocotón (`--orange-soft`):** `#FFF5F2` - Fondo de tarjetas y contenedores.
- **Borde Melocotón (`--orange-border`):** `#FFE0D6` - Delimitación sutil.
- **Resplandor Naranja (`--orange-glow`):** `rgba(255, 112, 67, 0.3)` - Efectos de enfoque.

## 🪟 Arquitectura Glassmorphism
Los paneles principales utilizan la clase `.glass-card`:
- **Fondo:** `rgba(255, 255, 255, 0.75)`
- **Efecto:** `blur(12px) saturate(160%)`
- **Interactividad:** Efecto **Tilt 3D** en hover para sensación de profundidad física.

## ❄️ Fondo Institucional (Marca de Agua)
El fondo base (`body::before`) está configurado para ser nítido pero sutil:
- **Opacidad:** Gradiente melocotón al 65%-80% sobre la foto institucional.
- **Filtros:** `saturate(1.6) contrast(1.1)` para elevar los colores originales de la foto sin competir con el texto.

## 🎬 Animaciones
- **PWA-Transition:** Fade-out al cambiar de página para eliminar parpadeos bruscos.
- **QR-Laser:** Línea de escaneo animada sobre el QR para indicar actividad en tiempo real.
- **Skeletons:** Carga suave de datos mediante shimmer dinámico, evitando saltos de contenido.

## 🔊 Feedback Sensorial
- **Audio:** Tono de éxito (`880Hz`) al completar registros.
- **Háptico:** Vibración breve en dispositivos móviles compatibles para confirmación de escaneo.
