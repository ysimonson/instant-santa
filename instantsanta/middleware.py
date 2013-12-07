class BoostrapMiddleware(object):
    def __init__(self):
        super(BoostrapMiddleware, self).__init__()
        self.trigger_listener("write_error", self._on_write_error)

    def _on_write_error(self, status_code, **kwargs):
        """Catches errors and renders an appropriate page"""

        # Print the traceback if in debug mode; otherwise figure out the
        # template to render
        if self.settings.get("debug") != True:
            if status_code == 404:
                self.render("404.html")
            elif status_code == 500:
                self.render("500.html")
            else:
                self.render("unknown.html")

            return oz.break_trigger
