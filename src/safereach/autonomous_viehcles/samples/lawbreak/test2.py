from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

def click_locxy(dr, x, y, left_click=True):
    if left_click:
        ActionChains(dr).move_by_offset(x, y).click().perform()
    else:
        ActionChains(dr).move_by_offset(x, y).context_click().perform()
    ActionChains(dr).move_by_offset(-x, -y).perform()


if __name__ == "__main__":
    dr = webdriver.Chrome()
    dr.get('http://localhost:8888')
    dr.find_element(By.XPATH, "//div[@class='dreamview-tabs-tab']/div[contains(text(), 'PNC Mode')]").click()
    dr.find_element(By.CSS_SELECTOR, "div#rc-tabs-0-panel-Pnc input.dreamview-check-box-input").click()
    dr.find_element(By.XPATH, "//div[@id='rc-tabs-0-panel-Pnc']//button[contains(@class, 'css-8vdc0a-enter-this-mode-btn')]").click()
    dr.refresh()
    time.sleep(5)
    dr.find_element(By.XPATH, "//span[@class='anticon']").click()
    dr.find_element(By.XPATH, "//span[@title='Law38']").click()
    dr.find_element(By.XPATH, "//span[@title='Law38_1_2']").click()
    dr.find_elements(By.CLASS_NAME, "css-1e8gv-btn-container-btn-stop")[0].click()
    dr.find_elements(By.CLASS_NAME, "css-1e8gv-btn-container-btn-stop")[-1].click()
    dr.find_element(By.XPATH, "//button[contains(text(), 'Reset All')]").click()
    time.sleep(3)
    dr.find_element(By.XPATH, "//button[contains(text(), 'Setup All')]").click()
    time.sleep(3)
    dr.find_element(By.CLASS_NAME, "css-frigpz-btn-container-btn-reactive-btn-start").click()
    time.sleep(1)
    dr.find_elements(By.CLASS_NAME, "css-1e8gv-btn-container-btn-stop")[-1].click()
    time.sleep(1)
    dr.find_element(By.CLASS_NAME, "css-frigpz-btn-container-btn-reactive-btn-start").click()



    