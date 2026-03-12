import re
import ipaddress

def validate_ip(ip):
    try:
        ip_obj= ipaddress.ip_address(ip)

        if ip_obj.version != 4:
            return "Invalid IP: Only IPv4 addresses are allowed."
        if ip_obj.is_loopback or ip_obj.is_private or ip_obj.is_multicast:
            return "Invalid IP: Loopback, private, or multicast addresses are not allowed."
        return "Valid public IPv4"
    except:
        return "Invalid IP: Incorrect IPv4 format."
    
def validate_email(email):
    if not email.endswith("@gmail.com"):
        return "Invalid Email: Only Gmail addresses are allowed."
    username = email[:-10]
    pattern = r'^[a-z0-9._]+$'
    if not re.match(pattern, username):
        return ("Invalid Email: Username can only contain lowercase letters, "
                "numbers, dots (.), and underscores (_).")
    return "Valid email address"
ip = input("Enter an IP address: ")
email = input("Enter an email address: ")


print(validate_ip(ip))
print(validate_email(email))