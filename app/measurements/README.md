<div align="center">
    <h1> Measurements App </h1>
</div>

The `measurements` app tracks user body-related metrics over time, such as weight. It represents **objective, time-stamped data** about the user's physical state.

## Purpose

While the `intake` app reflects actions (e.g., food consumed) and the `goals` app defines intent (e.g., desired weight), this app captures **measured outcomes** (e.g., current weight).

It’s primarily used to:

- Assess progress
- Visualize trends
- Provide feedback to users

## Rationale for Separation

- **Conceptual boundary**: Physical metrics like weight or body fat are not the same domain as food intake or goals.
- **Data lifecycle**: Measurements may be created manually or pulled from devices like smart scales.
- **Future independence**: We may introduce other types of measurements (e.g., blood pressure, sleep quality) without affecting other apps.

## Potential Future Expansion

- Support for other measurements: **body fat %, waist size, blood pressure**
- **Unit management** and **localization** for user-preferred formats

**Base API Path:** - `/api/v1/measurements/`

