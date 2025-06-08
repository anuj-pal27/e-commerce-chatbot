import re
from django.db.models import Q
from .models import Product
import random

class ChatbotService:
    def __init__(self):
        self.greetings = [
            "Hello! I'm here to help you find the perfect products. What are you looking for today?",
            "Hi there! Welcome to our store. How can I assist you with your shopping?",
            "Greetings! I'm your personal shopping assistant. What can I help you find?",
        ]
        
        self.farewells = [
            "Thank you for shopping with us! Have a great day!",
            "Goodbye! Feel free to come back if you need any more help.",
            "Thanks for visiting! Hope you found what you were looking for.",
        ]
        
        # Category mappings for broader searches
        self.category_mappings = {
            'electronics': ['laptops', 'mobile-accessories'],
            'technology': ['laptops', 'mobile-accessories'],
            'tech': ['laptops', 'mobile-accessories'],
            'computers': ['laptops'],
            'mobile': ['mobile-accessories'],
            'phones': ['mobile-accessories'],
            'clothing': ['mens-shirts', 'mens-shoes'],
            'fashion': ['mens-shirts', 'mens-shoes', 'mens-watches'],
            'mens': ['mens-shirts', 'mens-shoes', 'mens-watches'],
            'shoes': ['mens-shoes'],
            'shirts': ['mens-shirts'],
            'watches': ['mens-watches'],
            'accessories': ['mobile-accessories', 'mens-watches'],
            'home': ['furniture', 'home-decoration', 'kitchen-accessories'],
            'kitchen': ['kitchen-accessories'],
            'beauty': ['beauty', 'fragrances'],
            'cosmetics': ['beauty', 'fragrances'],
        }

    def generate_response(self, message, user=None):
        """
        Generate a response based on user message
        """
        message_lower = message.lower().strip()
        
        # Handle greetings
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.greetings), []
        
        # Handle farewells
        if any(farewell in message_lower for farewell in ['bye', 'goodbye', 'thanks', 'thank you']):
            return random.choice(self.farewells), []
        
        # Handle help requests
        if any(help_word in message_lower for help_word in ['help', 'assist', 'support']):
            return self._get_help_response(), []
        
        # Handle product searches and category browsing (combined for better matching)
        return self._handle_comprehensive_search(message)

    def _handle_comprehensive_search(self, message):
        """
        Handle both product searches and category browsing in one method
        """
        message_lower = message.lower().strip()
        
        # First, try to match category mappings
        matched_categories = []
        for broad_category, specific_categories in self.category_mappings.items():
            if broad_category in message_lower:
                matched_categories.extend(specific_categories)
        
        # Also check for direct category matches
        all_categories = Product.objects.values_list('category', flat=True).distinct()
        for category in all_categories:
            if category.lower() in message_lower or category.replace('-', ' ').lower() in message_lower:
                matched_categories.append(category)
        
        # Remove duplicates
        matched_categories = list(set(matched_categories))
        
        # If we found category matches, get products from those categories
        if matched_categories:
            return self._get_products_by_categories(matched_categories, message_lower)
        
        # If no category matches, try general product search
        if any(search_word in message_lower for search_word in ['find', 'search', 'looking for', 'need', 'want', 'show me']):
            return self._handle_product_search(message)
        
        # Handle price-related queries
        if any(price_word in message_lower for price_word in ['price', 'cost', 'cheap', 'expensive', 'budget']):
            return self._handle_price_query(message)
        
        # Try a general search as fallback
        search_terms = self._extract_search_terms(message)
        if search_terms:
            products = self._search_products(search_terms)
            if products:
                return self._format_product_response(products, f"I found products matching your search:")
        
        # Default response for unrecognized input
        return self._get_default_response(message), []

    def _get_products_by_categories(self, categories, original_message):
        """
        Get products from specific categories
        """
        products = Product.objects.filter(category__in=categories)[:8]
        
        if products:
            category_name = self._get_friendly_category_name(categories, original_message)
            return self._format_product_response(products, f"Here are some great {category_name} products:")
        else:
            return f"Sorry, I couldn't find any products in those categories at the moment.", []

    def _get_friendly_category_name(self, categories, original_message):
        """
        Get a user-friendly category name based on original message
        """
        message_lower = original_message.lower()
        
        # Check if user used a broad category term
        for broad_category in self.category_mappings.keys():
            if broad_category in message_lower:
                return broad_category
        
        # Otherwise, use the most common category
        if len(categories) == 1:
            return categories[0].replace('-', ' ')
        else:
            return "matching"

    def _format_product_response(self, products, intro_text):
        """
        Format product list into a response
        """
        response = f"{intro_text}\n\n"
        
        for product in products:
            response += f"🔸 **{product.name}**\n"
            response += f"   Category: {product.category.replace('-', ' ').title()}\n"
            response += f"   Price: ${product.price}\n"
            response += f"   Rating: {product.rating}/5.0\n"
            if product.stock > 0:
                response += f"   Stock: {product.stock} available\n"
            else:
                response += f"   Status: Out of stock\n"
            response += "\n"
        
        return response, list(products)

    def _handle_product_search(self, message):
        """
        Handle product search queries
        """
        # Extract search terms from message
        search_terms = self._extract_search_terms(message)
        
        if not search_terms:
            return "I'd be happy to help you find products! Could you tell me what specific item you're looking for?", []
        
        # Search for products
        products = self._search_products(search_terms)
        
        if products:
            return self._format_product_response(products[:6], f"I found {len(products)} product(s) matching your search:")
        else:
            return f"I couldn't find any products matching '{' '.join(search_terms)}'. Try searching for electronics, clothing, beauty products, or furniture.", []

    def _handle_price_query(self, message):
        """
        Handle price-related queries
        """
        message_lower = message.lower()
        
        if 'cheap' in message_lower or 'budget' in message_lower:
            products = Product.objects.filter(price__lt=100).order_by('price')[:6]
            response = "Here are some budget-friendly options under $100:\n\n"
        elif 'expensive' in message_lower or 'premium' in message_lower:
            products = Product.objects.filter(price__gt=500).order_by('-price')[:6]
            response = "Here are some premium products:\n\n"
        else:
            # Extract price range if mentioned
            prices = re.findall(r'\$?(\d+(?:\.\d{2})?)', message)
            if len(prices) >= 2:
                min_price, max_price = float(prices[0]), float(prices[1])
                products = Product.objects.filter(price__gte=min_price, price__lte=max_price)[:6]
                response = f"Products in the ${min_price}-${max_price} range:\n\n"
            else:
                return "Could you specify a price range? For example, 'products under $50' or 'between $100 and $200'", []
        
        return self._format_product_response(products, response.strip())

    def _extract_search_terms(self, message):
        """
        Extract meaningful search terms from user message
        """
        # Remove common words and extract meaningful terms
        stop_words = {'i', 'am', 'looking', 'for', 'find', 'search', 'show', 'me', 'can', 'you', 'the', 'a', 'an', 'and', 'or', 'but', 'want', 'need'}
        words = re.findall(r'\b\w+\b', message.lower())
        search_terms = [word for word in words if word not in stop_words and len(word) > 2]
        return search_terms

    def _search_products(self, search_terms):
        """
        Search products based on terms
        """
        query = Q()
        for term in search_terms:
            query |= Q(name__icontains=term) | Q(description__icontains=term) | Q(category__icontains=term)
        
        return Product.objects.filter(query).distinct()

    def _get_help_response(self):
        """
        Generate help response
        """
        return """I'm here to help you find products! Here's what I can do:

🔍 **Search Products**: Just tell me what you're looking for
   Example: "I need a laptop" or "show me books"

📱 **Browse Categories**: Ask about these categories:
   - **Electronics** (laptops, mobile accessories)
   - **Fashion** (shirts, shoes, watches)
   - **Beauty** (cosmetics, fragrances)
   - **Home** (furniture, kitchen accessories, decoration)
   - **Groceries**

💰 **Price Queries**: Ask about pricing
   Example: "cheap electronics" or "products under $50"

⭐ **Product Details**: I can show you ratings, stock, and descriptions

Just type what you're looking for and I'll help you find it!"""

    def _get_default_response(self, message):
        """
        Default response for unrecognized input
        """
        responses = [
            "I'm not sure I understand. Could you tell me what product you're looking for?",
            "Let me help you find what you need! What are you shopping for today?",
            "I'd be happy to help you find products. What can I assist you with?",
        ]
        return random.choice(responses)