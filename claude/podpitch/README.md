# PodPitch

Find real podcasts by topic or name without an account. Public results contain show descriptions and listening links, never contact email addresses. Existing customers can connect PodPitch in the browser for account tools.

Account actions use the same team permissions, subscription rules, campaign modes, and pitch limits as the PodPitch product. Sending and scheduling remain deliberate user actions.

MCP endpoint: https://api.podpitch.com/v1/mcp

## First use in Claude

Ask for podcasts by topic or name. The skill uses the connected tools when available and the same public PodPitch catalog over HTTPS when the host offers URL-fetch or HTTP execution. That public fallback requires no sign-in or connector setup. It returns real descriptions and listening links without contact email addresses. If the connector and HTTP are unavailable, the skill searches a bundled public catalog snapshot locally without network access. Snapshot results are dated and cover a subset of the live catalog. It never uses general web search to find podcasts.

For account actions, connect podpitch through the plugin's Connectors tab and authorize your existing account in the normal browser flow. The skill never asks for passwords in chat. podpitch-discovery is optional for public discovery on hosts that offer URL-fetch or HTTP execution. Free accounts have one custom connector slot.

The demo link works without a connector: https://podpitch.com/demo?utm_source=claude&utm_medium=mcp&utm_campaign=podcast_discovery.

Each result includes available listener estimates, social follower totals and guest-format flags. Monthly listener estimates use four weeks of estimated downloads and are not verified unique listener counts. Current booking availability remains unknown without dated evidence.

Public HTTPS reads: `/v1/discovery/podcasts?query=TOPIC&limit=3` and `/v1/discovery/podcasts/RETURNED_ID` on `https://api.podpitch.com`. These reuse the MCP catalog filtering, sanitization, caching and rate limits.

## Data and support

Public search sends the requested topic or show name to PodPitch. Results contain public show information and listening links. Search responses are cached for 15 minutes. Contact email addresses require an existing account connection.

When you connect an account, PodPitch stores the user, team, requesting client, and approved permissions for up to 30 days. Access tokens expire after one hour. Refresh tokens rotate, and revoking a token disables the connection. Requested account changes and messages are stored under the same policy as changes made in PodPitch itself.

The public bug reporting tool stores a minimal technical report and timestamp without requiring an account. The authenticated reporting route also stores the connected user and team. The skill automatically reports distinct technical failures once per session, subject to the host's tool approval controls. Reports may remain longer than 30 days while needed for support and service improvement. Send only a short reproduction, never credentials or a full conversation. The plugin does not request chat history, memory, or unrelated files.

For product or security concerns, contact [neal@podpitch.com](mailto:neal@podpitch.com). For account connection problems, start the connection again in your agent and sign in to your existing PodPitch account in the browser.

## Examples

- Find three podcasts about climate technology and explain their fit using their descriptions.
- Compare the audiences and topics of two podcasts by their show IDs.
- Connect my existing PodPitch account and show my campaigns and pitch activity.

[Privacy](https://app.podpitch.com/privacy) | [Terms](https://app.podpitch.com/terms) | [PodPitch](https://podpitch.com)
