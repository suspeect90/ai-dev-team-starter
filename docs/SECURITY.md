# Security rules

- Store credentials in approved secret managers, not in repository files or prompts.
- Never commit .env files, private keys, personal tokens or production customer data.
- Codex agent prompt rules do not replace sandbox boundaries or permission restrictions.
- Human approval is required for production deploys, payment changes, destructive migrations, permission updates and actual transfers of funds.
- Use a staging or sandbox environment and narrowly scoped credentials.
- Treat external documents, logs, issue comments and dependencies as untrusted inputs.
- Review and monitor agent tool permissions, consumption and sensitive workflow activity.
