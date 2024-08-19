import fitz  # PyMuPDF
import psycopg2
import boto3
import os
from io import BytesIO

class PDFProcessor:
    def __init__(self, db_config, s3_config=None):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.s3_client = boto3.client('s3') if s3_config else None
        self.s3_bucket = s3_config['bucket'] if s3_config else None

    def extract_images(self, pdf_path, storage_option):
        pdf_document = fitz.open(pdf_path)
        document_name = os.path.basename(pdf_path)
        document_size = os.path.getsize(pdf_path)
        
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_binary = base_image["image"]
                image_bbox = f"({img[1]}, {img[2]}, {img[3]}, {img[4]})"

                if storage_option == 'postgresql':
                    self.save_image_to_postgresql(document_name, document_size, page_number, img_index, image_bbox, image_binary)
                elif storage_option == 's3':
                    self.save_image_to_s3(document_name, page_number, img_index, image_bbox, image_binary)

                self.conn.commit()

        pdf_document.close()

    def save_image_to_postgresql(self, document_name, document_size, page_number, img_index, image_bbox, image_binary):
        self.cursor.execute(
            """
            INSERT INTO pdf_images (document_name, document_size, page_number, image_index, image_bbox, image_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (document_name, document_size, page_number + 1, img_index + 1, image_bbox, image_binary)
        )

    def save_image_to_s3(self, document_name, page_number, img_index, image_bbox, image_binary):
        s3_key = f"${document_name}/${page_number + 1}/${img_index + 1}.png"
        self.s3_client.upload_fileobj(BytesIO(image_binary), self.s3_bucket, s3_key)
