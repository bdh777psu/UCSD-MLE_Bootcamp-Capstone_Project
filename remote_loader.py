import requests
import os


# if you want it locally, you can use:
CONTENT_DIR = os.path.dirname(__file__)


# an alternative if you want it in /tmp or equivalent.
# CONTENT_DIR = tempfile.gettempdir()

def filename_from_url(url):
    filename = url.split("/")[-1]
    return filename


def download_csv(url, filename=None):
    response = requests.get(url)
    if not filename:
        filename = filename_from_url(url)

    data_dir = "data/"
    full_path = os.path.join(CONTENT_DIR, data_dir + filename + ".csv")

    with open(full_path, mode="wb") as f:
        f.write(response.content)
        download_path = os.path.realpath(f.name)
    print(f"Downloaded file {filename} to {download_path}")
    return download_path


def main():
    # run through the different remote loading functions.
    survey_responses = "https://docs.google.com/spreadsheets/d/1Oj8ROLPcsq_I8h3Au7bE9cUSFhTFQx3eEIr8BXV1Jx4/export?format=csv"
    download_csv(survey_responses, filename='Mental Health in the Tech Industry Survey')

if __name__ == "__main__":
    main()
