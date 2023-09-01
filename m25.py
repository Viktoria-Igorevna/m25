from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   driver.get('https://petfriends.skillfactory.ru/login')

   yield driver

   driver.quit()


def test_show_all_pets(driver):
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('pohta_pohta@gmail.com')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   driver.find_element(By.CSS_SELECTOR, '.nav-link').click()

   all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')
   all_pets_images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/th/img')
   assert len(all_my_pets) > 0
   element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
   count = driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text.split('\n')
   number = count[1].split(' ')
   number = int(number[1])

   pets_info = []
   for i in range(len(all_my_pets)):
      # получаем информацию о питомце из списка всех своих питомцев
      pet_info = all_my_pets[i].text

      # избавляемся от лишних символов '\n×'
      pet_info = pet_info.split("\n")[0]

      # добавляем в список pets_info информацию рода: имя, тип, возраст,  по каждому питомцу
      pets_info.append(pet_info)
   pets_base = 0
   pets_name = set()
   pets_set = set()
   for i in pets_info:
      pets_set.add(i.upper())
      pet = i.upper().split(' ')
      pets_base += len(pet)
      pets_name.add(pet[0])
   assert len(pets_info) == number           # Присутствуют все питомцы.
   assert len(all_pets_images) >= number//2  # Хотя бы у половины питомцев есть фото.
   assert pets_base == number*3              # У всех питомцев есть имя, возраст и порода.
   assert len(pets_name) == number           # У всех питомцев разные имена.
   assert len(pets_set) == number            # В списке нет повторяющихся питомцев.




