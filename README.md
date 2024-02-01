# BizCardX: Business Card Data Extraction with OCR

## Project Overview

### Technologies Used

- **Streamlit**: For creating a user-friendly graphical interface.
- **EasyOCR**: Utilized for Optical Character Recognition to extract text from business card images.
- **MySQL**: Integrated for storing and retrieving extracted business card data.
- **Pandas**: Used for data manipulation and DataFrame creation.
- **PIL (Pillow)**: Employed for handling image processing tasks.
- **Python Libraries**: Various Python libraries are used for handling different tasks within the project.

## Workflow Execution

### Setting Up the Project

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/BizCardX.git
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure a MySQL database is set up:**
    - Update the `start_mysql()` function in the `main.py` file with your database details.

### Running the Application

Execute the following command to run the Streamlit application:

```bash
streamlit run main.py
```

## Workflow Steps

### Home Page

- The Home page provides an overview of the project, including the technologies used and a brief description of the BizCardX project.

### Extract Data

- Users can upload business card images.
- The application performs OCR on the uploaded image using EasyOCR.
- Extracted information is displayed, and users have the option to move the data to a MySQL database.

### Modify Data

- Users can select a card holder from the database to modify or delete their information.
- Current information is displayed, and users can update or delete the selected card holder's details.

## Project Structure

- **main.py**: Contains the main application code.
- **uploaded_cards**: Directory to store uploaded business card images.

## Important Note

Ensure that the necessary dependencies are installed, and the MySQL database is set up before running the application.

Feel free to contribute, report issues, or suggest improvements!
