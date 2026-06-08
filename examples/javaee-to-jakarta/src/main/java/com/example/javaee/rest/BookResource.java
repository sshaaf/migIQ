package com.example.javaee.rest;

import com.example.javaee.model.Book;
import com.example.javaee.service.BookService;

import javax.ejb.EJB;
import javax.enterprise.context.RequestScoped;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.List;

@Path("/books")
@RequestScoped
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class BookResource {

    @EJB
    private BookService bookService;

    @GET
    public List<Book> getAllBooks() {
        return bookService.findAll();
    }

    @GET
    @Path("/{id}")
    public Response getBook(@PathParam("id") Long id) {
        Book book = bookService.findById(id);
        if (book == null) {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
        return Response.ok(book).build();
    }

    @POST
    public Response createBook(Book book) {
        Book created = bookService.create(book);
        return Response.status(Response.Status.CREATED).entity(created).build();
    }

    @PUT
    @Path("/{id}")
    public Response updateBook(@PathParam("id") Long id, Book book) {
        book.setId(id);
        Book updated = bookService.update(book);
        return Response.ok(updated).build();
    }

    @DELETE
    @Path("/{id}")
    public Response deleteBook(@PathParam("id") Long id) {
        bookService.delete(id);
        return Response.noContent().build();
    }
}
