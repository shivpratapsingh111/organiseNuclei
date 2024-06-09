import os
import yaml
import shutil
import argparse
import sys
import textwrap

defaultIds = ["http-missing-security-headers",  "tech-detect",  "missing-csp",  "display-via-header",  "kafka-topics-list",  "cors-misconfig",  "waf-detect",  "dns-waf-detect",  "secui-waf-detect",  "spring-detect",  "favicon-detect",  "akamai-detect",  "akamai-cache-detect",  "missing-sri",  "robots-txt-endpoint",  "aws-detect",  "aws-cloudfront-service",  "https-to-http-redirect",  "caa-fingerprint",  "dns-saas-service-detection",  "mx-fingerprint",  "txt-fingerprint",  "tls-version",  "spf-record-detect",  "nameserver-fingerprint",  "dnssec-detection",  "mx-service-detector",  "dmarc-detect",  "php-user-ini",  "weak-cipher-suites",  "ssl-issuer",  "ssl-dns-names",  "wildcard-tls",  "minecraft-enum",  "request-based-interaction",  "oidc-detect",  "security-txt",  "rdap-whois",  "options-method",  "robots-txt",  "apple-app-site-association",  "external-service-interaction",  "azure-domain-tenant",  "old-copyright",  "intercom",  "metatag-cms",  "xss-deprecated-header",  "addeventlistener-detect",  "deprecated-tls",  "erlang-daemon",  "mismatched-ssl-certificate",  "pop3-detect",  "google-floc-disabled",  "aws-cloudfront-service",  "aws-bucket-service",  "detect-sentry",  "email-extractor",  "http-trace",  "apache-detect",  "revoked-ssl-certificate",  "expired-ssl",  "microsoft-iis-version",  "fingerprinthub-web-fingerprints",  "public-documents",  "google-frontend-httpserver",  "wadl-api",  "nginx-version",  "openssh-detect",  "insecure-cipher-suite-detect",  "generic-c2-jarm",  "kafka-topics-list",  "openresty-detect",  "gpc-json",  "wordpress-readme-file",  "wp-user-enum",  "aws-sftp-detect",  "wordpress-wordpress-seo",  "wordpress-post-types-order",  "wordpress-maintenance",  "wordpress-login",  "wordpress-redirection",  "wordpress-svg-support",  "wordpress-xmlrpc-listmethods",  "untrusted-root-certificate",  "switch-protocol",  "sitemap-detect"]

outputFolder = ".separated"
configFile= os.path.join(os.path.join(os.getcwd(), outputFolder), ".config")



def usage():
    print("Examples:")
    print(f"\n[+] Provide file with `-i` flag containing `id` to exclude, one per line: \n\t- {sys.argv[0]} -dir /home/nuclei-templates -i ids.txt")
    print(f"\n[+] If you don't provide a file, It will exclude templates set by default:\n\t- {sys.argv[0]} -dir /home/nuclei-templates\n")




def extractId(templatePath):
    with open(templatePath, 'r') as file:
        ids = file.read().splitlines()
    return ids




def excludeTemplates(directory, ids, outputDir):
    global configFile

    if not os.path.exists(directory):
        print(f"[+] {directory}: This path does not exists")
    else: 

        if not os.path.exists(outputDir):
            os.mkdir(outputDir)

        with open(configFile, 'w') as f:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.yaml') or file.endswith('.yml'):
                        templatePath = os.path.join(root, file)

                        with open(templatePath, 'r') as yaml_file:
                            try:
                                content = yaml.safe_load(yaml_file)
                                if 'id' in content and content['id'] in ids:
                                    shutil.move(templatePath, os.path.join(outputDir, file))
                                    print(f"[+] Moved: {templatePath} ---> {outputDir}/")
                                    f.write(f'{templatePath}\n')

                            except yaml.YAMLError as exc:
                                print(f"[+] Error parsing {templatePath}: {exc}")
            print(f"\n---\n\n[+] All unecessary templates moved to {os.path.join(os.getcwd(), outputDir)}/ (Hidden folder in linux)")
            print(f"[+] Count: {len(os.listdir(directory))}\n\n---")
        f.close()




def reverseAction():
    global configFile
    with open(configFile, 'r') as file:

        for line in file:

            fileNameToMove = os.path.basename(line.strip())
            filePathToMove = f"{outputFolder}/{fileNameToMove}"
            
            shutil.move(filePathToMove, line.strip())
            print(f"[+] Moved back: {filePathToMove} to {line.strip()}")

        print(f"\n---\n\n[+] All templates moved back to their origin\n")
    file.close()
# Remove output folder and .config file and reversing the action
    shutil.rmtree(outputFolder)




def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='Separate Nuclei Templates files based on ID match.', epilog=textwrap.dedent(f"""Examples:
[+] Provide file with `-i` flag containing `id` to exclude, one per line: 
\t- {sys.argv[0]} -dir /home/nuclei-templates -i ids.txt
[+] If you don't provide a file, It will exclude templates set by default:
\t- {sys.argv[0]} -dir /home/nuclei-templates
[+] To move back all the templates back to their origin:
\t- {sys.argv[0]} -rev"""))
    
    
    parser.add_argument('-dir', required=False, help='Directory containing Nuclei Templates files')
    parser.add_argument('-rev', required=False, action='store_true' ,help='Reverse the action, to move back all the templates back to their origin')
    parser.add_argument('-i', required=False, help='File containing nuclei template IDs to exclude, Example: tech-detect, missing-csp, display-via-header')
    
    args = parser.parse_args()


# -i and -dir
    if args.i and args.dir and not args.rev:
        ids = extractId(args.i)
        excludeTemplates(args.dir, ids, outputFolder)

# -dir
    elif args.dir and not args.rev and not args.i:
        global defaultIds
        excludeTemplates(args.dir, defaultIds, outputFolder)

# None
    elif args.i==None and args.dir==None and args.rev==False:
        defaultDirectory = f"/home/{os.getlogin()}/nuclei-templates"
        if not os.path.exists(defaultDirectory):
            print(f"---\n[+] nuclei-templates folder not found in home: {defaultDirectory}\n[+] Please provide template folder path with `-dir` flag\n[+] Example: python3 {sys.argv[0]} -dir resources/nuclei-templates\n---")
        else: 
            excludeTemplates(defaultDirectory, defaultIds, outputFolder)

# -rev
    elif args.rev and (args.i==None and args.dir==None):
        reverseAction()

# -i
    elif args.i and not args.dir and not args.rev:
        print("[+] Incorrect use of flags!")             
        sys.exit(1)

    else: 
        print("[+] Incorrect use of flags!")
        sys.exit(1)




if __name__ == "__main__":


    try:
        main()
    except KeyboardInterrupt:
        print(f"\nProcess interrupted by {os.getlogin()} (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


# commands to filterout more by searching on some results
'''cat info.txt |grep -v dns-saas-service-detection | grep -v tls-version | grep -v mx-finger | grep -v txt-finger | grep -v caa-finger | grep -v dmarc-dete | grep -v mx-service-dete | grep -v dnssec-dete | grep -v spf-record | grep -v nameserver-finger | grep -v ssl-dns-names | grep -v ssl-issuer | grep -v wildcard-tls | grep -v minecraft-enum | grep -v request-based-interaction | grep -v waf-detect | grep -v oidc-detect | grep -v cors-miscon | grep -v missing-sri| grep -v security-txt | grep -v rdap-whois | grep -v robots-txt-endpoint | grep -v robots-txt | grep -v options-method | grep -v apple-app-site-association | grep -v aspx-debug-mode | grep -v exposed-gitignore | grep -v external-service-interaction| grep -v keycloak-openid-config | grep -v mercurial-hgignore  | grep -v http-missing-security-headers | grep -v azure-domain-tenant | grep -v intercom | grep -v old-copyr | grep -v tech-dete | grep -v azure-domain-ten | grep -v aws-dete  | grep -v metatag | grep -v missing-csp | grep -v addeventlistener-detect | grep -v display-via-header | grep -v xss-depre | grep -v deprecated-tls | grep -v pop3 | grep -v s3-detect| grep -v google-floc-disabled | grep -v default-nginx-page | grep -v aws-bucket-service | grep -v aws-cloudfront-service | grep -v akamai-detect | grep -v akamai-cache | grep -v favicon-detec | grep -v detect-sentry | grep -v http-trace | grep -v apache-detect | grep -v email-extract | grep -v cookies-without-httponly-secure | grep -v form-detection | grep -v https-to-http-redirect | grep -v dangling-cname | grep -v basic-auth-detect | grep -v microsoft-iis-version | grep -v insecure-cipher-suite-det | grep -v openssh-detect | grep -v generic-c2-jarm | grep -v kafka-topics-list | grep -v spring-detect | grep -v fingerprinthub-web-fingerprints| grep -v openresty-detect | grep -v wordpress-readme-file | grep -v gpc-json | grep -v nginx-version | grep -v wordpress-wordpress-seo | grep -v aws-sftp-detect | grep -v wordpress-post-types-order | grep -v wordpress-detect


cat low.txt | grep -v php-user-ini | grep -v weak-cipher-suites | grep -v erlang-daemon | grep -v mismatched-ssl-certificate | grep -v expired-ssl | grep -v revoked-ssl-certificate | grep -v wp-user-enum | grep -v untrusted-root-certificate
'''