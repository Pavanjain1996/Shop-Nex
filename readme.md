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

### **Product Services Overview**  

The product services handle all operations related to products and cart management. Below are the implemented API routes along with their functionalities:  

---

### **1. List All Products**  
- **Endpoint:** `GET /products`  
- **Description:** Retrieves a paginated list of all products available on the website. By default, a maximum of **10 products per page** is returned. However, the number of products per page can be customized using query parameters.  
- **Response:** Each response includes URLs for the **next** and **previous** pages (if applicable).  
- **Authentication:** **Not required**  

---

### **2. Get Product by ID**  
- **Endpoint:** `GET /product/<str:product_id>`  
- **Description:** Fetches details of a specific product using its **product_id**.  
- **Authentication:** **Not required**  

---

### **3. View Cart**  
- **Endpoint:** `GET /cart`  
- **Description:** Displays the user's cart, listing all products along with their quantities. The response includes:  
  - A breakdown of the total price for each product.  
  - The **final total amount** for the entire cart.  
- **Authentication:** **Required** (User must provide a valid token)  

---

### **4. Add Product to Cart**  
- **Endpoint:** `POST /cart/add`  
- **Description:** Adds a product to the user's cart.  
- **Behavior:**  
  - If the product **already exists** in the cart, the given quantity is **added** to the existing quantity.  
  - If the product is **not in the cart**, it is added as a new entry.  
- **Request Body:**  
  ```json
  {
      "product_id": "1311c455-ba36-43b9-a2a1-2422817f39e2",
      "quantity": 5
  }
  ```
- **Authentication:** **Required**  

---

### **5. Remove Product from Cart**  
- **Endpoint:** `POST /cart/remove`  
- **Description:** Removes an item completely or partially from the cart.  
- **Behavior:**  
  - If **quantity is specified**, only the given quantity is removed, and the cart is updated accordingly.  
  - If **quantity is not specified**, the product is removed **entirely** from the cart.  
- **Request Body:**  
  ```json
  {
      "product_id": "1311c455-ba36-43b9-a2a1-2422817f39e2",
      "quantity": 2
  }
  ```
- **Authentication:** **Required**  

---

### **Validations & Security Measures:**  
✅ **Authentication:** All cart-related operations require a **valid JWT token** for authorization.  
✅ **Product & Cart Validations:** Proper validation is implemented to ensure: data integrity.

---