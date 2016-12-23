import os

project_name = "instantsanta"

plugins = [
    "oz.core",
    project_name,
]

app_options = dict(
    port = int(os.environ.get("PORT", 8000)),
    debug = os.environ.get("DEBUG", "false") == "true",
    static_path = "static",
    template_path = "templates",
    xsrf_cookies = False,
    gzip = True
)
