# Airbrowser Docker Image (Optimized)
FROM python:3.11-slim-bullseye AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (with retry for transient network errors)
RUN for i in 1 2 3 4 5; do curl -LsSf https://astral.sh/uv/install.sh | sh && break || sleep 5; done
ENV PATH="/root/.local/bin:$PATH"

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Final stage
FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV HOME=/home/browseruser
ENV ENABLE_MCP=true
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Install all dependencies in a single layer with aggressive cleanup
# Retry logic for transient network failures
RUN for i in 1 2 3; do apt-get update && break || sleep 5; done \
    && for i in 1 2 3; do apt-get install -y --no-install-recommends \
    # Minimal system tools
    wget curl ca-certificates gnupg xvfb supervisor procps nginx openssl \
    # Fonts (minimal set)
    fonts-liberation fonts-dejavu-core fontconfig \
    # X11/VNC (minimal)
    fluxbox x11vnc xterm dbus-x11 \
    # Chrome dependencies
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 \
    libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 \
    libnspr4 libnss3 libwayland-client0 libxcomposite1 \
    libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils \
    # PyAutoGUI dependencies
    python3-tk scrot xdotool xsel xclip \
    libxtst6 libxss1 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
    # Locale
    locales \
    && break || sleep 5; done \
    && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
    # Install Chrome
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm ./google-chrome-stable_current_amd64.deb \
    # Cleanup (be careful not to break Chrome)
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* /usr/share/man/* /usr/share/info/* \
    && rm -rf /var/cache/apt/*

# Copy Python packages and scripts from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

# Install ChromeDriver (stable - cache this)
RUN seleniumbase install chromedriver

# Install noVNC (stable - cache this)
RUN mkdir -p /opt \
    && curl -sL https://github.com/novnc/noVNC/archive/v1.3.0.tar.gz | tar xz -C /opt/ \
    && mv /opt/noVNC-1.3.0 /opt/noVNC \
    && ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html \
    && rm -rf /opt/noVNC/docs /opt/noVNC/tests /opt/noVNC/*.md \
    && pip install --no-cache-dir websockify

# Create directories and user (stable - cache this)
RUN mkdir -p /app/{browser-profiles,screenshots,downloads,certs,src} \
    /var/log/supervisor /var/run /opt/vnc \
    /home/browseruser/.fluxbox /home/browseruser/.cache/selenium \
    /tmp/browser-queue /tmp/browser-status /tmp/browser-responses \
    && chmod 777 /tmp/browser-queue /tmp/browser-status /tmp/browser-responses \
    && mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix \
    && groupadd -r browseruser && useradd -r -g browseruser -G audio,video browseruser \
    && chown -R browseruser:browseruser /app /home/browseruser /var/log/supervisor /var/run \
    && chown -R browseruser:browseruser /usr/local/lib/python3.11/site-packages/seleniumbase/drivers/ \
    && touch /home/browseruser/.Xauthority && chown browseruser:browseruser /home/browseruser/.Xauthority

# Copy configs (rarely change)
RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
COPY docker/nginx.conf.template /etc/nginx/nginx.conf.template
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy application code LAST (changes frequently)
COPY src/ ./src/
COPY setup.py README.md ./
ENV PYTHONPATH="/app/src"

EXPOSE 8000 3000 5900 6080

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:8000/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
