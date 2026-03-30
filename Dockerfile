# Clawdbot gateway — patch so Anthropic "API usage limits" triggers model fallback
FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
	git ca-certificates curl python3 jq zip \
	python3-requests python3-yaml \
	&& ln -sf /usr/bin/python3 /usr/local/bin/python \
	&& rm -rf /var/lib/apt/lists/*

# Skills que en la UI sugieren `brew`: en Docker usamos binarios Linux desde GitHub (misma herramienta).
# goplaces → Google Places API (New); requiere GOOGLE_PLACES_API_KEY en el entorno.
# gog → Google Workspace (Gmail, Calendar, Drive…); OAuth interactivo la primera vez (ver docs/SKILLS-DOCKER.md).
ARG GOPLACES_VERSION=0.3.0
ARG GOGCLI_VERSION=0.12.0
RUN set -eu; \
	ARCH="$(dpkg --print-architecture)"; \
	case "$ARCH" in \
		amd64) GOLINUX=amd64 ;; \
		arm64) GOLINUX=arm64 ;; \
		*) echo "Unsupported dpkg arch: $ARCH (need amd64 or arm64)" >&2; exit 1 ;; \
	esac; \
	curl -fsSL "https://github.com/steipete/goplaces/releases/download/v${GOPLACES_VERSION}/goplaces_${GOPLACES_VERSION}_linux_${GOLINUX}.tar.gz" \
		| tar -xzf - -C /usr/local/bin goplaces; \
	chmod +x /usr/local/bin/goplaces; \
	curl -fsSL "https://github.com/steipete/gogcli/releases/download/v${GOGCLI_VERSION}/gogcli_${GOGCLI_VERSION}_linux_${GOLINUX}.tar.gz" \
		| tar -xzf - -C /tmp gog; \
	mv /tmp/gog /usr/local/bin/gog; \
	chmod +x /usr/local/bin/gog

RUN npm install -g clawdbot@latest

# Patch ERROR_PATTERNS.billing so "usage limits" / "regain access" trigger failover to Kimi
COPY patches/patch-failover-errors.js /tmp/patches/
RUN node /tmp/patches/patch-failover-errors.js

# WebSocket relay: permitir IP bridge Docker (172.x) para extensión Chrome en Mac (port-forward)
COPY patches/patch-extension-relay-docker.js /tmp/patches/
RUN node /tmp/patches/patch-extension-relay-docker.js

USER node

EXPOSE 18789

CMD ["clawdbot", "gateway", "--port", "18789", "--bind", "lan"]
