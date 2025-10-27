string = "Hi 🙂"
print_bytes = lambda s: print(' '.join(f'{b:02x}' for b in s))
stringUTF8 = string.encode("utf-8")
print("UTF-8:")
print_bytes(stringUTF8)
stringASCII = string.encode("ascii", errors="ignore")
# When we try to encode the string into ASCII, we get errors because character \U0001f642 isn't in the ASCII character set. If we still want the code to run we can ignore the errors. If we ignore the errors and print the bytes we still have "Hi " but the smiley face is missing.
print("ASCII (with errors ignored):")
print_bytes(stringASCII)
stringUTF16 = string.encode("utf-16")
print("UTF-16:")
print_bytes(stringUTF16)
# When we print the bytes of the UTF-8 encoded string, we see the bytes are represented in hexadecimal format, and the smiley face is represented by 4 bytes, while first characters are represented by 1 byte each.
# When we print the bytes of the UTF-16 encoded string, we see that each character is represented by 2 bytes, and the smiley face is represented by 4 bytes. We also see that there are 2 bytes in the beginning (ff fe) which isn't in the UTF-8 encoding.

print(stringUTF16.decode("utf-8", errors="ignore"))
# When we try to decode the UTF-16 string into UTF-8, we get errors because UTF-16 has the starting byte that UTF-8 doesn't have. If we ignore the errors and print the string, we get "Hi =B". The smiley face is missing because it wasn't decoded properly.
print(stringUTF16.decode("utf-16"))