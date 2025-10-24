---
applyTo: **
description: actually learning
---
- Aim for Turing’s and Dijkstra’s level of rigor and clarity. 
- Donald Knuth’s understanding and detail.
- Uncle Bob’s Martin’s rigor.
- Martin Fowler’s insight.
- Hejlsberg’s focus on strong typing and developer productivity.
- When debugging, strive for Hopper’s exactness and practicality.
- Provide clear explanations for corrections.
- Suggest potential solutions I didn’t mention or ask for.
- Be proactive and anticipate alternative solutions to problems.
- Explain complex topics in a simple, understandable manner, as would Sagan or Feynman.
- Tell it like it is don't sugar-coat responses. Take a forward-thinking view.
- This is Order service named "Basuketto" microservice.
- This service responsible for CRUD operations, apply coupons, discounts on basket.
- When order created, service will fire order.created event to AWS SQS follows pub/sub pattern.
- Service has 3 three tables. Order, Shopping Cart, Promo.
- Service should highly available, priotizing availability over consistency.
    1. Cart → AP system (available, partition-tolerant, weaker durability).
    2. Order → CP system (consistent, durable).

## Durability importance:

- Low for cart, moderate for promo, high for order.
- Service able to scale to support 100 DAU(Daily Average Users)
- Prioritize write scalability (event sourcing, or CQRS).
- Add read replicas or caches to offload lookups if needed.  
    - If you apply CQRS:
        - Command side (Order, Cart) scales for writes.  
        - Query side (Promo lookups, Order summaries) scales for reads.

## Fault Tolerance
High importance, but **scope-dependent**.

Breakdown by function:

1. **Order Service (Coordinator)**

   * **High fault tolerance needed.**
   * If it fails during orchestration (between payment and inventory), you risk dangling states — e.g., charged but not ordered.
   * Implement:
     * Persistent event log or outbox.
     * Idempotent message processing.
     * Retry with backoff and deduplication.
     * Stateless workers + persistent queue (Kafka, SQS).
     * Leader election or distributed scheduler if using timers (e.g., order expiration).

2. **Cart Service (Volatile state)**

   * **Medium fault tolerance.**
   * Outage should degrade gracefully — user can re-add items.
   * In-memory caches (Redis) can use replication but not strict durability.
   * Focus on **availability**, not full recovery.

3. **Promo Service (Cache-heavy)**

   * **Low-to-medium fault tolerance.**
   * If promo validation fails temporarily, fallback logic or retry later.
   * Replicate or cache promos globally for low latency.

## Core Entities

Order Service core:  Order, Cart, Promo  
External references: User (via ID), Product (via ID), Payment (via ID or transaction token)

