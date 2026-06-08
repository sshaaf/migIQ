# Apache Struts to Quarkus Migration Example

A minimal Struts 2 web application demonstrating typical migration patterns.

## What's Included

- Struts Action class with form handling
- JSP view with Struts tags
- Struts configuration (struts.xml)
- Model object with validation
- Web.xml configuration

## Migration Challenges

- Struts Actions → JAX-RS Resources
- Struts interceptors → CDI interceptors
- JSP + Struts tags → Qute templates or frontend framework
- struts.xml → Quarkus annotations
- Form validation → Bean Validation
- Session management patterns

## Demo Migration

```bash
cd examples/struts-to-quarkus
/migiq "Migrate this Apache Struts application to Quarkus"
```

**Expected time:** ~3-4 minutes
