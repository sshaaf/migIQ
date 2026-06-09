package com.example.demo.repository;

import com.example.demo.model.Product;
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for ProductRepository
 * Priority 2: Hub (2 edges)
 * Coverage Target: 85%+
 *
 * Tests Panache repository with real H2 database
 */
@QuarkusTest
public class ProductRepositoryTest {

    @Inject
    ProductRepository productRepository;

    @BeforeEach
    @Transactional
    public void cleanup() {
        // Clean database before each test
        productRepository.deleteAll();
    }

    /**
     * Test persist - saves product to database
     */
    @Test
    @Transactional
    public void testPersist_savesProductToDatabase() {
        // Arrange
        Product product = new Product();
        product.setName("Test Product");
        product.setDescription("Test Description");
        product.setPrice(99.99);

        // Act
        productRepository.persist(product);

        // Assert
        assertNotNull(product.getId());
        assertTrue(product.getId() > 0);
    }

    /**
     * Test listAll - returns all products
     */
    @Test
    @Transactional
    public void testListAll_returnsAllProducts() {
        // Arrange
        Product product1 = new Product();
        product1.setName("Product 1");
        product1.setDescription("Description 1");
        product1.setPrice(10.0);

        Product product2 = new Product();
        product2.setName("Product 2");
        product2.setDescription("Description 2");
        product2.setPrice(20.0);

        productRepository.persist(product1);
        productRepository.persist(product2);

        // Act
        List<Product> products = productRepository.listAll();

        // Assert
        assertNotNull(products);
        assertEquals(2, products.size());
    }

    /**
     * Test listAll - when empty
     */
    @Test
    @Transactional
    public void testListAll_whenEmpty_returnsEmptyList() {
        // Act
        List<Product> products = productRepository.listAll();

        // Assert
        assertNotNull(products);
        assertEquals(0, products.size());
    }

    /**
     * Test findByIdOptional - finds existing product
     */
    @Test
    @Transactional
    public void testFindByIdOptional_whenExists_returnsProduct() {
        // Arrange
        Product product = new Product();
        product.setName("Findable Product");
        product.setDescription("Can be found by ID");
        product.setPrice(50.0);
        productRepository.persist(product);
        Long productId = product.getId();

        // Act
        Optional<Product> found = productRepository.findByIdOptional(productId);

        // Assert
        assertTrue(found.isPresent());
        assertEquals("Findable Product", found.get().getName());
        assertEquals(50.0, found.get().getPrice());
    }

    /**
     * Test findByIdOptional - product not found
     */
    @Test
    @Transactional
    public void testFindByIdOptional_whenNotExists_returnsEmpty() {
        // Act
        Optional<Product> found = productRepository.findByIdOptional(99999L);

        // Assert
        assertFalse(found.isPresent());
    }

    /**
     * Test deleteById - deletes existing product
     */
    @Test
    @Transactional
    public void testDeleteById_whenExists_deletesProduct() {
        // Arrange
        Product product = new Product();
        product.setName("Product to delete");
        product.setDescription("Will be deleted");
        product.setPrice(25.0);
        productRepository.persist(product);
        Long productId = product.getId();

        // Act
        boolean deleted = productRepository.deleteById(productId);

        // Assert
        assertTrue(deleted);
        assertFalse(productRepository.findByIdOptional(productId).isPresent());
    }

    /**
     * Test deleteById - product not found
     */
    @Test
    @Transactional
    public void testDeleteById_whenNotExists_returnsFalse() {
        // Act
        boolean deleted = productRepository.deleteById(99999L);

        // Assert
        assertFalse(deleted);
    }

    /**
     * Test findByNameContaining - finds matching products (case-insensitive)
     */
    @Test
    @Transactional
    public void testFindByNameContaining_findsMatchingProducts() {
        // Arrange
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

        productRepository.persist(product1);
        productRepository.persist(product2);
        productRepository.persist(product3);

        // Act
        List<Product> computers = productRepository.findByNameContaining("Computer");

        // Assert
        assertNotNull(computers);
        assertEquals(2, computers.size());
        assertTrue(computers.stream().allMatch(p -> p.getName().contains("Computer")));
    }

    /**
     * Test findByNameContaining - case insensitive search
     */
    @Test
    @Transactional
    public void testFindByNameContaining_caseInsensitive() {
        // Arrange
        Product product = new Product();
        product.setName("Laptop Computer");
        product.setDescription("Test");
        product.setPrice(100.0);
        productRepository.persist(product);

        // Act - search with lowercase
        List<Product> results = productRepository.findByNameContaining("laptop");

        // Assert - should find the product (case-insensitive)
        assertNotNull(results);
        assertEquals(1, results.size());
        assertEquals("Laptop Computer", results.get(0).getName());
    }

    /**
     * Test findByNameContaining - no matches
     */
    @Test
    @Transactional
    public void testFindByNameContaining_noMatches_returnsEmptyList() {
        // Arrange
        Product product = new Product();
        product.setName("Laptop");
        product.setDescription("Test");
        product.setPrice(100.0);
        productRepository.persist(product);

        // Act
        List<Product> results = productRepository.findByNameContaining("Smartphone");

        // Assert
        assertNotNull(results);
        assertEquals(0, results.size());
    }

    /**
     * Test findByNameContaining - partial match
     */
    @Test
    @Transactional
    public void testFindByNameContaining_partialMatch() {
        // Arrange
        Product product = new Product();
        product.setName("Gaming Laptop Pro");
        product.setDescription("Test");
        product.setPrice(100.0);
        productRepository.persist(product);

        // Act - search for partial match
        List<Product> results = productRepository.findByNameContaining("Lap");

        // Assert
        assertNotNull(results);
        assertEquals(1, results.size());
        assertEquals("Gaming Laptop Pro", results.get(0).getName());
    }

    /**
     * Test count - returns correct count
     */
    @Test
    @Transactional
    public void testCount_returnsCorrectCount() {
        // Arrange
        Product product1 = new Product();
        product1.setName("Product 1");
        product1.setDescription("Desc 1");
        product1.setPrice(10.0);

        Product product2 = new Product();
        product2.setName("Product 2");
        product2.setDescription("Desc 2");
        product2.setPrice(20.0);

        productRepository.persist(product1);
        productRepository.persist(product2);

        // Act
        long count = productRepository.count();

        // Assert
        assertEquals(2, count);
    }
}
