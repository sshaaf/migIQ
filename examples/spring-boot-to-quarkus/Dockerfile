# Multi-stage Dockerfile for Quarkus Application
# Base: Red Hat Universal Base Image (UBI) 9 with OpenJDK 17

# Stage 1: Build
FROM registry.access.redhat.com/ubi9/openjdk-17:latest AS builder

# Set working directory
WORKDIR /build

# Copy Maven files
COPY pom.xml .
COPY src ./src

# Build the application (skip tests - they ran in CI)
# Quarkus creates quarkus-app/ directory structure
USER root
RUN mvn clean package -DskipTests

# Verify build output
RUN ls -la /build/target/quarkus-app/

# Stage 2: Runtime
FROM registry.access.redhat.com/ubi9/openjdk-17-runtime:latest

# Metadata labels
LABEL maintainer="MigIQ Team" \
      description="Quarkus Product API migrated from Spring Boot" \
      version="1.0.0" \
      io.openshift.tags="quarkus,java,rest-api" \
      io.k8s.description="Product management REST API built with Quarkus" \
      io.openshift.expose-services="8080:http"

# Set working directory
WORKDIR /deployments

# Security: Run as non-root user (185 is default jboss user in UBI Java images)
USER 185

# Copy Quarkus application from builder stage
# Quarkus fast-jar format: quarkus-app/ directory structure
COPY --from=builder --chown=185:0 /build/target/quarkus-app/lib/ /deployments/lib/
COPY --from=builder --chown=185:0 /build/target/quarkus-app/*.jar /deployments/
COPY --from=builder --chown=185:0 /build/target/quarkus-app/app/ /deployments/app/
COPY --from=builder --chown=185:0 /build/target/quarkus-app/quarkus/ /deployments/quarkus/

# Externalize configuration via environment variables
# These override application.properties at runtime
ENV QUARKUS_HTTP_PORT=8080 \
    QUARKUS_LOG_LEVEL=INFO \
    QUARKUS_LOG_CATEGORY_COM_EXAMPLE_DEMO=DEBUG

# Quarkus JVM mode optimization flags
ENV JAVA_OPTS="-Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"
ENV JAVA_APP_JAR="/deployments/quarkus-run.jar"

# Expose HTTP port
EXPOSE 8080

# Health check using Quarkus health endpoints
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/q/health/ready || exit 1

# Run Quarkus application
# The quarkus-run.jar is the runner JAR that loads the application
ENTRYPOINT ["java", "-jar", "/deployments/quarkus-run.jar"]
