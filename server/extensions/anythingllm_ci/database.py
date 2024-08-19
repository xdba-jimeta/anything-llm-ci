import psycopg2

def get_images_from_db(document_name, page_number):
    conn = psycopg2.connect(dbname="", user="", password="", host="", port="")
    cursor = conn.cursor()
    
    cursor.execute("SELECT image_data, image_s3_url FROM pdf_images WHERE document_name = %s AND page_number = %s", (document_name, page_number))
    images = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{'image_data': image[0], 'image_s3_url': image[1]} for image in images]
