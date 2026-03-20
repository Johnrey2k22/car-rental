# Design System Strategy: The Editorial Concierge

## 1. Overview & Creative North Star
The "Editorial Concierge" is the guiding principle of this design system. We are moving away from the "utility-first" look of standard car rental platforms and toward a high-end travel publication aesthetic. This system treats every vehicle as a featured story and every user interaction as a curated service.

By utilizing **intentional asymmetry**, **over-scaled typography**, and **layered surfaces**, we create a high-trust environment that feels both professional and bespoke. We reject the "boxed-in" layout of traditional templates, instead using breathing room and tonal depth to guide the user’s eye.

## 2. Colors: Tonal Depth & The "No-Line" Rule
The palette is built on a foundation of "Navy-on-Navy" depth and "Amber-on-Light" clarity.

### The "No-Line" Rule
**Explicit Instruction:** You are prohibited from using 1px solid borders to section content. Boundaries must be defined solely through background color shifts or subtle tonal transitions.
- Use `surface-container-low` (#f3f3f3) sections sitting on a `surface` (#f9f9f9) background to define areas.
- For high-impact areas, use `primary_container` (#2a1c00) to create a dark "void" that forces the user to focus on the text.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of fine stationery.
- **Base Layer:** `surface` (#f9f9f9)
- **Secondary Section:** `surface-container-low` (#f3f3f3)
- **Interactive Cards:** `surface-container-lowest` (#ffffff) sitting atop the Secondary Section to create a soft, natural lift.

### Signature Textures & Glass
- **The Amber Glow:** For Primary CTAs, do not use flat hex codes. Apply a subtle linear gradient from `primary_fixed_dim` (#fbbc00) to `on_primary_container` (#ab7f00) at a 135-degree angle. This provides a "metallic" soul to the amber.
- **The Frosted Navigator:** Floating navigation bars should use `surface_container_lowest` at 80% opacity with a `backdrop-filter: blur(12px)`. This integrates the UI into the car imagery behind it.

## 3. Typography: The Editorial Scale
We use a tri-font system to establish authority and modernism.

*   **Display & Headlines (Syne):** Our "Display" scale uses `epilogue` (as per token map) to mimic the Syne-style geometric boldness. Use `display-lg` (3.5rem) for hero car titles. Tighten letter-spacing by -2% for a "premium print" look.
*   **Body Text (Newsreader):** Use `newsreader` for all descriptions. This serif choice signals heritage and high-trust. At `body-lg` (1rem), it ensures high readability for rental terms.
*   **Metadata & Labels (DM Mono):** Represented by the `inter` tokens in the scale, these should be treated as "technical data." Use `label-md` for car specs (e.g., "AUTOMATIC," "DIESEL") to provide a functional contrast to the elegant serif body text.

## 4. Elevation & Depth: Tonal Layering
Avoid the "Shadow Gallery" look. Depth should feel like ambient light in a showroom.

*   **The Layering Principle:** Rather than adding a shadow to a card, change its surface. Place a `surface_container_lowest` (#ffffff) card on a `surface_dim` (#dadada) background. The contrast creates the "lift."
*   **Ambient Shadows:** If a floating element (like a booking modal) requires a shadow, use: `box-shadow: 0 20px 40px rgba(0, 31, 63, 0.06)`. Note the use of the Navy primary color in the shadow tint rather than pure black.
*   **The Ghost Border:** If accessibility requires a stroke (e.g., in a high-glare environment), use the `outline_variant` token at 15% opacity. It should be felt, not seen.

## 5. Components

### Primary CTA (The Amber Button)
- **Style:** Pill-shaped (`rounded-full`). 
- **Color:** Gradient from `primary_fixed_dim` to `primary_fixed`.
- **Label:** `label-md` (All Caps, 0.05em tracking).
- **Interaction:** On hover, shift the gradient density rather than changing the color to a flat shade.

### Vehicle Selection Cards
- **Forbid Dividers:** Do not use lines between the car image and the specs.
- **Structure:** Use a `surface-container-lowest` card. Use a `3` (0.75rem) padding scale for internal grouping and a `10` (2.5rem) margin to separate cards.
- **The "Hero" Shift:** The selected car card should not get a border; it should transition to `secondary_container` (#bdd6ff) with `on_secondary_container` (#445d80) text.

### Input Fields
- **State:** `surface_container_high` background.
- **Active State:** Instead of a thick border, use a 2px bottom-bar in `primary_fixed_dim` (#fbbc00).
- **Labels:** Always `label-sm` in `on_surface_variant`.

### Search & Filter Chips
- **Style:** `rounded-md` (0.375rem).
- **Unselected:** `surface_variant` with `on_surface_variant`.
- **Selected:** `primary` (#0a0500) background with `on_primary` (#ffffff) text.

## 6. Do's and Don'ts

### Do
- **Use Asymmetric Grids:** Align your car imagery to the far right bleed while keeping text content in a centered 8-column container.
- **Embrace White Space:** Use the `16` (4rem) and `20` (5rem) spacing tokens between major sections. If it feels "too empty," you are doing it right.
- **Tint your Grays:** Ensure "Light Gray" areas always lean slightly cool to complement the Navy primary.

### Don't
- **Don't use 100% Black:** Use `primary` (#0a0500) for text. It’s softer and feels more expensive.
- **Don't use Box Shadows on everything:** Let the background color shifts do the work of defining hierarchy.
- **Don't use Standard Sans-Serif for Body:** Stick to the Newsreader serif. A sans-serif body will immediately collapse the "High-End Editorial" look into a generic SaaS template.