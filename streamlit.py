



import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_information(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    except requests.exceptions.RequestException as e:
        return None, None, None, None, f"Error: {e}"

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract links
        links = [link['href'] for link in soup.find_all('a', href=True)]

        # Extract titles
        titles = [title.text for title in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

        # Extract paragraphs
        paragraphs = [paragraph.text for paragraph in soup.find_all('p')]

        # Extract headings
        headings = [heading.text for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

        return links, titles, paragraphs, headings, None
    else:
        return None, None, None, None, f"Failed to retrieve the web page. Status code: {response.status_code}"

def main():
    st.title("Web Information Extractor with Streamlit")

    # Input URL from the user
    url = st.text_input("Enter the URL:")

    if st.button("Extract Information"):
        if url:
            result = extract_information(url)

            links, titles, paragraphs, headings, error = result if result else ([], [], [], [], "Failed to extract information")

            if error:
                st.error(error)
            else:
                st.header("Extracted Information:")

                st.subheader("Links:")
                for i, link in enumerate(links, 1):
                    st.write(f'Link {i}: {link}')

                st.subheader("Titles:")
                for i, title in enumerate(titles, 1):
                    st.write(f'Title {i}: {title}')

                st.subheader("Paragraphs:")
                for i, paragraph in enumerate(paragraphs, 1):
                    st.write(f'Paragraph {i}: {paragraph}')

                st.subheader("Headings:")
                for i, heading in enumerate(headings, 1):
                    st.write(f'Heading {i}: {heading}')

if __name__ == "__main__":
    main()
