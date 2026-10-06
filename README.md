# PodPitch plugins

Find podcasts that fit your expertise, audience, or story through ChatGPT, Claude, and MCP agents. Public discovery works without a PodPitch account and never returns contact email addresses.

Existing customers can connect their PodPitch account in the browser to manage campaigns, drafts, inbox replies, templates, and outreach. Existing team permissions, subscription rules, and pitch limits apply. The agent feedback tool records reproducible bugs for PodPitch's engineering team.

- ChatGPT package: `chatgpt/podpitch`
- Claude package: `claude/podpitch`
- MCP endpoint: `https://api.podpitch.com/v1/mcp`
- Website: https://podpitch.com
- Privacy: https://app.podpitch.com/privacy
- Terms: https://app.podpitch.com/terms

Directory review and publication are separate from these installation files. A package in this repository does not mean its directory listing has been approved.

## Claude first-use catalog

The Claude skill includes a dated subset of 5,848 public catalog records for hosts that cannot reach PodPitch's live discovery endpoint. Version 1.0.4 stores them in 34 JSON files, each under 128 KB, with a catalog index and a standard-library Python helper. Search, exact show details, audience estimates and the demo link are available together without connector setup when the host can execute or read the bundled files. Host permissions still apply.

The sharded package was executed in native Claude without connectors or network access on October 6, 2026. The index and unique record count matched, topic and category searches returned shows, and details matched the returned ID. All records match the preceding snapshot. Eighteen subprocess tests cover both catalog layouts. This verifies package compatibility; directory approval and a fresh published installation remain separate release checks.
