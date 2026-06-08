# Java EE to Jakarta EE Migration Example

A minimal Java EE application demonstrating namespace and API migration.

## What's Included

- EJB stateless session bean
- JAX-RS REST endpoint
- JPA entity with bean validation
- CDI managed bean
- persistence.xml configuration

## Migration Challenges

- `javax.*` → `jakarta.*` namespace changes
- EJB annotations update
- JAX-RS API migration
- JPA/Hibernate compatibility
- Bean Validation updates
- Dependency updates in pom.xml

## Demo Migration

```bash
cd examples/javaee-to-jakarta
/migiq "Migrate this Java EE 8 application to Jakarta EE 10"
```

**Expected time:** ~2-3 minutes
