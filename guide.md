# Task 1: Energy Company Booking & Energy Usage System

## 1. Business Context
An energy company wants a digital solution that allows customers to:
- **Book installations and consultations** for their energy systems.
- **Log in to view their energy usage** via an online dashboard.

This system must be **accessible, user-friendly, and secure**, ensuring smooth customer interactions.

---

## 2. User Stories

### **Customers**
- **As a customer**, I want to **register and log in** so that I can manage my bookings and view my energy usage.
- **As a customer**, I want to **book an installation appointment** so that I can set up my new energy system at a convenient time.
- **As a customer**, I want to **book a consultation** so that I can discuss energy-saving options with an expert.
- **As a customer**, I want to **see my past and upcoming bookings** so that I can stay updated on my appointments.
- **As a customer**, I want to **track my energy usage in real-time** so that I can monitor and reduce my consumption.
- **As a customer**, I want to **receive alerts** if my energy usage is unusually high so that I can adjust my consumption.

### **Administrators**
- **As an admin**, I want to **view and manage customer bookings** so that I can allocate resources efficiently.
- **As an admin**, I want to **update appointment availability** so that customers can only book available slots.
- **As an admin**, I want to **send notifications to customers** about upcoming appointments or service updates.

---

## 3. Wireframes (UI Mockups)
These basic wireframes outline the layout of key screens:

### **Homepage**
- Welcome message
- Login/Register button
- Quick access to:
  - **Book Installation**
  - **Book Consultation**
  - **View Energy Usage**

### **Booking Page**
- Select **installation or consultation**
- Choose **date & time**
- Enter details and **confirm booking**
- Booking confirmation screen

### **Energy Usage Dashboard**
- Graph showing **energy consumption over time**
- Daily/weekly/monthly usage statistics
- Alerts for high usage
- Comparison with previous periods

> Wireframes can be created using **Figma** or **Balsamiq**.

---

## 4. Technical Justification

### **Tech Stack**
| Component   | Technology |
|------------|-------------|
| **Frontend** | React.js / Next.js |
| **Backend**  | Node.js with Express.js |
| **Database** | MongoDB or PostgreSQL |
| **Authentication** | JWT (JSON Web Token) |
| **Hosting**  | Vercel / AWS |

### **Database Structure**
A simplified **ERD (Entity-Relationship Diagram)**:

#### **Tables / Collections**
#### `Users`
- `user_id` (Primary Key)
- `name`
- `email`
- `password` (hashed)
- `role` (customer/admin)

#### `Bookings`
- `booking_id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `type` (Installation / Consultation)
- `date`
- `time`
- `status` (Confirmed / Cancelled / Completed)

#### `EnergyUsage`
- `usage_id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `timestamp`
- `energy_consumed` (kWh)

---

## 5. API Structure

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | Authenticate user |
| `/api/bookings` | GET | Retrieve user's bookings |
| `/api/bookings` | POST | Create a new booking |
| `/api/bookings/:id` | DELETE | Cancel a booking |
| `/api/energy-usage` | GET | Get energy usage data |

---

## 6. Test Strategy

To ensure the system works as expected, we will implement the following tests:

### **Unit Testing**
- Test the **booking logic**: Ensure that only available slots can be booked.
- Test **energy data retrieval**: Verify that the energy usage data is fetched correctly.

### **Integration Testing**
- **Ensure login and authentication** work correctly.
- **Verify that bookings are stored correctly** in the database.

### **User Acceptance Testing (UAT)**
- Ask real users (customers & admins) to test the system and give feedback.

### **Example Test Case**
| **Test** | **Steps** | **Expected Result** |
|----------|----------|---------------------|
| **Booking Installation** | 1. Log in 2. Select installation 3. Choose date & time 4. Confirm booking | Booking is saved & confirmation message appears |
| **View Energy Usage** | 1. Log in 2. Navigate to dashboard 3. View energy graph | Graph updates with user’s data |

---

## 7. Conclusion
This system provides an **efficient, user-friendly** way for customers to:
- **Book installations & consultations**
- **Monitor their energy usage**  

It ensures **security, accessibility, and maintainability**, making it a scalable solution for the energy company.

---

## ✅ Final Check for Exam Readiness
✔ **User stories** included  
✔ **Wireframes/UI design** covered  
✔ **Database structure & API endpoints** defined  
✔ **Technical justification (tech stack)** provided  
✔ **Test strategy & example cases** outlined  

This **Markdown file** can be used for submission or documentation. 🚀 Let me know if you need any refinements!
