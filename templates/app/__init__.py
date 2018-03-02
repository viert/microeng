from library.engine.baseapp import BaseApp


class App(BaseApp):
    VERSION = "1.0.0"

    def configure_routes(self):
        self.logger.info("Configuring conductor endpoints")

        self.logger.debug("main_ctrl at /")
        from app.controllers.main import main_ctrl
        self.flask.register_blueprint(main_ctrl, url_prefix="/")


app = App()
