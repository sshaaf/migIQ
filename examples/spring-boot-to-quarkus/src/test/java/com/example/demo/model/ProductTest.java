package com.example.demo.model;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for Product entity
 * Priority 1: God Node (9 edges - highest!)
 * Coverage Target: 90%+
 *
 * Tests entity behavior, getters, setters, and field constraints
 */
public class ProductTest {

    private Product product;

    @BeforeEach
    public void setup() {
        product = new Product();
    }

    /**
     * Test entity instantiation
     */
    @Test
    public void testProductInstantiation() {
        assertNotNull(product);
    }

    /**
     * Test ID getter and setter
     */
    @Test
    public void testIdGetterAndSetter() {
        Long expectedId = 123L;
        product.setId(expectedId);
        assertEquals(expectedId, product.getId());
    }

    /**
     * Test name getter and setter
     */
    @Test
    public void testNameGetterAndSetter() {
        String expectedName = "Test Product";
        product.setName(expectedName);
        assertEquals(expectedName, product.getName());
    }

    /**
     * Test name with null value
     * Characterization: @Column(nullable = false) but no bean validation
     */
    @Test
    public void testName_acceptsNull_characterization() {
        product.setName(null);
        assertNull(product.getName());
        // Note: Database constraint will fail on persist, but entity allows it
    }

    /**
     * Test description getter and setter
     */
    @Test
    public void testDescriptionGetterAndSetter() {
        String expectedDescription = "A test product description";
        product.setDescription(expectedDescription);
        assertEquals(expectedDescription, product.getDescription());
    }

    /**
     * Test description with null value (allowed)
     */
    @Test
    public void testDescription_acceptsNull() {
        product.setDescription(null);
        assertNull(product.getDescription());
    }

    /**
     * Test price getter and setter
     */
    @Test
    public void testPriceGetterAndSetter() {
        Double expectedPrice = 99.99;
        product.setPrice(expectedPrice);
        assertEquals(expectedPrice, product.getPrice());
    }

    /**
     * Test price with null value
     * Characterization: @Column(nullable = false) but no bean validation
     */
    @Test
    public void testPrice_acceptsNull_characterization() {
        product.setPrice(null);
        assertNull(product.getPrice());
        // Note: Database constraint will fail on persist, but entity allows it
    }

    /**
     * Test price with negative value
     * Characterization: No validation, allows negative
     */
    @Test
    public void testPrice_acceptsNegative_characterization() {
        product.setPrice(-10.0);
        assertEquals(-10.0, product.getPrice());
        // Note: Might want to add @Positive validation in the future
    }

    /**
     * Test price with zero
     */
    @Test
    public void testPrice_acceptsZero() {
        product.setPrice(0.0);
        assertEquals(0.0, product.getPrice());
    }

    /**
     * Test price with very large number
     */
    @Test
    public void testPrice_acceptsLargeNumber() {
        Double largePrice = 999999999.99;
        product.setPrice(largePrice);
        assertEquals(largePrice, product.getPrice());
    }

    /**
     * Test setting all fields
     */
    @Test
    public void testSettingAllFields() {
        Long id = 1L;
        String name = "Complete Product";
        String description = "A product with all fields set";
        Double price = 49.99;

        product.setId(id);
        product.setName(name);
        product.setDescription(description);
        product.setPrice(price);

        assertEquals(id, product.getId());
        assertEquals(name, product.getName());
        assertEquals(description, product.getDescription());
        assertEquals(price, product.getPrice());
    }

    /**
     * Test product with minimal fields (ID and required fields)
     */
    @Test
    public void testProduct_withMinimalFields() {
        product.setName("Minimal Product");
        product.setPrice(9.99);
        // Description is optional

        assertNotNull(product.getName());
        assertNotNull(product.getPrice());
        assertNull(product.getDescription());
        assertNull(product.getId()); // Not yet persisted
    }

    /**
     * Test name with empty string
     */
    @Test
    public void testName_acceptsEmptyString() {
        product.setName("");
        assertEquals("", product.getName());
    }

    /**
     * Test name with very long string
     */
    @Test
    public void testName_acceptsLongString() {
        String longName = "A".repeat(255);
        product.setName(longName);
        assertEquals(longName, product.getName());
    }

    /**
     * Test description with empty string
     */
    @Test
    public void testDescription_acceptsEmptyString() {
        product.setDescription("");
        assertEquals("", product.getDescription());
    }

    /**
     * Test description with very long text
     */
    @Test
    public void testDescription_acceptsLongText() {
        String longDescription = "Lorem ipsum dolor sit amet. ".repeat(50);
        product.setDescription(longDescription);
        assertEquals(longDescription, product.getDescription());
    }

    /**
     * Test price precision (Double type)
     */
    @Test
    public void testPrice_handlesPrecision() {
        Double precisePrice = 99.999999;
        product.setPrice(precisePrice);
        assertEquals(precisePrice, product.getPrice(), 0.000001);
    }
}
