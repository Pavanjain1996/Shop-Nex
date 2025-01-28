### Project Overview

This project is a comprehensive e-commerce platform developed as part of capstone project module. It includes the following key services:

- **Product Services**: Manage products, categories, and related details with efficient APIs.
- **Authentication Services**: Secure user authentication and authorization mechanisms.
- **Payment Services**: Seamless payment integration for processing transactions.
- **Performance Optimization**: Leveraged **Redis** for caching and API performance enhancement.
- **Deployment**: Deployed on AWS using an **EC2 instance** for robust scalability and reliability.

---

### Superuser Details

- **Uername**: `admin`
- **Email**: `admin@admin.com`
- **Password**: `admin`

---

### Products listing from a 3rd Party API

The project begins with the integration of a third-party API, **FakeStoreAPI**, to provide core e-commerce functionality. The following features are implemented:

- **Listing All Products**: Fetches and displays a comprehensive list of products.
    - URL : `GET /fs/products`
- **Fetching Product by ID**: Retrieves detailed information about a specific product based on its unique ID.
    - URL : `GET /fs/products/{product_id}`
- **Fetching All Product Categories**: Lists all available product categories.
    - URL : `GET /fs/products/categories`
- **Fetching Products by Category**: Allows users to view products filtered by a specific category.
    - URL : `GET /fs/products/category/{category}`

These URLs lay the foundation for the application by providing dynamic, real-time product data, but they are limited to product listing functionalities. To enhance the e-commerce experience, we will now focus on building the backend to support additional operations, such as adding, updating, and deleting products, as well as enabling users to purchase items, add products to their cart, and implement other essential features.

---

### User Registration and Login Summary:

To facilitate user registration and authentication in the project, two API routes have been added:

1. **User Registration (`/user/register/`)**:
   - This route allows users to register with mandatory fields (username, password, first name, last name, email, phone number, and address).
   - The `username` and `email` fields are unique to ensure no duplicates in the system.
   - Example payload for registration:
     ```json
     {
         "username": "testuser3",
         "password": "test123",
         "first_name": "Test",
         "last_name": "User",
         "email": "testuser3@admin.com",
         "phone_number": "9898989898",
         "address": "ABC Street"
     }
     ```

2. **User Login (`/user/login/`)**:
   - This route validates a user's credentials (username and password).
   - Example payload for login:
     ```json
     {
         "username": "testuser3",
         "password": "test123"
     }
     ```
   - Upon successful authentication, a JSON Web Token (JWT) is returned to the user.
   - The token is used for further authentication in subsequent requests (like cart and order operations).
   - The JWT token serves as the authentication mechanism and is not stored in the database or managed in sessions.
   - If the token is compromised or expired, the user must log in again to generate a new token.

This implementation leverages the stateless nature of JWT, where the token itself contains the necessary information to authenticate the user, ensuring secure and efficient management of user sessions without the need for storing tokens or session data on the server.

---