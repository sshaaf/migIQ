package com.example.demo.service;

import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.InjectMock;
import jakarta.inject.Inject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.*;

/**
 * Unit tests for ProductService
 * Priority 1: God Node (6 edges)
 * Coverage Target: 90%+
 *
 * Tests all business logic methods with mocked repository
 */
@QuarkusTest
public class ProductServiceTest {

    @Inject
    ProductService productService;

    @InjectMock
    ProductRepository productRepository;

    private Product testProduct;

    @BeforeEach
    public void setup() {
        testProduct = new Product();
        testProduct.setId(1L);
        testProduct.setName("Test Product");
        testProduct.setDescription("Test Description");
        testProduct.setPrice(99.99);
    }

    /**
     * Test getAllProducts - happy path
     */
    @Test
    public void testGetAllProducts_returnsAllProducts() {
        // Arrange
        Product product1 = new Product();
        product1.setId(1L);
        product1.setName("Product 1");

        Product product2 = new Product();
        product2.setId(2L);
        product2.setName("Product 2");

        List<Product> expectedProducts = Arrays.asList(product1, product2);
        when(productRepository.listAll()).thenReturn(expectedProducts);

        // Act
        List<Product> result = productService.getAllProducts();

        // Assert
        assertNotNull(result);
        assertEquals(2, result.size());
        assertEquals("Product 1", result.get(0).getName());
        assertEquals("Product 2", result.get(1).getName());
        verify(productRepository, times(1)).listAll();
    }

    /**
     * Test getAllProducts - empty list
     */
    @Test
    public void testGetAllProducts_whenEmpty_returnsEmptyList() {
        // Arrange
        when(productRepository.listAll()).thenReturn(Arrays.asList());

        // Act
        List<Product> result = productService.getAllProducts();

        // Assert
        assertNotNull(result);
        assertEquals(0, result.size());
        verify(productRepository, times(1)).listAll();
    }

    /**
     * Test getProductById - product exists
     */
    @Test
    public void testGetProductById_whenExists_returnsProduct() {
        // Arrange
        when(productRepository.findByIdOptional(1L)).thenReturn(Optional.of(testProduct));

        // Act
        Optional<Product> result = productService.getProductById(1L);

        // Assert
        assertTrue(result.isPresent());
        assertEquals(1L, result.get().getId());
        assertEquals("Test Product", result.get().getName());
        assertEquals(99.99, result.get().getPrice());
        verify(productRepository, times(1)).findByIdOptional(1L);
    }

    /**
     * Test getProductById - product does not exist
     */
    @Test
    public void testGetProductById_whenNotExists_returnsEmpty() {
        // Arrange
        when(productRepository.findByIdOptional(anyLong())).thenReturn(Optional.empty());

        // Act
        Optional<Product> result = productService.getProductById(999L);

        // Assert
        assertFalse(result.isPresent());
        verify(productRepository, times(1)).findByIdOptional(999L);
    }

    /**
     * Test createProduct - successful creation
     */
    @Test
    public void testCreateProduct_persistsAndReturnsProduct() {
        // Arrange
        Product newProduct = new Product();
        newProduct.setName("New Product");
        newProduct.setDescription("New Description");
        newProduct.setPrice(49.99);

        doNothing().when(productRepository).persist(any(Product.class));

        // Act
        Product result = productService.createProduct(newProduct);

        // Assert
        assertNotNull(result);
        assertEquals("New Product", result.getName());
        assertEquals("New Description", result.getDescription());
        assertEquals(49.99, result.getPrice());
        verify(productRepository, times(1)).persist(newProduct);
    }

    /**
     * Test createProduct - with null product
     * Characterization test: documents current behavior
     * Current behavior: Service doesn't validate null, just calls persist()
     */
    @Test
    public void testCreateProduct_withNullProduct_characterizationTest() {
        // Current behavior: Service doesn't validate null, just calls persist()
        // In real scenario, would fail at database level
        // TODO: Add null-checking in service layer

        // Skip mocking to avoid ambiguity - just document behavior
        // In real scenario with actual repository, this would fail
        Product result = productService.createProduct(null);

        // Service returns what it received (null in this case)
        assertNull(result);
    }

    /**
     * Test deleteProduct - successful deletion
     */
    @Test
    public void testDeleteProduct_delegatesToRepository() {
        // Arrange
        when(productRepository.deleteById(1L)).thenReturn(true);

        // Act
        productService.deleteProduct(1L);

        // Assert
        verify(productRepository, times(1)).deleteById(1L);
    }

    /**
     * Test deleteProduct - delete non-existent product
     */
    @Test
    public void testDeleteProduct_whenNotExists_stillCallsRepository() {
        // Arrange
        when(productRepository.deleteById(anyLong())).thenReturn(false);

        // Act
        productService.deleteProduct(999L);

        // Assert
        // Service doesn't check if delete succeeded - just delegates
        verify(productRepository, times(1)).deleteById(999L);
    }

    /**
     * Test searchProducts - finds matches
     */
    @Test
    public void testSearchProducts_findsMatchingProducts() {
        // Arrange
        Product product1 = new Product();
        product1.setName("Laptop");

        Product product2 = new Product();
        product2.setName("Laptop Pro");

        List<Product> expectedProducts = Arrays.asList(product1, product2);
        when(productRepository.findByNameContaining("Laptop")).thenReturn(expectedProducts);

        // Act
        List<Product> result = productService.searchProducts("Laptop");

        // Assert
        assertNotNull(result);
        assertEquals(2, result.size());
        verify(productRepository, times(1)).findByNameContaining("Laptop");
    }

    /**
     * Test searchProducts - no matches
     */
    @Test
    public void testSearchProducts_whenNoMatches_returnsEmptyList() {
        // Arrange
        when(productRepository.findByNameContaining("Nonexistent")).thenReturn(Arrays.asList());

        // Act
        List<Product> result = productService.searchProducts("Nonexistent");

        // Assert
        assertNotNull(result);
        assertEquals(0, result.size());
        verify(productRepository, times(1)).findByNameContaining("Nonexistent");
    }

    /**
     * Test searchProducts - with empty search term
     */
    @Test
    public void testSearchProducts_withEmptyString_searchesForEmpty() {
        // Arrange
        when(productRepository.findByNameContaining("")).thenReturn(Arrays.asList(testProduct));

        // Act
        List<Product> result = productService.searchProducts("");

        // Assert
        assertNotNull(result);
        assertEquals(1, result.size());
        verify(productRepository, times(1)).findByNameContaining("");
    }
}
