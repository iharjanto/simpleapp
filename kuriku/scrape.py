import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Konfigurasi ChromeDriver
chrome_driver_path = "./chromedriver"  # Ganti dengan path ChromeDriver Anda
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL target
url = "https://id.wikipedia.org/wiki/Daftar_penyanyi_solo_perempuan_Indonesia"


def get_all_singer_links():
    try:
        # Buka halaman Wikipedia
        driver.get(url)

        # Tunggu sampai konten utama dimuat
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mw-content-text"))
        )
        _singerlink = driver.find_elements(By.XPATH, "//li[a]")
        for i in _singerlink:
            print(i.get_attribute("href"))

    except Exception as e:
        print(f"Error: {str(e)}")
        return []
    finally:
        driver.quit()


def save_to_csv(links, filename="singer_links.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "href", "text"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for link in links:
            writer.writerow(link)

    print(f"Data telah disimpan ke {filename}")


if __name__ == "__main__":
    print("Mengambil semua link penyanyi...")
    # all_links = get_all_singer_links()
    get_all_singer_links()
    # if all_links:
    # print(f"Berhasil menemukan {len(all_links)} link penyanyi")

    # # Simpan ke CSV
    # timestamp = time.strftime("%Y%m%d_%H%M%S")
    # filename = f"singer_links_{timestamp}.csv"
    # # save_to_csv(all_links, filename)

    # # Tampilkan contoh hasil
    # print("\nContoh 5 link pertama:")
    # for i, link in enumerate(all_links[:5]):
    #     print(f"{i+1}. {link['text']} - {link['href']}")
    # else:
    #     print("Tidak menemukan link penyanyi")
