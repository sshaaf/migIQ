package com.example.javaee.service;

import com.example.javaee.model.Book;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;

@Stateless
public class BookService {

    @PersistenceContext
    private EntityManager entityManager;

    public List<Book> findAll() {
        return entityManager.createQuery("SELECT b FROM Book b", Book.class)
                           .getResultList();
    }

    public Book findById(Long id) {
        return entityManager.find(Book.class, id);
    }

    public Book create(Book book) {
        entityManager.persist(book);
        return book;
    }

    public Book update(Book book) {
        return entityManager.merge(book);
    }

    public void delete(Long id) {
        Book book = findById(id);
        if (book != null) {
            entityManager.remove(book);
        }
    }
}
