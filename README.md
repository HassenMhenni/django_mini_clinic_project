# MyClinic: A Mini Clinic Management System (mini django project)

## 1. Introduction 

### 1.1. Project Goal and My Role

I developed this mini clinic management system as a personal project to Enhance my skills in Django and build a practical web application. The goal was to create a simple tool that could handle basic patient and appointment management tasks.

### 1.2. Key Features 

I Implemented In this project, I implemented the following key features: 

 - Patient management: Adding, viewing, updating, and deleting patient
   records.  
 - Appointment scheduling: Creating, viewing, updating, and    deleting
   appointments.
 - User authentication: Ensuring that only logged-in users can access
   the application's features.
 - Admin  interface customization: Making the admin interface easy to
   use.
## 2. My Implementation 

### 2.1. Core Functionality 

#### 2.1.1. Patient Management (`patient_app`)

I built the `patient_app` to handle all aspects of patient data. This includes: 

Storing patient names, dates of birth, contact information, and basic medical histories. 

 * Providing a user interface to create new patient records. 
 * Allowing users to view, update, and delete existing patient records.
 * Implementing a search feature to quickly find patients by name. *
 * Adding a boolean field to indicate if a patient has been verified by  an admin.
 * 
#### 2.1.2. Appointment Scheduling (`scheduler_app`)

 The `scheduler_app` is responsible for managing appointments. I implemented the following: 
 
 * Linking appointments to specific patients. 
 * Storing appointment dates, times, and doctor names. 
 * Providing a user interface to create new appointments. 
 * Allowing users to view, update, and delete  existing appointments.
 * Displaying  appointments in chronological order. 
 * Adding an internal admin notes field for each appointment.

### 2.2. Forms and User Interface

 I created user-friendly forms for both patient and appointment management. These forms allow users to easily input and modify data. I also used Django templates to build the user interface, ensuring that the application is easy to navigate. 
 
 ### 2.3. Authentication and Access Control 
 
 To protect patient data and ensure the application is used responsibly, I implemented user authentication. This means that only logged-in users can access the patient and appointment management features. 
 
 ### 2.4. Admin Interface Customization
 
  I customized the Django admin interface to make it easier to manage the application. This includes:
   * Displaying relevant information in the admin list views. 
   * Adding search and filter options to quickly find specific records. 
   * Allowing admin users to edit internal notes for appointments and verify patients.

## 3. How to Run and Explore

 ### 3.1. Setting Up the Project
  To run this project, follow these steps: 
  1. Make sure you have Python 3.6+ and pip installed. 
  2. Clone this repository to your local machine. 
  3.  Navigate to the project directory in your terminal. 
  4.  Create a virtual environment: `python -m venv venv` 
  5.  Activate the virtual environment: * On Windows: `venv\Scripts\activate` * On macOS/Linux: `source venv/bin/activate` 
  6. Install the required packages: `pip install -r requirements.txt`
  7.  Apply migrations: `python manage.py migrate` 
  8. Create a superuser to access the admin panel: `python manage.py createsuperuser`

### 3.2. Accessing the Application

After setting up the project, start the development server:

    python manage.py runserver

Then, open your web browser and go to http://127.0.0.1:8000/.

### 3.3. Navigating the Features

Once the application is running:

-   You can view the patient list by clicking on "Patient List" on the home page.
    
-   You can view the appointment list by clicking on "Appointment List" on the home page.
    
-   You can access the admin panel by clicking on "Admin Login" on the home page or going to http://127.0.0.1:8000/admin/ and logging in with the superuser credentials you created earlier.
    
-   Explore the different functionalities by creating, updating, and deleting patients and appointments.

## 4. Testing

### 4.1. Testing Information

I've implemented tests for both the patient_app and scheduler_app to ensure the core functionalities are working as expected. These tests cover the following:

-   **Model Tests:**
    
    -   Verifying the creation of Patient and Appointment objects.
        
    -   Checking the string representation of the models.
        
-   **Form Tests:**
    
    -   Validating both valid and invalid form data for PatientForm and AppointmentForm.
        
    -   Ensuring that the forms handle errors correctly.
        
-   **View Tests:**
    
    -   Testing the functionality of the patient and appointment list views, detail views, create views, update views, and delete views.
        
    -   Verifying the response status codes and context data.
        
    -   Ensuring that unauthenticated users are redirected to the login page.

To run the tests, use the following command in your terminal:


    python manage.py test

This command will run all the tests in your project and provide a summary of the results.
