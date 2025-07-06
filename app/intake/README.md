<div align="center">
    <h1> Intake App</h1>
</div>

The `intake` app is responsible for tracking food and nutrient consumption by users on a daily basis. It stores the actual intake data — i.e., what a user has eaten, in what quantity, and with what nutritional content.

## Purpose

This app serves as the core source of **actual consumption data**, separate from:

- **Goals**, which represent what the user wants to achieve
- **Measurements**, which reflect outcomes like weight or body changes

By isolating intake into its own app, we establish a clear boundary between *user actions* (e.g., logging food) and *user state* (e.g., current body weight or macro goals).

## Rationale for Separation

- **Domain clarity**: Food intake is a distinct concept from goals or physical measurements.
- **Scalability**: Future features such as meal templates, food tagging, or integration with wearables can be isolated here.
- **API responsibility**: This app owns the `/api/v1/intake/` namespace, making endpoint ownership clear and maintainable.

## Potential Future Expansion

- Support for **meal types** (e.g., breakfast, lunch)
- Relationships to **recipes**, **meal plans**, or **intake patterns**
- Logging **micronutrients** and hydration

**Base API Path:** - `/api/v1/intake/`

