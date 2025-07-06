<div align="center">
    <h1> Goals App </h1>
</div>

The `goals` app defines **user-intended targets** related to nutrition and body metrics. It serves as the authoritative source for where the user wants to be — for example, setting a desired daily calorie intake or a goal weight by a specific date.

## Purpose

This app exists to capture **user-defined objectives** that the system can measure progress against. Unlike `intake`, which reflects logged behavior, or `measurements`, which reflect outcomes, `goals` focuses on **intent**.

| Concept         | Example                          | Category | Description                                         |
| --------------- | -------------------------------- | -------- | --------------------------------------------------- |
| **Goal**        | *"I want to weigh 70kg by Sept"* | Intent   | User’s future target or desired state.              |
| **Intake**      | *"I ate 2100 kcal today"*        | Behavior | User’s actual actions and inputs (food, nutrition). |
| **Measurement** | *"Today I weigh 74.2kg"*         | Outcome  | An objective snapshot of the user’s current state.  |


This clear separation ensures that:

- Data about *what the user wants* is cleanly decoupled from *what the user does* or *what the user is*.
- The system can compute progress (e.g., % of goal calories reached) without tightly coupling logic between apps.

## Rationale for Separation

- **Intent vs behavior**: Goals represent future-oriented targets, not past actions.
- **Modularity**: Goals may evolve into a user-planning system, with scheduling and recommendations.
- **Scope clarity**: Keeping this in a separate app allows its schema and logic to remain focused and extensible.

## Potential Future Expansion

- Add support for **non-nutrition goals**, such as sleep or exercise

**Base API Path:** - `/api/v1/goals/`
