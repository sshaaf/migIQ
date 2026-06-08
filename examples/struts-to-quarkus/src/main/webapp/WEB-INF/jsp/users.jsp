<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="s" uri="/struts-tags" %>
<html>
<head>
    <title>User List</title>
</head>
<body>
    <h1>Users</h1>

    <s:actionmessage />

    <table border="1">
        <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Actions</th>
        </tr>
        <s:iterator value="users">
            <tr>
                <td><s:property value="username" /></td>
                <td><s:property value="email" /></td>
                <td>
                    <s:url action="deleteUser" var="deleteUrl">
                        <s:param name="username" value="username" />
                    </s:url>
                    <a href="<s:property value='#deleteUrl' />">Delete</a>
                </td>
            </tr>
        </s:iterator>
    </table>

    <br/>
    <a href="userForm.jsp">Add New User</a>
</body>
</html>
