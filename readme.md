## Project Overview

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
