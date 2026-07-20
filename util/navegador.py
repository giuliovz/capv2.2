from playwright.sync_api import sync_playwright

from config import (
    HEADLESS,
    TIMEOUT
)



class Navegador:


    def __init__(self):

        self.playwright = None

        self.browser = None

        self.page = None



    def iniciar(self):

        self.playwright = sync_playwright().start()


        self.browser = self.playwright.chromium.launch(

            headless=HEADLESS

        )


        self.page = self.browser.new_page(

            ignore_https_errors=True

        )


        self.page.set_default_timeout(

            TIMEOUT

        )


        return self.page



    def abrir(self, url):

        if not self.page:

            self.iniciar()


        try:

            self.page.goto(

                url,

                wait_until="domcontentloaded",

                timeout=30000

            )


        except Exception as erro:

            print(

                "Aviso carregando página:",

                erro

            )


        return self.page



    def fechar(self):

        if self.browser:

            self.browser.close()


        if self.playwright:

            self.playwright.stop()