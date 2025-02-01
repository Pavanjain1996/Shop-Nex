### Project Overview

This project is a comprehensive e-commerce platform developed as part of capstone project module. It includes the following key services:

- **Authentication Services**: Secure user authentication and authorization mechanisms.
- **Product Services**: List products, categories, manage cart and orders.
- **Payment Services**: Seamless payment integration for processing transactions.

---

### Superuser Details

- **Uername**: `admin`
- **Email**: `admin@admin.com`
- **Password**: `admin`

---

### Postman Collection

- This project also includes a postman collection to execute all different kind of functionalities.

---

### User Registration and Login Summary

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

### **1. List All Products**  
- **Endpoint:** `GET /products`  
- **Description:** Retrieves a paginated list of all products available on the website. By default, a maximum of **10 products per page** is returned. However, the number of products per page can be customized using query parameters.  
- **Response:** Each response includes URLs for the **next** and **previous** pages (if applicable).  
- **Authentication:** **Not required**  

### **2. Get Product by ID**  
- **Endpoint:** `GET /product/<str:product_id>`  
- **Description:** Fetches details of a specific product using its **product_id**.  
- **Authentication:** **Not required**  

### **3. View Cart**  
- **Endpoint:** `GET /cart`  
- **Description:** Displays the user's cart, listing all products along with their quantities. The response includes:  
  - A breakdown of the total price for each product.  
  - The **final total amount** for the entire cart.  
- **Authentication:** **Required** (User must provide a valid token)  

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

### **6. Checkout from Cart**  
- **Endpoint:** `POST /cart/checkout`  
- **Description:** Creates an order for you and send you a payment link to complete the payment, to confirm your order
- **Behavior:**  
  - It creates an order for all items in your cart and empties the cart.
- **Authentication:** **Required** 

### **7. Check order status**  
- **Endpoint:** `POST /order/status`  
- **Description:** Once the payment is completed from the payment link received in previous request, it verifies the payment and moves you order for processing. You can check the status of your order from this path
- **Request Body:**  
  ```json
  {
      "order_id": "0194481b-55cd-4f67-9eb3-8c3c9cd79588"
  }
  ```
- **Authentication:** **Required** 

### **Validations & Security Measures:**  
✅ **Authentication:** All cart and order related operations require a **valid JWT token** for authorization.  
✅ **Product & Cart Validations:** Proper validation is implemented to ensure: data integrity.

---

### Deployment Steps for this application

Here are the steps to deploy your Django application on AWS EC2:

### **1. Set Up an AWS EC2 Instance**
- Log in to your AWS account.
- Navigate to **EC2 Dashboard** and launch a new instance.
- Choose an **Amazon Machine Image (AMI)** (Ubuntu 20.04 recommended).
- Select an instance type (e.g., t2.micro for free-tier).
- Configure security group: Allow **HTTP (80)**, **HTTPS (443)**, and **SSH (22)**.
- Generate and download a **.pem key pair** for SSH access.
- Launch the instance and note the **public IP address**.

### **2. Connect to the EC2 Instance**
Run the following command from your local machine:
```sh
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### **3. Update and Install Required Packages**
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx -y
```

### **4. Clone Your Project**
Transfer your Django project from GitHub or any repository:
```sh
git clone https://github.com/Pavanjain1996/Shop-Nex.git
cd your-project-folder
```

### **5. Set Up Virtual Environment**
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **6. Configure Environment Variables**
Edit `~/.bashrc` or `~/.profile` and add:
```sh
export SECRET_KEY="your-secret-key"
export DEBUG=False
```
Then run:
```sh
source ~/.bashrc
```

### **7. Set Up the Database**
In local we used `SQLIte` but for production usage we need to use PostgreSQL, below are steps to install and configure:
```sh
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql
```
Inside PostgreSQL shell:
```sql
CREATE DATABASE your_db;
CREATE USER your_user WITH PASSWORD 'your_password';
ALTER ROLE your_user SET client_encoding TO 'utf8';
ALTER ROLE your_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;
\q
```
Update `DATABASES` settings in `settings.py` accordingly.

### **8. Run Migrations and Collect Static Files**
```sh
python manage.py migrate
python manage.py collectstatic
```

### **9. Set Up Gunicorn**
```sh
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 your_project.wsgi:application
```

### **10. Configure Nginx as Reverse Proxy**
Create an Nginx config file:
```sh
sudo nano /etc/nginx/sites-available/your_project
```
Add the following:
```
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Enable Nginx config:
```sh
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

### **11. Set Up Supervisor (Optional)**
To keep Gunicorn running:
```sh
sudo apt install supervisor -y
sudo nano /etc/supervisor/conf.d/your_project.conf
```
Add:
```
[program:your_project]
command=/home/ubuntu/your_project/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 your_project.wsgi:application
directory=/home/ubuntu/your_project
autostart=true
autorestart=true
stderr_logfile=/var/log/your_project.err.log
stdout_logfile=/var/log/your_project.out.log
```
Save and run:
```sh
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start your_project
```

### **12. Access the Application**
Open **http://your-ec2-public-ip/** in a browser to see your Django app running!

---