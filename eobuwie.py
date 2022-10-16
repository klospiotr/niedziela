import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from faker import Faker

#PARAMETRY TESTU
caps = {}
caps['browserName'] = 'edge'
GRID_HUB_URL = "127.0.0.1/wd/hub"

# DANE TESTOWE
haslo = "DSfbv76564@@@"



class RejestracjaNowegoUzytkownika(unittest.TestCase):
    def setUp(self):
        # WARUNKI WSTĘPNE
        # 1. Otwarta strona główna
        #self.driver = webdriver.Chrome()
        self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub", desired_capabilities=DesiredCapabilities.FIREFOX)
        self.driver.maximize_window()
        self.driver.get("https://www.eobuwie.com.pl/")
        self.faker = Faker
        # (2. Użytkownik niezalogowany)
        # Zamknij alert o ciasteczkach
        self.driver.find_element(By.CLASS_NAME, "e-button--type-primary.e-button--color-brand.e-consents-alert__button.e-button").click()

    def tearDown(self):
        # Zakończenie testu
        self.driver.quit()

    def testBrakPodaniaImienia(self):
        sleep(2)
        # driver = self.driver
        # 1. Kliknij „Zarejestruj”
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zarejestruj").click()
        # 2.Wpisz nazwisko
        nazwisko = self.driver.find_element(By.ID, "lastname")
        nazwisko.send_keys("Nowak")
        # 3. Wpisz adres e-mail
        adres_mail = self.driver.find_element(By.ID, "email_address")
        adres_mail.send_keys("jannowak12341234@gmail.com")
        # 4. Wpisz hasło (co najmniej 6 znaków)
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(haslo)
        # 5. Wpisz ponownie hasło w celu potwierdzenia
        passwordconf = self.driver.find_element(By.ID, "confirmation")
        passwordconf.send_keys(haslo)
        # 6. Zaznacz „Oświadczam, że zapoznałem się z treścią Regulaminu serwisu i akceptuję
        # jego postanowienia.”
        self.driver.find_element(By.XPATH, '//label[@class="checkbox-wrapper__label"]').click()
        # OSTROŻNIE!!!!
        # 7. Kliknij „Załóż nowe konto” (tylko dla przypadków niegatywnych!)
        self.driver.find_element(By.XPATH, '//button[@data-testid="register-create-account-button"]').click()
        ### OCZEKIWANY REZULTAT ####
        # Użytkownik otrzymuje informację „To pole jest wymagane” pod imieniem
        # 1. Szukam pola imię
        imie = self.driver.find_element(By.NAME, "firstname")
        # 2. Szukam spana z błędem obok pola imię (nad nazwiskiem) przy pomocy 2 metod
        error_span = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').near(imie))
        error_span2 = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').above(nazwisko))
        # Sprawdzam, czy obie metody wskazują na ten sam element
        self.assertEqual(error_span.id, error_span2.id) # assertEqual
        # 3. Sprawdzam, czy jest tylko jeden taki span
        errory = self.driver.find_elements(By.XPATH, '//span[@class="form-error"]')
        liczba_errorow = len(errory)
        self.assertEqual(liczba_errorow, 1)
        # 4. Sprawdzam, czy treść tegoż spana brzmi "To pole jest wymagane"
        self.assertEqual("To pole jest wymagane", error_span.text)

# Jeśli uruchamiam z tego pliku
if __name__ == '__main__':
    # to uruchom testy
    unittest.main()