# MigIQ Demo Guide

Quick reference for demonstrating MigIQ capabilities using the example projects.

## Overview

All examples are designed for **sub-5-minute demos** showing real-world migration scenarios.

## Example Projects

### 1. Spring Boot → Quarkus (8 files, ~3-4 min)
**Path:** `examples/spring-boot-to-quarkus`

**Shows:**
- Spring annotations → Quarkus/Jakarta EE
- Spring Data JPA → Panache
- REST controller migration
- Dependency injection changes
- Configuration properties migration

**Demo command:**
```bash
cd examples/spring-boot-to-quarkus
/migiq "Migrate this Spring Boot application to Quarkus"
```

**Key files to highlight:**
- `src/main/java/com/example/demo/controller/ProductController.java` - REST endpoints
- `src/main/java/com/example/demo/repository/ProductRepository.java` - Spring Data JPA
- `src/main/resources/application.properties` - Configuration

---

### 2. Apache Struts → Quarkus (7 files, ~3-4 min)
**Path:** `examples/struts-to-quarkus`

**Shows:**
- Legacy Struts Actions → Modern JAX-RS
- struts.xml → Annotation-based routing
- JSP/Struts tags → Modern templating
- Form handling modernization

**Demo command:**
```bash
cd examples/struts-to-quarkus
/migiq "Migrate this Apache Struts application to Quarkus"
```

**Key files to highlight:**
- `src/main/java/com/example/struts/action/UserAction.java` - Struts Action class
- `src/main/resources/struts.xml` - XML-based routing
- `src/main/webapp/WEB-INF/jsp/users.jsp` - JSP with Struts tags

---

### 3. Java EE → Jakarta EE (7 files, ~2-3 min)
**Path:** `examples/javaee-to-jakarta`

**Shows:**
- `javax.*` → `jakarta.*` namespace migration
- EJB and JAX-RS updates
- persistence.xml updates
- Bean Validation changes

**Demo command:**
```bash
cd examples/javaee-to-jakarta
/migiq "Migrate this Java EE 8 application to Jakarta EE 10"
```

**Key files to highlight:**
- `src/main/java/com/example/javaee/rest/BookResource.java` - JAX-RS endpoint
- `src/main/java/com/example/javaee/service/BookService.java` - EJB stateless bean
- `src/main/resources/META-INF/persistence.xml` - JPA configuration

---

### 4. .NET Framework → .NET 8 (6 files, ~3-4 min)
**Path:** `examples/dotnet-modernization`

**Shows:**
- ASP.NET MVC → ASP.NET Core
- Entity Framework → EF Core
- Web.config → appsettings.json
- System.Web dependency removal

**Demo command:**
```bash
cd examples/dotnet-modernization
/migiq "Migrate this .NET Framework application to .NET 8"
```

**Key files to highlight:**
- `Controllers/CustomersController.cs` - MVC controller with EF
- `Data/ApplicationDbContext.cs` - Entity Framework DbContext
- `Web.config` - Legacy configuration

---

### 5. Rails 5 → Rails 7 (10 files, ~3-4 min)
**Path:** `examples/rails-upgrade`

**Shows:**
- Rails version upgrade patterns
- ActiveRecord query updates
- Classic autoloader → Zeitwerk
- Gem dependency updates
- Migration version changes

**Demo command:**
```bash
cd examples/rails-upgrade
/migiq "Upgrade this Rails 5 application to Rails 7"
```

**Key files to highlight:**
- `app/controllers/articles_controller.rb` - REST controller
- `app/models/article.rb` - ActiveRecord model with scopes
- `config/application.rb` - Classic autoloader configuration
- `Gemfile` - Rails 5 dependencies

---

## Demo Tips

### Quick Demo Flow (5 minutes)

1. **Show the code** (30 sec)
   - Open 2-3 key files showing legacy patterns
   - Point out migration challenges (annotations, imports, config)

2. **Run MigIQ** (2-3 min)
   ```bash
   /migiq "Migrate [from] to [target]"
   ```
   - MigIQ analyzes with mig-rgctl / rgctl
   - Generates migration plan
   - Shows task breakdown

3. **Review output** (1-2 min)
   - Compare before/after code
   - Highlight intelligent transformations
   - Show preserved business logic

### What Makes This Better Than Static Analysis

**Point out during demo:**
- ✅ No pre-written rules needed
- ✅ Understands context, not just syntax
- ✅ Handles edge cases through reasoning
- ✅ Preserves business logic and intent
- ✅ Knowledge graph shows full dependency impact

### One-Line Pitch Per Example

- **Spring Boot → Quarkus**: "Watch MigIQ transform Spring annotations to Quarkus while preserving your business logic"
- **Struts → Quarkus**: "See how MigIQ modernizes a 15-year-old Struts app to cloud-native Quarkus"
- **Java EE → Jakarta**: "MigIQ handles the tedious javax→jakarta namespace migration across your entire codebase"
- **.NET Modernization**: "Watch MigIQ navigate the complex .NET Framework to .NET 8 upgrade path"
- **Rails Upgrade**: "MigIQ intelligently upgrades Rails apps while handling deprecations and API changes"

## File Count Summary

- **Total:** 38 files across 5 projects
- Each example: 6-10 files (perfect for quick demos)
- All examples: Minimal but realistic code
