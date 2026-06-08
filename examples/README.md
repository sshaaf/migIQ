# MigIQ Examples

This directory contains example projects and migration scenarios for testing and demonstrating MigIQ capabilities.

## Purpose

- **Testing**: Validate MigIQ skills and workflows
- **Benchmarking**: Measure performance across different project types
- **Documentation**: Show real-world migration examples
- **Development**: Quick test cases for skill development

## Structure

```
examples/
├── spring-boot-to-quarkus/    # Spring Boot → Quarkus migration
├── struts-to-quarkus/         # Apache Struts → Quarkus migration
├── javaee-to-jakarta/         # Java EE → Jakarta EE migration
├── dotnet-modernization/      # .NET Framework → .NET Core/8+ migration
└── rails-upgrade/             # Ruby on Rails version upgrades
```

## Usage

```bash
# Run MigIQ on an example
cd examples/spring-boot-to-quarkus
/migiq "Migrate this Spring Boot application to Quarkus"

# Struts to Quarkus
cd examples/struts-to-quarkus
/migiq "Migrate this Apache Struts application to Quarkus"

# .NET modernization
cd examples/dotnet-modernization
/migiq "Migrate this .NET Framework app to .NET 8"

# Rails upgrade
cd examples/rails-upgrade
/migiq "Upgrade this Rails 5 application to Rails 7"
```

## Note

This directory is **not included** in the npm package. It's for development and testing purposes only.
