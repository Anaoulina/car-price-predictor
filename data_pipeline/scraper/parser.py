from bs4 import BeautifulSoup
import re

class AvitoParser:
    @staticmethod
    def extract_links(html_source):
        soup = BeautifulSoup(html_source, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True) if "voitures_d_occasion" in a['href']]

    @staticmethod
    def extract_car_details(html_source, link):
        soup = BeautifulSoup(html_source, 'html.parser')
        car_info = {"URL": link}
        
        h1 = soup.find('h1')
        title_text = h1.get_text(strip=True) if h1 else "N/A"
        car_info["Titre"] = title_text
        
        car_info["Prix"] = "N/A"
        for text in soup.stripped_strings:
            if "DH" in text and any(char.isdigit() for char in text) and "mois" not in text.lower():
                car_info["Prix"] = text.replace("\u202f", "").strip()
                break
                
        keywords = ["Année", "Kilométrage", "Carburant", "Boite de vitesses", "Marque", "Modèle"]
        for kw in keywords:
            car_info[kw] = "N/A"
            for elem in soup.find_all(string=re.compile(kw, re.IGNORECASE)):
                if kw == "Modèle" and "année" in elem.lower(): continue
                container = elem.find_parent().find_parent()
                if container:
                    parent_text = container.get_text(separator=" ", strip=True)
                    if kw == "Modèle" and "année" in parent_text.lower(): continue
                    if len(parent_text) < 100 and kw.lower() in parent_text.lower():
                        clean_val = parent_text.replace(elem.strip(), "").strip()
                        clean_val = re.sub(rf'Type de {kw}|{kw}', '', clean_val, flags=re.IGNORECASE).strip()
                        car_info[kw] = clean_val.replace("-Modèle", "").replace(":", "").strip()
                        break
                        
        if car_info["Carburant"] == "N/A" and title_text != "N/A":
            if "diesel" in title_text.lower(): car_info["Carburant"] = "Diesel"
            elif "essence" in title_text.lower(): car_info["Carburant"] = "Essence"

        return car_info