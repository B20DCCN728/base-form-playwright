import logging
import threading
import time
import colorlog
from playwright.sync_api import sync_playwright

import JSON
import dcom
import file

# Set up logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s:%(levelname)s: %(message)s'
))

logger = logging.getLogger('ЧВК «Вагнер»')
logger.addHandler(handler)

# Set the log level to INFO
logger.setLevel(logging.INFO)


def PlayWrightForm(current_thread: int, current_profile: int, current_wallet: dict, current_mail: str) -> None:
    if current_thread == 1:
        window_position = "0,0"
        executable_path = r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-119\chrome.exe"
    else:
        window_position = "960,0"
        executable_path = r"C:\Users\Nguyen Hoang Viet\.gologin\browser\orbita-browser-120\chrome.exe"

    with sync_playwright() as ap:
        browser = ap.chromium.launch_persistent_context(
            user_data_dir=f"D:\\Documents\\Gologin_Profile\\profile\\profile_{current_profile}",
            headless=False,
            devtools=False,
            executable_path=executable_path,
            args=[
                '--start-maximized',
                f'-window-position={window_position}',
                '--disable-blink-features=AutomationControlled',
            ]
        )

        page = browser.new_page()
        page.goto(
            "https://docs.google.com/forms/d/e/1FAIpQLSehuOu7hhT_98Heh3jbHwIGY9OhY-H5sDrAOCZraMp3L2nazA/viewform?usp"
            "=sf_link"
        )
        logger.info(f"Profile {current_profile} in thread {current_thread} went to form.")
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input'
        ).fill(current_mail)
        logger.info(f"Profile {current_profile} in thread {current_thread} filled mail.")
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
        ).fill(current_wallet["address"])
        logger.info(f"Profile {current_profile} in thread {current_thread} filled wallet.")
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]'
        ).click()
        logger.info(f"Profile {current_profile} in thread {current_thread} clicked on the file picker button.")
        time.sleep(4)

        username = page.frame_locator('iframe').nth(1).locator(
            'input[type="file"][jsname="G1bupd"]'
        )
        logger.info(f"Profile {current_profile} in thread {current_thread} located the file picker button.")

        username.set_input_files(r'C:\Users\Nguyen Hoang Viet\Downloads\screenshot-1708930425691.png')
        logger.info(f"Profile {current_profile} in thread {current_thread} uploaded the file.")
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="i18"]'
        ).click()
        logger.info(f"Profile {current_profile} in thread {current_thread} checked specific radio.")
        time.sleep(2)

        page.locator(
            'xpath=//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
        ).click()
        logger.info(f"Profile {current_profile} in thread {current_thread} clicked on the submit button.")
        time.sleep(2)

        page.close()
        browser.close()
        # Close browser
        time.sleep(2)


if __name__ == '__main__':
    # Read wallets from eth.json
    wallets = JSON.read("eth.json")
    logger.info(f"Read {len(wallets)} wallets from eth.json")
    # Read extension ids from export.txt
    emails = file.read_email("BAD2LJAVMB.txt")
    logger.info(f"Read {len(emails)} emails from BAD2LJAVMB.txt")

    # Setting up threads
    num_threads = 2
    profile = 0
    while profile < 99:
        dcom.connect()
        threads = []
        # Create 2 threads
        for num_thread in range(num_threads):
            thread = threading.Thread(
                target=PlayWrightForm,
                args=(
                    num_thread + 1,
                    profile + 1,
                    wallets[profile],
                    emails[profile][0]
                )
            )
            logger.info(f"Thread {num_thread + 1} created with profile {profile + 1}")
            # Append thread to threads
            threads.append(thread)
            # Increment profile
            profile += 1
            time.sleep(1)

        # Start and join threads
        for index, thread in enumerate(threads):
            logger.info(f"Starting profile {profile + 1} in thread {index + 1}...")
            thread.start()
        for index, thread in enumerate(threads):
            thread.join()
            logger.info(f"Profile {profile + 1} in thread {index + 1} is done.")

        # Clear threads
        threads.clear()
        dcom.disconnect()

    logger.info("All profiles are done.")

