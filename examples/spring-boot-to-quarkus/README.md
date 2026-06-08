# Spring Boot to Quarkus Migration Example

A minimal Spring Boot REST API demonstrating typical migration patterns.

## What's Included

- REST controller with CRUD operations
- JPA entity and repository
- Service layer with dependency injection
- Application properties configuration
- Maven POM with Spring Boot dependencies

## Migration Challenges

- Spring annotations → Quarkus/Jakarta EE
- Spring Data JPA → Panache
- Spring Boot properties → Quarkus configuration
- Spring Web → JAX-RS
- Dependency injection differences

## Demo Migration

```bash
cd examples/spring-boot-to-quarkus
/migiq "Migrate this Spring Boot application to Quarkus"
```

**Expected time:** ~3-4 minutes
