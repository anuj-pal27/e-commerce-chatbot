import React from 'react';
import ProductCard from './ProductCard';

const ChatMessage = ({ message, isUser }) => {
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatMessageContent = (content) => {
    // Convert markdown-style formatting to JSX
    const lines = content.split('\n');
    return lines.map((line, index) => {
      if (line.startsWith('🔸 **') && line.endsWith('**')) {
        // Product name formatting
        const productName = line.replace('🔸 **', '').replace('**', '');
        return (
          <div key={index} className="font-semibold text-blue-700 mt-2">
            🔸 {productName}
          </div>
        );
      } else if (line.startsWith('   ')) {
        // Product details formatting
        return (
          <div key={index} className="ml-4 text-sm text-gray-600">
            {line.trim()}
          </div>
        );
      } else if (line.trim() === '') {
        return <br key={index} />;
      } else if (line.includes('**') && !line.startsWith('🔸')) {
        // Bold text formatting
        const parts = line.split('**');
        return (
          <div key={index} className="mb-1">
            {parts.map((part, partIndex) => 
              partIndex % 2 === 1 ? 
                <strong key={partIndex}>{part}</strong> : 
                part
            )}
          </div>
        );
      } else {
        return (
          <div key={index} className="mb-1">
            {line}
          </div>
        );
      }
    });
  };

  return (
    <div className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs lg:max-w-md ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Avatar */}
        <div className={`flex items-end ${isUser ? 'justify-end' : 'justify-start'}`}>
          {!isUser && (
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center mr-2 mb-1">
              <span className="text-white text-sm font-semibold">🤖</span>
            </div>
          )}
          
          {/* Message bubble */}
          <div
            className={`px-4 py-2 rounded-lg ${
              isUser
                ? 'bg-blue-500 text-white rounded-br-none'
                : 'bg-gray-100 text-gray-800 rounded-bl-none'
            }`}
          >
            <div className="whitespace-pre-wrap break-words">
              {formatMessageContent(message.content)}
            </div>
            
            {/* Timestamp */}
            <div
              className={`text-xs mt-1 ${
                isUser ? 'text-blue-100' : 'text-gray-500'
              }`}
            >
              {formatTimestamp(message.timestamp)}
            </div>
          </div>

          {isUser && (
            <div className="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center ml-2 mb-1">
              <span className="text-white text-sm font-semibold">👤</span>
            </div>
          )}
        </div>

        {/* Related Products */}
        {!isUser && message.related_products && message.related_products.length > 0 && (
          <div className="mt-3 ml-10">
            <div className="text-sm font-medium text-gray-700 mb-2">
              Recommended Products:
            </div>
            <div className="flex flex-wrap">
              {message.related_products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage; 