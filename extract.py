from google.cloud import vision
import glob
import re


def extract(file, front_or_rear):
    image_data = file.read()

    extraction = {}

    google_ocr_response = get_google_ocr_response(image_data)

    extraction['data'] = extract_data(google_ocr_response, front_or_rear)

    return extraction


def get_google_ocr_response(image_data):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image(content=image_data)

    response = client.text_detection(image=image)

    return response


def extract_data(google_ocr_response, front_or_rear):
    text = str(google_ocr_response.full_text_annotation.text)
    if front_or_rear == 'front':
        req_text = re.findall(r"\s+(\w{3})[-.\s](\w{4})\s+", text)
    else:
        req_text = re.findall(r"(\w{3})(\w)\s*(\d{6})\s*(\d?)", text)
    if len(req_text):
        return req_text
    return [('None',)]


def main():
    path = './images/rear3.jpg'
    files = glob.glob(path)
    for file_name in files:
        with open(file_name, 'rb') as file:
            print(file_name)
            extraction = extract(file, 'rear')
            print(extraction)


if __name__ == '__main__':
    main()
