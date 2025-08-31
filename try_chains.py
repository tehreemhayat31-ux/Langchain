from chains import generate_service_info

def main():
    query = "How to renew CNIC in Pakistan?"
    response = generate_service_info(query)
    
    print("\n--- Outline ---")
    print(response["outline"])
    print("\n--- Guide ---")
    print(response["guide"])
    print("\n--- FAQs ---")
    print(response["faqs"])
    print("\n--- Important Notes ---")
    print(response["important_notes"])

if __name__ == "__main__":
    main()
