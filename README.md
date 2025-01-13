Вот переработанный **README.md** с разделением на секции для запуска с использованием Docker и без него:  

---

# 🍕 **PizzaLava - The Ultimate Pizza Delivery Platform**
![screen_main](https://github.com/user-attachments/assets/523b39d0-ab55-43e5-89ce-fd96e2d55c25)

Welcome to **PizzaLava**, your go-to online pizza delivery platform! Built on Django and equipped with modern tools, PizzaLava ensures a top-notch user experience and easy scalability.

---

## 🚀 **Project Highlights**

PizzaLava is packed with features to deliver both delicious pizzas and a great online experience:
- **Django 5**: Secure and robust backend.
- **Bootstrap 5**: Responsive and stylish UI.
- **PostgreSQL**: Reliable database solution.
- **Docker & Docker Compose**: Simplified containerized setup.
- **Static Assets**: Enhanced interactivity using jQuery, FontAwesome, and Swiper.js.

---

## 📦 **Getting Started**

You can run PizzaLava in two ways:
1. **Using Docker (Recommended)**: Simplifies setup and deployment with containerization.
2. **Manual Setup**: Traditional approach using virtual environments and local dependencies.

---

### 🐳 **1. Using Docker**

#### Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

#### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/PizzaLava.git
   cd PizzaLava
   ```

2. **Create an `.env` File**  
   Add environment variables to a `.env` file in the project root. Example:  
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
   DATABASE_NAME=pizza
   DATABASE_USER=postgres
   DATABASE_PASSWORD=yourpassword
   DATABASE_HOST=db
   DATABASE_PORT=5432
   ```

3. **Build and Start Services**  
   Run the following command to build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**
   - Visit the app at `http://localhost:8000`.
   - Create a superuser for administrative tasks:
     ```bash
     docker-compose exec web python manage.py createsuperuser
     ```

#### Managing Static Files
Run the following command inside the `web` container to collect static files:
```bash
docker-compose exec web python manage.py collectstatic
```

---

### 🖥️ **2. Manual Setup**

#### Prerequisites
- Python 3.10+ installed on your system.
- PostgreSQL installed and running.

#### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/PizzaLava.git
   cd PizzaLava
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Set up a PostgreSQL database and update the `.env` file with your credentials:
     ```env
     DATABASE_NAME=pizza
     DATABASE_USER=postgres
     DATABASE_PASSWORD=yourpassword
     DATABASE_HOST=localhost
     DATABASE_PORT=5432
     ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open `http://127.0.0.1:8000` in your browser.
   - Create a superuser:
     ```bash
     python manage.py createsuperuser
     ```

---

## 🔧 **Features**
- 🍕 **Dynamic Menu**: Fully customizable pizzas with add-ons.
- 📱 **Responsive Design**: Optimized for all devices.
- 🚚 **Order Tracking**: Keep up with your orders in real-time.
- 🛠 **Admin Panel**: Manage orders, menus, and more with ease.

---

## 🤝 **Contributing**

We welcome contributions! Feel free to fork the repository, submit pull requests, or open issues. Let's make PizzaLava even better together.

---

## 📝 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🎉 **Enjoy Your Pizza!**

Whether you're deploying with Docker or running locally, PizzaLava is ready to deliver. Thank you for choosing PizzaLava! 🍕✨

--- 

Would you like me to enhance this further with diagrams or specific commands?
