import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url):
    # Envia una petició GET a la pàgina web
    response = requests.get(url)
    
    # Comprova si la petició va ser exitosa
    if response.status_code == 200:
        # Analitza el contingut HTML de la pàgina
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Exemple: Extreu tots els paràgrafs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            print(p.get_text())
        
        
        # Exemple: Extreu tots els enllaços
        links = soup.find_all('a')
        
        # Crear un diccionari per representar l'estructura de carpetes
        folder_structure = {}

        def add_to_structure(structure, parts):
            current_level = structure
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]

        # Afegir els enllaços a la estructura
        for link in links:
            href = link.get('href')
            if href:
                # Normalitza la URL per garantir que és absoluta
                full_url = urljoin(url, href)
                parts = full_url.split('/')[2:]  # Ignorar el protocol (http, https)
                add_to_structure(folder_structure, parts)
        
        # Funció per imprimir l'estructura de carpetes
        def print_structure(d, indent=0, base_url=''):
            for key, value in d.items():
                if value:
                    print('  ' * indent + key)
                    print_structure(value, indent + 1, base_url + '/' + key)
                else:
                    print('  ' * indent + f"{key} - {base_url}/{key}")

        # Imprimeix l'estructura de carpetes
        print('Estructura de carpetes:...........................')
        print_structure(folder_structure)
        
        # Exemple: Extreu tots els títols
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            print(heading.get_text())
        
        # Pots afegir més lògica d'extracció aquí segons les teves necessitats
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    # Converteix el contingut extret a Markdown
    markdown_content = "# Contingut extret de la pàgina web\n\n"

    # Afegir paràgrafs
    markdown_content += "## Paràgrafs\n"
    for p in paragraphs:
        markdown_content += p.get_text() + "\n\n"

    # Afegir títols
    markdown_content += "## Títols\n"
    for heading in headings:
        markdown_content += heading.name + " " + heading.get_text() + "\n\n"

    # Afegir estructura de carpetes
    markdown_content += "## Estructura de carpetes\n"
    def add_structure_to_markdown(d, indent=0):
        md = ""
        for key, value in d.items():
            md += '  ' * indent + f"- {key}\n"
            if value:
                md += add_structure_to_markdown(value, indent + 1)
        return md

    markdown_content += add_structure_to_markdown(folder_structure)

    
    # Afegir enllaços
    markdown_content += "## Enllaços\n"
    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            markdown_content += f"[{full_url}]({full_url})\n\n"

    # Guarda el contingut Markdown en un fitxer
    with open('scraped_content.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)

    
    

    # Funció per extreure i guardar el contingut dels enllaços
    def save_link_content(link_url, base_filename):
        try:
            link_response = requests.get(link_url)
            if link_response.status_code == 200:
                link_soup = BeautifulSoup(link_response.content, 'html.parser')
                link_content = link_soup.get_text()
                filename = base_filename + '.md'
                with open(filename, 'w', encoding='utf-8') as link_file:
                    link_file.write(link_content)
                print(f"Contingut de l'enllaç guardat a: {filename}")
            else:
                print(f"Failed to retrieve the link: {link_url}. Status code: {link_response.status_code}")
        except Exception as e:
            print(f"Error retrieving the link: {link_url}. Error: {e}")

    # Guarda el contingut dels enllaços en fitxers markdown
    for i, link in enumerate(links):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            save_link_content(full_url, f'link_content_{i}')
    
if __name__ == "__main__":
    url = 'https://www.fib.upc.edu/ca/la-fib/serveis-tic/el-raco'
    scrape_website(url)