import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';

const BookCard = ({ book, onAddToCart }) => (
  <div className="flex bg-white rounded-lg shadow-md overflow-hidden mb-4 hover:shadow-lg transition-shadow duration-300">
    <img 
      src={book.image_url || 'https://via.placeholder.com/100x150?text=No+Image'} 
      alt={book.title} 
      className="w-20 h-30 object-cover"
    />
    <div className="p-3 flex-1 flex flex-col justify-between">
      <div>
        <h4 className="text-sm font-semibold mb-1 text-gray-800">{book.title}</h4>
        <p className="text-xs text-gray-600 mb-1">Pages: {book.pages || 'N/A'}</p>
        <p className="text-xs text-gray-600 mb-1">Release Year: {book.release_year || 'N/A'}</p>
        <p className="text-xs text-gray-600 mb-1">Price: ${book.Price || 'N/A'}</p>
        <p className="text-xs text-gray-700">{book.ReasonForRecommendation}</p>
      </div>
      <button 
        className="mt-2 bg-green-500 text-white text-xs py-1 px-2 rounded hover:bg-green-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
        onClick={() => onAddToCart(book)}
      >
        Add to Cart
      </button>
    </div>
  </div>
);

const Cart = ({ books, onRemoveFromCart, onPlaceOrder, isOrderProcessing }) => (
  <div className="bg-white border-t p-4">
    <h3 className="text-lg font-semibold mb-2">Cart</h3>
    {books.length === 0 ? (
      <p className="text-sm text-gray-500">Your cart is empty</p>
    ) : (
      <>
        {books.map((book, index) => (
          <div key={index} className="flex justify-between items-center mb-2">
            <p className="text-sm">{book.title}</p>
            <button 
              onClick={() => onRemoveFromCart(index)}
              className="text-red-500 text-xs hover:text-red-700"
            >
              Remove
            </button>
          </div>
        ))}
        <button 
          className={`mt-2 bg-blue-500 text-white text-sm py-1 px-3 rounded hover:bg-blue-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 ${isOrderProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
          onClick={onPlaceOrder}
          disabled={isOrderProcessing}
        >
          {isOrderProcessing ? 'Processing...' : 'Place Order'}
        </button>
      </>
    )}
  </div>
);

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [cart, setCart] = useState([]);
  const [isOrderProcessing, setIsOrderProcessing] = useState(false);
  const [tempMessage, setTempMessage] = useState(null);
  const messagesEndRef = useRef(null);

  const addMessage = useCallback((content, sender, type = 'text') => {
    setMessages(prev => [...prev, { content, sender, type }]);
  }, []);

  const clearConversation = () => {
    setMessages([]);
    setCart([]);
    setIsOrderProcessing(false);
  };

  const handleClose = () => {
    setIsOpen(false);
    clearConversation();
  };

  const sendMessage = async (message) => {
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/chatbot/chat', { message });
      const data = response.data;

      if (data.type === 'question' || data.type === 'order_question') {
        addMessage(data.response, 'bot');
      } else if (data.type === 'recommendation') {
        addMessage("Based on our conversation, here are some book recommendations for you:", 'bot');
        addMessage(data.response, 'bot', 'recommendations');
        addMessage("Would you like more recommendations or have any other questions?", 'bot');
      } else if (data.type === 'order_confirmation') {
        addMessage(data.response, 'bot');
        setIsOrderProcessing(false);
        setCart([]);
      }
    } catch (error) {
      console.error('Error communicating with chatbot:', error);
      addMessage("I'm sorry, I'm having trouble processing your request. Please try again later.", 'bot');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      sendMessage('Hi');
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userInput = input.trim();
    addMessage(userInput, 'user');
    setInput('');

    if (userInput.toLowerCase() === 'quit') {
      handleClose();
    } else if (userInput.toLowerCase() === 'clear') {
      clearConversation();
    } else {
      await sendMessage(userInput);
    }
  };

  const handleAddToCart = (book) => {
    setCart(prevCart => [...prevCart, book]);
    setTempMessage(`"${book.title}" has been added to your cart.`);
    setTimeout(() => setTempMessage(null), 3000);
  };

  const handleRemoveFromCart = (index) => {
    setCart(prevCart => {
      const newCart = [...prevCart];
      newCart.splice(index, 1);
      return newCart;
    });
  };

  const handlePlaceOrder = async () => {
    setIsOrderProcessing(true);
    try {
      const response = await axios.post('http://localhost:8000/api/chatbot/place-order', { order_data: cart[0] });
      console.log({order_data: cart[0]})
      addMessage(response.data.response, 'bot');
      // The chat will continue through the normal sendMessage flow
    } catch (error) {
      console.error('Error placing order:', error);
      addMessage("I'm sorry, there was an error placing your order. Please try again.", 'bot');
      setIsOrderProcessing(false);
    }
  };

  return (
    <div className="fixed right-4 bottom-4 z-50">
      {!isOpen ? (
        <button 
          onClick={() => setIsOpen(true)} 
          className="bg-blue-500 text-white rounded-full p-4 shadow-lg hover:bg-blue-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </button>
      ) : (
        <div className="bg-white rounded-lg shadow-xl flex flex-col w-[28rem] h-[36rem] transition-all duration-300 ease-in-out">
          <div className="bg-blue-500 text-white px-4 py-3 flex justify-between items-center rounded-t-lg">
            <h3 className="text-lg font-semibold">Book Recommendations</h3>
            <button onClick={handleClose} className="text-white hover:text-gray-200 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`${msg.type === 'recommendations' ? 'w-full' : 'max-w-[75%]'} p-3 rounded-lg ${msg.sender === 'user' ? 'bg-blue-100 text-blue-900' : 'bg-gray-100 text-gray-900'} shadow-md`}>
                  {msg.type === 'recommendations' ? (
                    <div className="w-full space-y-4">
                      {msg.content.map((book, bookIndex) => (
                        <BookCard key={bookIndex} book={book} onAddToCart={handleAddToCart} />
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm">{msg.content}</p>
                  )}
                </div>
              </div>
            ))}
            {tempMessage && (
              <div className="flex justify-center">
                <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm">
                  {tempMessage}
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <Cart 
            books={cart} 
            onRemoveFromCart={handleRemoveFromCart} 
            onPlaceOrder={handlePlaceOrder}
            isOrderProcessing={isOrderProcessing}
          />
          <form onSubmit={handleSubmit} className="border-t p-4 flex">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 border rounded-l-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className={`bg-blue-500 text-white px-4 py-2 rounded-r-lg ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'} transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50`}
              disabled={isLoading}
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : 'Send'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;