from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://globalsearch.cuny.edu/CFGlobalSearchTool/search.jsp")

print("it worked!")

driver.close()