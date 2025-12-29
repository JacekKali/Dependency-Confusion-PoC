# ⚠️ Dependency Confusion PoC

**RESEARCH PROJECT - FOR EDUCATIONAL PURPOSES ONLY - DO NOT INSTALL**

## You Likely Installed This By Accident

This is a **Proof of Concept** demonstrating the **dependency confusion vulnerability**. It collects and sends username and hostname for usage statistics only.

## If You're Here By Accident

Your internal package name conflicts with this PoC. **How to protect yourself:**

- Use `pip install --index-url <your-internal-registry>` to specify your registry
- Register your package name on PyPI first
- Use a private PyPI registry
- Rename internal packages to avoid conflicts

## Purpose

This is for **educational security awareness** to help organizations understand and prevent dependency confusion attacks.

**Learn more:**
- [Alex Birsan PoC explained](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
- [CICD-SEC-3: Dependency Chain Abuse](https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-03-Dependency-Chain-Abuse)
