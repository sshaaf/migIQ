package com.example.demo.controller;

import com.example.demo.model.Product;
import io.quarkus.test.junit.QuarkusTest;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.junit.jupiter.api.Order;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.*;
import static org.hamcrest.Matchers.greaterThan;

/**
 * Integration tests for ProductController REST API
 * Priority 1: God Node (6 edges)
 * Coverage Target: 95%+ (Public API)
 *
 * Tests all 5 REST endpoints with full request/response validation
 */
@QuarkusTest
@TestMethodOrder(OrderAnnotation.class)
public class ProductControllerTest {

    /**
     * Test 1: GET /api/products - Get all products
     * Expected: HTTP 200, JSON array
     */
    @Test
    @Order(1)
    public void testGetAllProducts_returnsEmptyList() {
        given()
            .when()
                .get("/api/products")
            .then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("size()", is(0));
    }

    /**
     * Test 2: POST /api/products - Create a product
     * Expected: HTTP 200, product with generated ID
     */
    @Test
    @Order(2)
    public void testCreateProduct_returnsCreatedProduct() {
        Product product = new Product();
        product.setName("Test Product");
        product.setDescription("A test product for validation");
        product.setPrice(29.99);

        given()
            .contentType(ContentType.JSON)
            .body(product)
            .when()
                .post("/api/products")
            .then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("name", is("Test Product"))
                .body("description", is("A test product for validation"))
                .body("price", is(29.99f))
                .body("id", notNullValue());
    }

    /**
     * Test 3: GET /api/products - Get all products (after creation)
     * Expected: HTTP 200, non-empty JSON array
     */
    @Test
    @Order(3)
    public void testGetAllProducts_returnsNonEmptyList() {
        given()
            .when()
                .get("/api/products")
            .then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("size()", greaterThan(0));
    }

    /**
     * Test 4: GET /api/products/{id} - Get product by ID
     * Expected: HTTP 200, product matches
     */
    @Test
    @Order(4)
    public void testGetProductById_whenExists_returnsProduct() {
        // Create a product first
        Product product = new Product();
        product.setName("Product for GET test");
        product.setDescription("Description");
        product.setPrice(19.99);

        Integer productId = given()
            .contentType(ContentType.JSON)
            .body(product)
            .when()
                .post("/api/products")
            .then()
                .statusCode(200)
                .extract()
                .path("id");

        // Now get it by ID
        given()
            .when()
                .get("/api/products/" + productId)
            .then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("id", is(productId))
                .body("name", is("Product for GET test"))
                .body("description", is("Description"))
                .body("price", is(19.99f));
    }

    /**
     * Test 5: GET /api/products/{id} - Get product by ID (not found)
     * Expected: HTTP 404
     */
    @Test
    @Order(5)
    public void testGetProductById_whenNotExists_returns404() {
        given()
            .when()
                .get("/api/products/99999")
            .then()
                .statusCode(404);
    }

    /**
     * Test 6: GET /api/products/search?name= - Search products
     * Expected: HTTP 200, filtered results
     */
    @Test
    @Order(6)
    public void testSearchProducts_findsMatchingProducts() {
        // Create products with different names
        Product product1 = new Product();
        product1.setName("Laptop Computer");
        product1.setDescription("High-end laptop");
        product1.setPrice(999.99);

        Product product2 = new Product();
        product2.setName("Desktop Computer");
        product2.setDescription("Desktop workstation");
        product2.setPrice(1299.99);

        Product product3 = new Product();
        product3.setName("Smartphone");
        product3.setDescription("Mobile device");
        product3.setPrice(699.99);

        given().contentType(ContentType.JSON).body(product1).post("/api/products");
        given().contentType(ContentType.JSON).body(product2).post("/api/products");
        given().contentType(ContentType.JSON).body(product3).post("/api/products");

        // Search for "Computer"
        given()
            .queryParam("name", "Computer")
            .when()
                .get("/api/products/search")
            .then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("size()", is(2))
                .body("[0].name", containsString("Computer"))
                .body("[1].name", containsString("Computer"));
    }

    /**
     * Test 7: GET /api/products/search?name= - Search with no matches
     * Expected: HTTP 200, empty array
     */
    @Test
    @Order(7)
    public void testSearchProducts_noMatches_returnsEmptyList() {
        given()
            .queryParam("name", "NonexistentProduct")
            .when()
                .get("/api/products/search")
            .then()
                .statusCode(200)
                .contentType(ContentType.JSON)
                .body("size()", is(0));
    }

    /**
     * Test 8: DELETE /api/products/{id} - Delete product
     * Expected: HTTP 204
     */
    @Test
    @Order(8)
    public void testDeleteProduct_whenExists_returns204() {
        // Create a product
        Product product = new Product();
        product.setName("Product to delete");
        product.setDescription("Will be deleted");
        product.setPrice(9.99);

        Integer productId = given()
            .contentType(ContentType.JSON)
            .body(product)
            .when()
                .post("/api/products")
            .then()
                .statusCode(200)
                .extract()
                .path("id");

        // Delete it
        given()
            .when()
                .delete("/api/products/" + productId)
            .then()
                .statusCode(204);

        // Verify it's gone
        given()
            .when()
                .get("/api/products/" + productId)
            .then()
                .statusCode(404);
    }

    /**
     * Test 9: POST /api/products - Create product with missing required field
     * Characterization test - documents current behavior
     * Current behavior: Returns HTTP 500 (database constraint violation)
     */
    @Test
    @Order(9)
    public void testCreateProduct_withNullName_characterizationTest() {
        Product product = new Product();
        // name is null (marked as @Column(nullable = false))
        product.setDescription("Product without name");
        product.setPrice(49.99);

        // Current behavior: Database constraint fails, returns 500
        // TODO: Add bean validation to catch this earlier and return 400
        given()
            .contentType(ContentType.JSON)
            .body(product)
            .when()
                .post("/api/products")
            .then()
                .statusCode(500);
        // Documents that database constraint is enforced but not validated in application
    }

    /**
     * Test 10: POST /api/products - Create product with negative price
     * Characterization test - current behavior allows it
     */
    @Test
    @Order(10)
    public void testCreateProduct_withNegativePrice_characterizationTest() {
        Product product = new Product();
        product.setName("Product with negative price");
        product.setDescription("Edge case");
        product.setPrice(-10.0);

        // Current behavior: No validation, allows negative price
        // TODO: Add @Positive validation and expect 400
        given()
            .contentType(ContentType.JSON)
            .body(product)
            .when()
                .post("/api/products")
            .then()
                .statusCode(200)
                .body("price", is(-10.0f));
    }
}
