from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


class testsE2E(LiveServerTestCase):
    def test_login(self):
        selenium = webdriver.Chrome()
        # Choose your URL to visit
        selenium.get('http://127.0.0.1:8000/')
        time.sleep(2)
        # Find the elements you need to submit the form
        usuarioT = selenium.find_element(By.ID, 'username')
        contraT = selenium.find_element(By.ID, 'password')
        logInT = selenium.find_element(By.ID, 'ingresar')
        time.sleep(2)
        usuarioT.send_keys('Filantropia')
        contraT.send_keys('F1234567')

        logInT.send_keys(Keys.RETURN)

        # Use assertEqual to check if the current URL is as expected
        expected_url = 'http://127.0.0.1:8000/home/'
        self.assertEqual(expected_url, selenium.current_url)
        time.sleep(1)

    def test_login_except(self):
        selenium = webdriver.Chrome()
        # Choose your URL to visit
        selenium.get('http://127.0.0.1:8000/')
        time.sleep(2)

        # Find the elements you need to submit the form
        usuarioT = selenium.find_element(By.ID, 'username')
        contraT = selenium.find_element(By.ID, 'password')
        logInT = selenium.find_element(By.ID, 'ingresar')

        # Introduce credenciales incorrectas
        usuarioT.send_keys('messi')
        contraT.send_keys('1234')
        time.sleep(2)

        logInT.send_keys(Keys.RETURN)

        # Verifica que el bloque de error esté presente en el DOM
        blockEcp = selenium.find_element(
            By.XPATH, '/html/body/section/div/div/div/div/div/div[2]/div/form/p')
        # Verifica que el bloque sea visible
        self.assertTrue(blockEcp.is_displayed())
        time.sleep(2)
        # Verifica que el URL actual sea el esperado (que no haya redirección a la página de inicio)
        expected_url = 'http://127.0.0.1:8000/'
        self.assertEqual(expected_url, selenium.current_url)

    def test_reg_estudiante(self):
        selenium = webdriver.Chrome()
        # Choose your URL to visit
        selenium.get('http://127.0.0.1:8000/estudiantes/')
        time.sleep(2)

        # Find the elements you need to submit the form
        buttonRegEst = selenium.find_element(By.ID, 'regEstud')
        buttonRegEst.send_keys(Keys.RETURN)
        expected_url = 'http://127.0.0.1:8000/students_info/'
        self.assertEqual(expected_url, selenium.current_url)

        time.sleep(2)
        name = selenium.find_element(By.ID, 'name')
        code = selenium.find_element(By.ID, 'code')
        selectDocument = selenium.find_element(By.ID, 'selDoc')
        selectDoc = Select(selectDocument)
        numDoc = selenium.find_element(By.ID, 'numDoc')
        selectGenero = selenium.find_element(By.ID, 'selectGnr')
        selectGnr = Select(selectGenero)
        email = selenium.find_element(By.ID, 'email')
        emailUni = selenium.find_element(By.ID, 'emailUni')
        icfes = selenium.find_element(By.ID, 'icfes')
        birth = selenium.find_element(By.ID, 'start')
        phone = selenium.find_element(By.ID, 'phone')
        promedio = selenium.find_element(By.ID, 'promedio')
        creditos = selenium.find_element(By.ID, 'creditos')
        sendForm = selenium.find_element(By.ID, 'sendForms')

        # Introduce credenciales
        name.send_keys('Juan Perez')
        code.send_keys('123456789')
        selectDoc.select_by_value('CC')
        numDoc.send_keys('987654321')
        selectGnr.select_by_value('M')
        email.send_keys('juan.perez@example.com')
        emailUni.send_keys('juan.perez@universidad.edu')
        icfes.send_keys('345')
        birth.send_keys('19-07-2004')
        phone.send_keys('1234567890')
        promedio.send_keys('4.5')
        creditos.send_keys('120')

        time.sleep(1)

        sendForm.send_keys(Keys.RETURN)
        name = selenium.find_element(By.ID, 'name')
        self.assertEqual("", name.get_attribute("value"))

    def test_upload_scholarship(self):
        selenium = webdriver.Chrome()
        selenium.get('http://127.0.0.1:8000/estudiantes/')
        time.sleep(2)

        # Choose your URL to visit
        buttonRegEst = selenium.find_element(By.ID, 'subirBeca')
        buttonRegEst.send_keys(Keys.RETURN)
        selenium.find_element(By.ID, 'file').send_keys(
            "C:\\Users\\Jacobo Ossa\\OneDrive - Universidad Icesi (@icesi.edu.co)\\Escritorio\\TestApoyoFinanciero.xlsx")
        uploadbutton = selenium.find_element(By.ID, 'inputGroupFileAddon04')
        uploadbutton.send_keys(Keys.RETURN)
        # Wait for some time for the processing to complete (adjust the sleep duration as needed)
        time.sleep(2)
        # Find the div element that is expected after uploading the file
        expected_div = selenium.find_element(By.ID, 'uploadSucess')

        # Assert that the div is displayed
        self.assertTrue(expected_div.is_displayed())

    def test_request_info(self):
        # Choose your URL to visit
        selenium = webdriver.Chrome()
        selenium.get('http://127.0.0.1:8000/estudiantes/')
        buttonReqInfo = selenium.find_element(By.ID, 'reqInfo')
        buttonReqInfo.send_keys(Keys.RETURN)
        expected_url = 'http://127.0.0.1:8000/askInfoUpdate/'
        self.assertEqual(expected_url, selenium.current_url)

        time.sleep(2)

        # Find the elements you need to submit the form
        select_Office = selenium.find_element(By.ID, 'selOffice')
        selectOfic = Select(select_Office)
        selectOfic.select_by_value('1')
        time.sleep(1)
        student_items = selenium.find_elements(By.CLASS_NAME, 'student-item')
        selected_student = student_items[0]
        selected_student.click()
        time.sleep(1)
        submit = selenium.find_element(By.ID, 'sendReq')
        submit.send_keys(Keys.RETURN)
        expected_message = selenium.find_element(By.ID, 'message')
        time.sleep(3)
        self.assertTrue(expected_message.is_displayed())

    def test_upload_BU_Activities(self):
        selenium = webdriver.Chrome()
        selenium.get('http://127.0.0.1:8000/estudiantes/')
        time.sleep(2)

        # Choose your URL to visit
        buttonRegEst = selenium.find_element(By.ID, 'uploadBU')
        buttonRegEst.send_keys(Keys.RETURN)
        selenium.find_element(By.ID, 'file').send_keys(
            "C:\\Users\\Jacobo Ossa\\OneDrive - Universidad Icesi (@icesi.edu.co)\\Escritorio\\TestBienestarUniversitario.xlsx")
        uploadbutton = selenium.find_element(By.ID, 'inputGroupFileAddon04')
        uploadbutton.send_keys(Keys.RETURN)
        # Wait for some time for the processing to complete (adjust the sleep duration as needed)
        time.sleep(2)
        # Find the div element that is expected after uploading the file
        expected_div = selenium.find_element(By.ID, 'succesfulMess')

        # Assert that the div is displayed
        self.assertTrue(expected_div.is_displayed())

    def test_upload_Academic_Report(self):
        selenium = webdriver.Chrome()
        selenium.get('http://127.0.0.1:8000/estudiantes/')
        time.sleep(2)

        # Choose your URL to visit
        buttonRegEst = selenium.find_element(By.ID, 'academicRprt')
        buttonRegEst.send_keys(Keys.RETURN)
        selenium.find_element(By.ID, 'file').send_keys(
            "C:\\Users\\Jacobo Ossa\\OneDrive - Universidad Icesi (@icesi.edu.co)\\Escritorio\\A00381321.pdf")
        uploadbutton = selenium.find_element(By.ID, 'inputGroupFileAddon04')
        uploadbutton.send_keys(Keys.RETURN)
        # Wait for some time for the processing to complete (adjust the sleep duration as needed)
        time.sleep(2)
        # Find the div element that is expected after uploading the file
        expected_div = selenium.find_element(By.ID, 'succesfulMess')

        # Assert that the div is displayed
        self.assertTrue(expected_div.is_displayed())

    def test_upload_BU_Activities(self):
        selenium = webdriver.Chrome()
        selenium.get('http://127.0.0.1:8000/estudiantes/')
        time.sleep(2)

        # Choose your URL to visit
        buttonRegEst = selenium.find_element(By.ID, 'reportCREA')
        buttonRegEst.send_keys(Keys.RETURN)
        selenium.find_element(By.ID, 'file').send_keys(
            "C:\\Users\\Jacobo Ossa\\OneDrive - Universidad Icesi (@icesi.edu.co)\\Escritorio\\TestCREA.xlsx")
        uploadbutton = selenium.find_element(By.ID, 'inputGroupFileAddon04')
        uploadbutton.send_keys(Keys.RETURN)
        # Wait for some time for the processing to complete (adjust the sleep duration as needed)
        time.sleep(2)
        # Find the div element that is expected after uploading the file
        expected_div = selenium.find_element(By.ID, 'succesfulMess')

        # Assert that the div is displayed
        self.assertTrue(expected_div.is_displayed())
