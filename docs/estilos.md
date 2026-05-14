# Sistema de Identidad Visual - Escala Naranja

## 1. Técnica
Se ha implementado un sistema de **Variables CSS (Custom Properties)** centralizado en `:root` para garantizar la coherencia cromática en toda la aplicación. Se utiliza una escala basada en el naranja institucional (#D35400) con variaciones de luminosidad para diferentes estados de UI.

### Variables Principales (Paleta Sobria)
- `--orange-main`: #D35400 (Naranja institucional profundo)
- `--orange-50`: #FFFBF5 (Crema suave para fondos)
- `--orange-100`: #FDF2E9 (Bordes sutiles)
- `--orange-600/700`: #A04000 (Énfasis y contraste alto)

## 2. Elementos Visuales
### Iconografía
- **Icono Principal:** Se utiliza `Icono-1.webp` en la pantalla de login, reemplazando al logo anterior para una estética más moderna y ligera.
- **Botones:** Los botones de acción principal utilizan la clase `.btn-uninpahu-orange`.

## 3. Técnica de Fondo
Para evitar la saturación visual, se utiliza un gradiente naranja extremadamente tenue sobre la fotografía institucional:
```css
linear-gradient(135deg, rgba(211, 84, 0, 0.08), rgba(255, 255, 255, 0.6))
```

## 4. Diagrama de Aplicación de Estilos

```ascii
[ Pantalla Login ]
    |
    +-- [ Icono-1.webp ] --> Animación Hover (scale-105)
    |
    +-- [ Títulos ] -------> Color var(--orange-main)
    |
    +-- [ Inputs ] --------> Fondos Blancos + Bordes Orange-100
```
