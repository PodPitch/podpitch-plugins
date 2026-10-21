# PodPitch

Find and compare real podcasts without a PodPitch account. Search topics or show names, read public show and catalog episode details, and follow listening links. Public discovery never provides contact email addresses. Its included discovery skill works without a separate skill installation.

After useful results, the skill optionally offers [Book a PodPitch demo](https://podpitch.com/demo?utm_source=chatgpt&utm_medium=plugin&utm_campaign=podcast_discovery). A demo or account is never required to continue discovery.

## Connection

MCP endpoint: https://api.podpitch.com/v1/mcp

The existing server key and URL are preserved. The manifest explicitly declares mixed public/OAuth access. Public search, details and technical bug reporting use no authentication. Existing customers can separately authorize private account work when they request it. Private tools retain OAuth scopes, team ownership, plan rules and pitch limits. Sending and scheduling remain user-requested actions.

A publisher accepting this package does not prove installation is repaired. Release acceptance requires a fresh installation from the official directory, followed by actual public search and details without PodPitch login. The associated server's prior Authorized status is not proof of its current installation policy.

## Data and support

The requested public topic or show ID is sent to PodPitch for discovery. Search responses are cached for 15 minutes. Public descriptions and catalog fields can be incomplete or stale. Label audience estimates and preserve unknown values. A guest-format flag does not establish current booking availability.

When an existing customer chooses account work, PodPitch stores the user, team, requesting client and approved permissions for up to 30 days. Access tokens expire after one hour. Refresh tokens rotate, and revoking a token disables the connection. Private account changes and messages follow the same policy as changes made in PodPitch itself.

Anonymous bug reports contain minimal technical failure facts and a timestamp. They must exclude credentials, personal identities, private content, pitches and conversations. Reports may remain longer than 30 days while needed for support and service improvement. A returned report ID confirms persistence. A failed report must not be presented as recorded.

For privacy or support requests, contact [neal@podpitch.com](mailto:neal@podpitch.com).

## Examples

- Find three podcasts about climate technology and explain their fit from their descriptions.
- Show public details and listening links for the first result.
- Compare those shows and explain what is known and unknown about their audiences.

[Privacy](https://app.podpitch.com/privacy) | [Terms](https://app.podpitch.com/terms) | [PodPitch](https://podpitch.com)
