package com.example.struts.action;

import com.example.struts.model.User;
import com.opensymphony.xwork2.ActionSupport;
import com.opensymphony.xwork2.ModelDriven;

import java.util.ArrayList;
import java.util.List;

public class UserAction extends ActionSupport implements ModelDriven<User> {

    private User user = new User();
    private List<User> users = new ArrayList<>();

    public String execute() {
        return SUCCESS;
    }

    public String list() {
        // Simulate fetching users
        users.add(createSampleUser("alice", "alice@example.com"));
        users.add(createSampleUser("bob", "bob@example.com"));
        return SUCCESS;
    }

    public String create() {
        // Validate
        if (user.getUsername() == null || user.getUsername().isEmpty()) {
            addFieldError("username", "Username is required");
            return INPUT;
        }
        if (user.getEmail() == null || user.getEmail().isEmpty()) {
            addFieldError("email", "Email is required");
            return INPUT;
        }

        // Save user (simulated)
        users.add(user);
        addActionMessage("User created successfully!");
        return SUCCESS;
    }

    public String delete() {
        // Simulate delete
        users.removeIf(u -> u.getUsername().equals(user.getUsername()));
        addActionMessage("User deleted successfully!");
        return SUCCESS;
    }

    private User createSampleUser(String username, String email) {
        User u = new User();
        u.setUsername(username);
        u.setEmail(email);
        return u;
    }

    @Override
    public User getModel() {
        return user;
    }

    public List<User> getUsers() {
        return users;
    }
}
