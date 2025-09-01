## **What is DNS** 

- At its core, the **Domain Name System (DNS)** is the phonebook of the internet. Humans remember names like `google.com` or `hackthebox.com`, but computers communicate using IP addresses like `142.251.42.206`.

### Tools used for **DNS Enumeration** 

-  `nslookup`, `dig`, `dnsrecon` `fierce.`

### How does it work 

1. **The Query:** You type `www.example.com` into your browser.
    
2. **The Recursive Resolver (Your ISP's DNS Server):** Your computer doesn't know the answer, so it asks a **Recursive Resolver** (like your ISP's server, or public ones like `8.8.8.8` (Google) or `1.1.1.1` (Cloudflare)). Its job is to find the answer for you by doing the legwork.
    
3. **The Root Name Server:** The resolver first asks a **Root Server** (there are 13 logical clusters of these). The root server doesn't know the IP for `example.com`, but it knows who's in charge of all `.com` domains. It directs the resolver to the **Top-Level Domain (TLD) Name Servers** for `.com`.
    
4. **The TLD Name Server:** The resolver asks a `.com` TLD server. This server doesn't know `example.com` either, but it knows the **Authoritative Name Servers** for the `example.com` domain (e.g., `ns1.example.com`). It sends that information back.
    
5. **The Authoritative Name Server:** The resolver finally asks the Authoritative Name Server for `example.com`. This server _is_ the ultimate source of truth for that domain. It holds the **DNS records**. It looks up the `www` record and returns the corresponding IP address (e.g., `93.184.216.34`) to the resolver.
    
6. **The Response:** The resolver caches this information (to speed up future requests) and returns the final IP address to your computer.
    
7. **Connection:** Your browser can now initiate a connection to `93.184.216.34`.
---
### What are **DNS Records**

- **A Records:** IP addresses of hosts.
    
- **MX Records:** Mail servers (a prime target).
    
- **TXT Records:** Often contain **SPF (Sender Policy Framework) / DKIM (DomainKeys Identified Mail) settings** for email, or sometimes even accidental leaks of internal data or API keys.

	-  **SPF Record:** A note that says, **"Only these specific mail servers are allowed to send email on behalf of** `@mycompany.com`. If you get mail from anyone else, it's probably fake."
    
	- **DKIM Record:** A note that **provides a special digital signature to prove that an email from** `@mycompany.com` **is genuine and hasn't been tampered with, like an official wax seal on a letter.**
    
- **NS Records:** Identifies the authoritative name servers. Are they the company's, or a third-party's? This defines attack surface.
    
- **CNAME Records:** Can reveal the true hostnames of services (e.g., `webapp.prod.us-east-1.elasticbeanstalk.amazonaws.com`), exposing the underlying infrastructure.

### What is DNS Zone Transfer AXFR

-  A **Zone Transfer (AXFR)** is a mechanism used by *DNS servers to replicate this entire "phonebook" from a **primary (master)** server to a **secondary (slave)** server.*
-  It's a legitimate and necessary function for **ensuring redundancy and reliability.**

### Output : 

```bash title:output.md

python3 dns/dns_enum.py youtube.com

A records for youtube.com
 142.251.43.46

AAAA records for youtube.com
 2404:6800:4009:81c::200e

MX records for youtube.com
 0 smtp.google.com.

TXT records for youtube.com
 "google-site-verification=QtQWEwHWM8tHiJ4s-jJWzEQrD_fF3luPnpzNDH-Nw-w"
 "v=spf1 include:google.com mx -all"
 "facebook-domain-verification=64jdes7le4h7e7lfpi22rijygx58j1"

SOA records for youtube.com
 ns1.google.com. dns-admin.google.com. 801461948 900 900 1800 60

NS records for youtube.com
 ns3.google.com.
 ns1.google.com.
 ns4.google.com.
 ns2.google.com.

Attempting AXFR for youtube.com
 Zone transfer failed: 
 

```