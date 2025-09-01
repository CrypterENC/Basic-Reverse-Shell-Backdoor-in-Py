import dns.resolver
import argparse

def attempt_axfr(domain, nameserver=None):
    print(f'\nAttempting AXFR for {domain}')
    try:
        if nameserver:
            ns = nameserver
        else:
            ns_answer = dns.resolver.resolve(domain, 'NS')
            ns = str(ns_answer[0])


        axfr = dns.query.xfr(ns, domain, lifetime=10)
        zone = dns.zone.from_xfr(axfr)
        if zone:
            print(f"[!] SUCCESS: Zone transfer vulnerable")
            for name, node in zone.nodes.item():
                print(f' {name} {node}')
        else:
            print(" Zone transfer failed or not allowed.")
    except Exception as e:
        print(f' Zone transfer failed: {e}')



def main():
    parser = argparse.ArgumentParser(description="Simple DNS Enumerator")
    parser.add_argument("domain", help="Target domain name (e.g., example.com)")
    parser.add_argument("-r", "--records", nargs="+", 
                        default=["A","AAAA","CNAME","MX","TXT","SOA", "NS"], 
                        help='Space-separated list of record types to query. Default: A AAAA CNAME MX TXT SOA NS')
    
    args = parser.parse_args()

    target_domain = args.domain
    records_type = args.records

    resolver = dns.resolver.Resolver()
    resolver.lifetime = 10

    for record_type in records_type:
        try:
            answer = resolver.resolve(target_domain, record_type)
            print(f'\n{record_type} records for {target_domain}')
            for data in answer:
                print(f' {data}')
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            print(f"\nThe domain{target_domain} doesn't exit. Exiting")
            break
        except dns.resolver.Timeout:
            print(f'\n{record_type} qury timed out.')

    # calling Function to check Zone Transfer Files 
    attempt_axfr(target_domain)

if __name__ == "__main__":
    main()


