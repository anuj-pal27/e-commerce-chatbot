import React from 'react';

const ProductCard = ({ product }) => {
  const handleViewProduct = () => {
    // You can implement navigation to product detail page here
    window.open(`/products/${product.id}`, '_blank');
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-4 m-2 max-w-sm">
      <div className="flex flex-col h-full">
        {/* Product Image */}
        <div className="mb-3">
          <img
            src={product.image_url || 'https://via.placeholder.com/300x200?text=Product+Image'}
            alt={product.name}
            className="w-full h-32 object-cover rounded-md"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/300x200?text=Product+Image';
            }}
          />
        </div>

        {/* Product Info */}
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 text-sm mb-1 line-clamp-2">
            {product.name}
          </h3>
          
          <p className="text-xs text-gray-600 mb-2">
            Category: <span className="font-medium">{product.category}</span>
          </p>
          
          <div className="flex items-center justify-between mb-2">
            <span className="text-lg font-bold text-blue-600">
              ${product.price}
            </span>
            <div className="flex items-center">
              <span className="text-yellow-400 mr-1">⭐</span>
              <span className="text-sm text-gray-600">{product.rating}/5</span>
            </div>
          </div>

          <div className="flex items-center justify-between mb-3">
            <span className={`text-xs px-2 py-1 rounded ${
              product.stock > 0 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
            </span>
          </div>

          {/* Description (truncated) */}
          <p className="text-xs text-gray-600 mb-3 line-clamp-2">
            {product.description}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <button
            onClick={handleViewProduct}
            className="flex-1 bg-blue-600 text-white text-xs py-2 px-3 rounded hover:bg-blue-700 transition-colors"
          >
            View Details
          </button>
          <button
            className="flex-1 bg-green-600 text-white text-xs py-2 px-3 rounded hover:bg-green-700 transition-colors"
            disabled={product.stock === 0}
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard; 