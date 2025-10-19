# app/utils/rag_faq.py
# Placeholder for future RAG + FAQ handling
# You can integrate FAISS or Pinecone here
def get_faq_response(user_text):
    # Example: simple dictionary lookup
    faq_dict = {
        "hours": "We are open from 9 AM to 6 PM, Monday to Saturday.",
        "timing": "Our office hours are 9 AM to 6 PM.",
        "booking": "You can easily book online using our web portal or call our support line.",
        "location": "We are located in Lahore, near Model Town main road.",
        "services": "We offer AI-powered customer support, automation, and voice agent solutions.",
        "contact": "You can contact us via email at support@aivoiceagent.com.",
        "address": "Our main office is near Model Town, Lahore, Pakistan.",
        "price": "Pricing depends on the package. Please visit our pricing page for more details.",
        "help": "You can get assistance anytime by calling our helpline or visiting the support section.",
        "about": "We are an AI startup focused on building intelligent voice agents for customer support.",
        "support": "Our support team is available 24/7 through chat and email.",
        "subscription": "You can start with a free trial, and upgrade anytime to a premium plan.",
        "refund": "Refunds are processed within 5-7 business days of approval.",
        "policy": "You can read our privacy policy and terms of service on our official website.",
        "demo": "We offer free demos of our AI Voice Agent. Book a slot through our website.",
    }
    for k, v in faq_dict.items():
        if k in user_text.lower():
            return v
    return None
