FROM cicadatesting/cicada-distributed-base-image:1.3.0

RUN apt-get update
RUN apt-get install -y bash unzip curl xvfb libxi6 libgconf-2-4 gnupg

# Install chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

# Install ChromeDriver.
# NOTE: may have to change this to appropriate version of google-chrome-stable listed here: https://www.ubuntuupdates.org/pm/google-chrome-stable
RUN wget -N https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

# Install selenium
RUN pip install selenium

# Install tests
COPY . .

ENTRYPOINT ["python", "-u", "test.py"]
