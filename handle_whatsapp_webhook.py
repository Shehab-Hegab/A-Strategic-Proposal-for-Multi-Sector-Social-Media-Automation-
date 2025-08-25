# NOTE: This snippet demonstrates the core handling logic, not a full production application.
def handle_whatsapp_webhook(request_data, signature_header):
    """
    Processes incoming WhatsApp messages with signature validation and business routing.
    """
    # 1. Security: Verify the request signature to confirm authenticity.
    if not is_signature_valid(request_data, signature_header):
        log_security_event("Invalid webhook signature received.")
        return {"status": "error", "message": "Invalid Signature"}, 403
    # 2. Data Parsing: Safely extract essential data from the JSON payload.
    try:
        message = request_data['entry'][0]['changes'][0]['value']['messages'][0]
        customer_number = message['from']
        message_text = message['text']['body'].lower()
        business_account_id = request_data['entry'][0]['id']
    except (KeyError, IndexError):
        log_application_error("Malformed webhook payload received.")
        return {"status": "error", "message": "Malformed Payload"}, 400
    # 3. Business Logic Routing: Apply rules based on the receiving business account.
    # Each handler function represents a modular, sector-specific logic unit.
    if business_account_id == HAVANA_CAFE_ACCOUNT_ID:
        handle_havana_cafe_inquiry(customer_number, message_text)

    elif business_account_id == SCHOOL_CATERING_ACCOUNT_ID:
        handle_catering_inquiry(customer_number, message_text)

    elif business_account_id == INVESTMENT_SERVICES_ACCOUNT_ID:
        # For high-security contexts, immediately route to a human agent.
        route_to_human_agent(customer_number, "Investment Inquiry")
        send_investment_acknowledgement(customer_number)
    # 4. Acknowledge Receipt: Confirm successful processing to WhatsApp.
    return {"status": "success"}, 200
  
  
  
  






