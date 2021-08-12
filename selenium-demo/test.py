from datetime import datetime
from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cicadad.core.scenario import UserCommands
from cicadad.core.decorators import scenario, user_loop, users_per_container
from cicadad.core.engine import Engine

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
WINDOW_SIZE = "1920,1080"

engine = Engine()


def chromedriver_user_loop(user_commands: UserCommands, context: dict):
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options
    )

    start = datetime.now()

    output, exception, logs = user_commands.run(
        context=context,
        driver=driver,
    )

    end = datetime.now()

    user_commands.report_result(
        output,
        exception,
        logs,
        time_taken=(end - start).seconds,
    )

    driver.close()


@scenario(engine)
@users_per_container(1)
@user_loop(chromedriver_user_loop)
def get_tutorial(context, driver: Any):
    driver.get("https://cicadatesting.github.io/cicada-distributed-docs/")

    em = driver.find_element_by_link_text("Tutorial")

    assert em is not None
    em.click()

    url = driver.current_url

    assert "installation" in url, f"Did not navigate to tutorial; current url is {url}"
    return url


if __name__ == "__main__":
    engine.start()
