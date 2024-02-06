# Import necessary libraries
import streamlit as st
import easyocr
import mysql.connector
import pandas as pd
from PIL import Image
import io
from streamlit_option_menu import option_menu
import re
import os

# Initialize variables
name = designation = phone = address = pincode = email = website = company = ""
            
# Function to start MySQL connection
def start_mysql():
    mysql_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mysql',
        database='bizcard'
    )
    mysql_cursor = mysql_connection.cursor()
    return mysql_connection, mysql_cursor

# Function to perform OCR and return results
def perform_ocr(image):
    # Convert PIL Image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes = image_bytes.getvalue()

    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_bytes)
    return results

# Function to extract data from the OCR results
def extract_data(lst,saved_img):
    for line in lst:
        name = lst[0]
        designation = lst[1]

        if '-' in line:
            phone = line
        elif ',' in line and ' ' in line:
            address = line
        elif re.match(r'^(?:[a-zA-Z]+\s)?(\d+)$', line):
            pincode = line[-7:]
        elif '@' in line and (line.lower().endswith('.com')):
            email = line.lower()
        elif line.lower().startswith('www.') or line.lower().endswith('.com'):
            website = line.lower()
        else:
            company = line

    data = {
            'Name': [name],
            'Designation': [designation],
            'Address': [address],
            'Pincode': [pincode],
            'Phone': [phone],
            'Email': [email],
            'Website': [website],
            'Company': [company],
            'Image' : [image_to_binary(saved_img)]
            }
    return data

# Function to Execute and Commit SQL Query
def execute_query(mysql_cursor, mysql_connection, query, values = None):
    mysql_cursor.execute(query, values)
    mysql_connection.commit()

# Function to save the uploaded image
def save_card(uploaded_image):
    upload_dir = 'uploaded_cards'
    os.makedirs(upload_dir, exist_ok=True)

    with open(os.path.join(upload_dir,uploaded_image.name), 'wb') as f:
        f.write(uploaded_image.getbuffer())

def image_to_binary(uploaded_image):
    with open(uploaded_image, 'rb') as file:
        binary_data = file.read()
        return binary_data

# Function to close MySQL connection
def close_mysql(mysql_cursor, mysql_connection):
    mysql_cursor.close()
    mysql_connection.close()

# Main Function
def main():

    st.set_page_config(layout = 'wide')

    mysql_connection, mysql_cursor = start_mysql()

    with st.sidebar:
        options = option_menu("Menu", ["Home", "Extract Data", "Modify Data"])

    if options == 'Home':
        # Home Page
        st.title('BizCardX: Extracting Business Card Data with OCR')
        st.subheader('Technologies Used: ')
        st.write('OCR, Streamlit GUI, SQL, Data Extraction')
        
        st.subheader('About BizCardX Project')
        about_project = (
        "The BizCardX project is a streamlined tool designed for extracting valuable information from business card images using Optical Character Recognition (OCR) technology. "
        "Developed with Python and Streamlit, the application allows users to effortlessly upload business card images, which are then processed and analyzed using the EasyOCR library. "
        "The extracted data includes key details such as name, designation, contact information, address, email, website, and company details. "
        "Users can view the uploaded image alongside the extracted information, promoting a user-friendly experience. "
        "It incorporates MySQL integration for seamless data storage and retrieval. "
        "The project prioritizes simplicity, efficiency, and adaptability, making it a valuable tool for quickly digitizing business card data."
        )

        st.write(about_project)
        

    if options == 'Extract Data':
        # Extract Data Page
        st.title('Business Card Data Extraction')

        uploaded_image = st.file_uploader('Upload Business Card Image', type = ['jpg','jpeg','png'])

        if uploaded_image is not None:

            save_card(uploaded_image)
            saved_img = os.path.join(os.getcwd(), "uploaded_cards", uploaded_image.name)

            image = Image.open(uploaded_image)

            st.image(image, caption = 'Uploaded Image')

            ocr_results = perform_ocr(image)

            lst = [detection[1] for detection in ocr_results]

            if st.button('Extract Information'):
                with st.spinner('Extracting Information...'):

                    data = extract_data(lst, saved_img)

                    st.subheader('Extracted Information:')
                    # Create a DataFrame
                    df = pd.DataFrame(data)

                    # Display DataFrame in Streamlit
                    st.dataframe(df)

            if st.button('Move to Database'):
                data = extract_data(lst,saved_img)
                df = pd.DataFrame(data)

                query = '''insert into card_data (name,designation,address,pincode,phone,email,website,company_name,image)
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
                values = tuple(df.iloc[0].values)
                    
                execute_query(mysql_cursor, mysql_connection, query, values)
                    
                st.success('Data Moved to Database Successfully!')
    
    if options == 'Modify Data':
        # Modify Data Page
        st.title('Modify Business Card Data')
        
        mysql_cursor.execute('select id,name from card_data')
        card_holders = mysql_cursor.fetchall()

        selected_card_holder = st.selectbox('Select a Card Holder to Modify', [f'{card[0]} : {card[1]}' for card in card_holders])
        
        st.subheader('Update the Details below:')
        
        if selected_card_holder is not None:
            card_id = int(selected_card_holder.split(':')[0].strip())
            mysql_cursor.execute(f'select * from card_data where id = {card_id}')
            selected_card_data = mysql_cursor.fetchone()

            st.subheader('Current Information:')
            
            current_df = pd.DataFrame({
                'Name': [selected_card_data[1]],
                'Designation': [selected_card_data[2]],
                'Address': [selected_card_data[3]],
                'Pincode': [selected_card_data[4]],
                'Phone': [selected_card_data[5]],
                'Email': [selected_card_data[6]],
                'Website': [selected_card_data[7]],
                'Company': [selected_card_data[8]],
                })
            st.dataframe(current_df)

            col1,col2 = st.columns(2)

            with col1:
                st.subheader('Modify Information:')
                modified_name = st.text_input('Name', selected_card_data[1])
                modified_designation = st.text_input('Designation', selected_card_data[2])
                modified_address = st.text_input('Address', selected_card_data[3])
                modified_pincode = st.text_input('Pincode', selected_card_data[4])
                modified_phone = st.text_input('Phone', selected_card_data[5])
                modified_email = st.text_input('Email', selected_card_data[6])
                modified_website = st.text_input('Website', selected_card_data[7])
                modified_company = st.text_input('Company', selected_card_data[8])

                if st.button('Update Information'):
                    query = '''update card_data
                            set name = %s, designation = %s, address = %s, pincode = %s, phone = %s, email = %s,
                            website = %s, company_name = %s '''
                    values = (modified_name, modified_designation, modified_address, modified_pincode,
                            modified_phone, modified_email, modified_website, modified_company)
                
                    execute_query(mysql_cursor, mysql_connection, query, values)

                    st.success('Data Updated Successfully!')

            with col2:
                st.subheader('Delete Information:')
                selected_card_to_delete = st.selectbox('Select Card Holder to Delete',[f'{card[0]} : {card[1]}' for card in card_holders])

                delete_confirmation = st.checkbox(f"I want to delete the information")

                if delete_confirmation:
                    if st.button('Delete Card Holder'):
                        card_id_to_delete = int(selected_card_holder.split(':')[0].strip())
                        query = f'delete from card_data where id = %s'
                        values = (card_id_to_delete,)
                        execute_query(mysql_cursor, mysql_connection, query,values)

                        st.success('Card Holder Deleted Successfully!')
        else:
            st.warning('No Data to Display')

    close_mysql(mysql_cursor, mysql_connection)

if __name__ == '__main__':
    main()
