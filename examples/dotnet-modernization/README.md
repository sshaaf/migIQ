# .NET Framework to .NET 8 Migration Example

A minimal ASP.NET MVC application demonstrating modernization to .NET 8.

## What's Included

- ASP.NET MVC Controller
- Model with Data Annotations
- Entity Framework DbContext
- App configuration (Web.config)
- Simple views

## Migration Challenges

- ASP.NET MVC → ASP.NET Core MVC
- System.Web dependencies removal
- Entity Framework → EF Core
- Web.config → appsettings.json
- .NET Framework → .NET 8
- Dependency injection patterns
- Middleware pipeline

## Demo Migration

```bash
cd examples/dotnet-modernization
/migiq "Migrate this .NET Framework application to .NET 8"
```

**Expected time:** ~3-4 minutes
