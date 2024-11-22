import React, { useState, useEffect, useRef, useCallback } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRobot } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

const BookCard = ({ book, onAddToCart }) => (
  <div className="flex bg-white rounded-lg shadow-md overflow-hidden mb-4 hover:shadow-lg transition-shadow duration-300">
    <img
      src={
        book.image_url || "https://via.placeholder.com/100x150?text=No+Image"
      }
      alt={book.title}
      className="w-20 h-30 object-cover"
    />
    <div className="p-3 flex-1 flex flex-col justify-between">
      <div>
        <h4 className="text-sm font-semibold mb-1 text-gray-800">
          {book.title}
        </h4>
        <p className="text-xs text-gray-600 mb-1">
          Pages: {book.pages || "N/A"}
        </p>
        <p className="text-xs text-gray-600 mb-1">
          Release Year: {book.release_year || "N/A"}
        </p>
        <p className="text-xs text-gray-600 mb-1">
          Price: ${book.Price || "N/A"}
        </p>
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

const UserForm = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: "",
    address: "",
    cardNumber: "",
    expiryDate: "",
    cvv: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { name, address, cardNumber, expiryDate, cvv } = formData;

    if (!name || !address || !cardNumber || !expiryDate || !cvv) {
      alert("Please fill out all fields");
      return;
    }

    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white rounded-lg shadow-md">
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Shipping Address
        </label>
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Card Number (16 digits)
        </label>
        <input
          type="text"
          name="cardNumber"
          value={formData.cardNumber}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
          maxLength="16"
          pattern="\d{16}"
          title="Card number must be 16 digits"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Expiry Date (MM/YY)
        </label>
        <input
          type="text"
          name="expiryDate"
          value={formData.expiryDate}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
          pattern="\d{2}/\d{2}"
          title="Expiry date must be in MM/YY format"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">CVV</label>
        <input
          type="text"
          name="cvv"
          value={formData.cvv}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
          maxLength="3"
          pattern="\d{3}" // Ensures only 3 digits
          title="CVV must be 3 digits"
        />
      </div>
      <div className="flex justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="bg-gray-300 text-gray-700 px-4 py-2 rounded mr-2"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Submit
        </button>
      </div>
    </form>
  );
};

const Cart = ({
  cartItems = {},
  onRemoveFromCart,
  onPlaceOrder,
  isOrderProcessing,
}) => {
  if (!cartItems || Object.keys(cartItems).length === 0) return null;

  const totalPrice = Object.values(cartItems).reduce(
    (sum, item) =>
      sum + parseFloat(item?.book?.Price || 0) * (item?.quantity || 0),
    0
  );

  return (
    <div className="bg-gray-50 border-b p-2 shadow-sm">
      <div className="max-h-40 overflow-y-auto">
        {Object.entries(cartItems).map(([bookId, item]) => {
          if (!item || !item.book) return null;

          const { book, quantity } = item;

          return (
            <div
              key={bookId}
              className="flex items-center justify-between py-1 px-2 hover:bg-white rounded transition-colors duration-200"
            >
              <div className="flex items-center space-x-2 flex-1">
                <div className="flex-1">
                  <div className="flex items-center">
                    <span className="text-sm font-medium truncate">
                      {book.title}
                    </span>
                    <span className="ml-2 text-xs px-2 py-0.5 bg-gray-200 rounded-full">
                      x{quantity}
                    </span>
                  </div>
                  <span className="text-xs text-gray-600">
                    ${((parseFloat(book.Price) || 0) * quantity).toFixed(2)}
                  </span>
                </div>
              </div>
              <button
                onClick={() => onRemoveFromCart(bookId)}
                className="text-red-500 text-xs hover:text-red-700 ml-2"
              >
                Remove
              </button>
            </div>
          );
        })}
      </div>
      <button
        className={`w-full mt-2 bg-blue-500 text-white text-sm py-2 px-3 rounded hover:bg-blue-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 ${
          isOrderProcessing ? "opacity-50 cursor-not-allowed" : ""
        }`}
        onClick={onPlaceOrder}
        disabled={isOrderProcessing}
      >
        {isOrderProcessing
          ? "Processing..."
          : `Place Order ($${totalPrice.toFixed(2)})`}
      </button>
    </div>
  );
};

const OrderConfirmationCard = ({ orderDetails }) => {
  if (!orderDetails) return null;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-green-100">
      <div className="flex items-center justify-center mb-4">
        <div className="bg-green-100 rounded-full p-2">
          <svg
            className="w-6 h-6 text-green-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
      </div>

      <h3 className="text-lg font-semibold text-center text-gray-800 mb-4">
        Order Confirmed!
      </h3>

      <div className="space-y-3">
        <div className="flex justify-between items-center py-2 border-b border-gray-100">
          <span className="text-sm text-gray-600">Order ID</span>
          <span className="text-sm font-medium text-gray-800">
            {orderDetails.order_id}
          </span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-gray-100">
          <span className="text-sm text-gray-600">Total Cost</span>
          <span className="text-sm font-medium text-green-600">
            ${orderDetails.total_cost}
          </span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-gray-100">
          <span className="text-sm text-gray-600">Order Date</span>
          <span className="text-sm font-medium text-gray-800">
            {new Date(
              orderDetails.order_placed_on.replace(" ", "T")
            ).toLocaleDateString()}
          </span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-gray-100">
          <span className="text-sm text-gray-600">Expected Delivery</span>
          <span className="text-sm font-medium text-gray-800">
            {new Date(orderDetails.expected_delivery).toLocaleDateString()}
          </span>
        </div>

        <div className="flex justify-between items-center py-2 border-b border-gray-100">
          <span className="text-sm text-gray-600">Status</span>
          <span className="text-sm font-medium text-green-600">
            {orderDetails.status === "success"
              ? "Successful"
              : orderDetails.status}
          </span>
        </div>
      </div>

      <div className="mt-4 pt-3 text-center">
        <p className="text-sm text-gray-600">{orderDetails.message}</p>
      </div>
    </div>
  );
};

const OrderListCard = ({ orders, onViewDetails }) => {
  if (!orders || orders.length === 0) return null;

  return (
    <div className="w-full space-y-3">
      {orders.map((order, index) => (
        <div 
          key={index} 
          className="bg-white rounded-lg shadow-sm p-4 border border-gray-100 hover:shadow-md transition-shadow duration-200"
        >
          <div className="flex flex-col space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-900">Order ID</span>
              <span className="text-sm text-gray-600 font-mono">{order.order_id.slice(-8)}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-900">Ordered On</span>
              <span className="text-sm text-gray-600">
                {new Date(order.purchase_date.replace(' ', 'T')).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric'
                })}
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-900">Delivery By</span>
              <span className="text-sm text-gray-600">
                {new Date(order.expected_delivery).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric'
                })}
              </span>
            </div>

            <button 
              className="mt-2 w-full text-sm bg-blue-50 text-blue-600 py-2 px-4 rounded-md hover:bg-blue-100 transition-colors duration-200 flex items-center justify-center space-x-1"
              onClick={() => onViewDetails(order.order_id)}
            >
              <span>View Details</span>
              <svg 
                className="w-4 h-4" 
                fill="none" 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth="2" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

const OrderInfoCard = ({ orderInfo }) => {
  if (!orderInfo) return null;

  const formatDate = (dateString) => {
    return new Date(dateString.replace(' ', 'T')).toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 w-full">
      <div className="border-l-4 border-blue-500 pl-4 mb-4">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-semibold text-gray-800">Order Summary</h3>
          <span className={`px-3 py-1 rounded-full text-sm ${
            orderInfo.status === 'Delivered' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
          }`}>
            {orderInfo.status}
          </span>
        </div>
        <p className="text-sm text-gray-600">Order #{orderInfo.order_id.slice(-8)}</p>
      </div>

      <div className="space-y-4">
        {/* Dates Section */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600">Ordered On</p>
            <p className="text-sm font-medium">{formatDate(orderInfo.order_placed_on)}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Expected Delivery</p>
            <p className="text-sm font-medium">{formatDate(orderInfo.expected_delivery)}</p>
          </div>
        </div>

        {/* Items Section */}
        <div className="border-t border-b border-gray-100 py-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Items</p>
          {orderInfo.items.map((item, index) => (
            <div key={index} className="flex justify-between items-center py-2">
              <div className="flex-1">
                <p className="text-sm font-medium">{item.title}</p>
                <p className="text-xs text-gray-600">Qty: {item.quantity}</p>
              </div>
              <p className="text-sm font-medium">${item.subtotal.toFixed(2)}</p>
            </div>
          ))}
        </div>

        {/* Total and Address Section */}
        <div className="space-y-3">
          <div className="flex justify-between items-center font-medium">
            <span className="text-gray-700">Total Amount</span>
            <span className="text-lg text-blue-600">${orderInfo.total_cost}</span>
          </div>

          {orderInfo.shipping_address && (
            <div className="pt-3 border-t border-gray-100">
              <p className="text-sm font-medium text-gray-700 mb-1">Delivery Address</p>
              <p className="text-sm text-gray-600">
                {orderInfo.shipping_address.street},<br />
                {orderInfo.shipping_address.city}, {orderInfo.shipping_address.state} {orderInfo.shipping_address.zip_code}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [cart, setCart] = useState({});
  const [isOrderProcessing, setIsOrderProcessing] = useState(false);
  const [isOrderComplete, setIsOrderComplete] = useState(false);
  const [showUserForm, setShowUserForm] = useState(false);
  const [tempMessage, setTempMessage] = useState(null);
  const messagesEndRef = useRef(null);


  const handleViewOrderDetails = async (orderId) => {
    setIsLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/chatbot/chat",
        { 
          message: `view order details ${orderId}`,
          metadata: {
            type: "order_info", // Changed from order_details to order_info
            order_id: orderId
          }
        }
      );
      const data = response.data;
      
      if (data.type === "order_info") { // Changed this check to order_info
        addMessage("Here are the details for your order:", "bot");
        addMessage(data.response, "bot", "order_info"); // Changed from order_confirmation to order_info
      } else {
        addMessage("Sorry, I couldn't find the details for this order.", "bot");
      }
    } catch (error) {
      console.error("Error fetching order details:", error);
      addMessage(
        "I'm sorry, I couldn't fetch the order details at this moment. Please try again later.",
        "bot"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (message) => {
    setIsLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/chatbot/chat",
        { message }
      );
      const data = response.data;

      if (message.toLowerCase() === "quit") {
        return;
      }

      if (data.type === "greeting" || data.type === "clarification") {
        addMessage(data.response, "bot");
      } else if (data.type === "question" || data.type === "order_question") {
        addMessage(data.response, "bot");
      } else if (data.type === "recommendation") {
        addMessage(
          "Based on our conversation, here are some book recommendations for you:",
          "bot"
        );
        addMessage(data.response, "bot", "recommendations");
        addMessage(
          "Would you like more recommendations or have any other questions?",
          "bot"
        );
      } else if (data.type === "order_confirmation") {
        addMessage(data.response, "bot", "order_confirmation");
        setIsOrderProcessing(false);
        setCart({});
        setIsOrderComplete(true);
      }else if(data.type === "order_list"){
        if (data.response && data.response.length > 0) {
          addMessage("Here are your recent orders:", "bot");
          addMessage(data.response, "bot", "order_list");
          addMessage("You can view the details of any order or ask me something else.", "bot");
        } else {
          addMessage("You don't have any orders yet. Would you like to browse some books?", "bot");
        }
      }
      else if(data.type === "order_info") {
        addMessage("Here's the current status of your order:", "bot");
        addMessage(data.response, "bot", "order_info");
      }
    } catch (error) {
      console.error("Error communicating with chatbot:", error);
      addMessage(
        "I'm sorry, I'm having trouble processing your request. Please try again later.",
        "bot"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const addMessage = useCallback((content, sender, type = "text") => {
    setMessages((prev) => [...prev, { content, sender, type }]);
  }, []);

  const handleRestart = async () => {
    setIsOrderComplete(false);
    clearConversation();
  };

  const clearConversation = async () => {
    sendMessage("quit");
    setMessages([]);
    setCart({});
    setIsOrderProcessing(false);
    setIsOrderComplete(false);
    setShowUserForm(false);
    setTempMessage(null);
    addMessage("Welcome! I'm BookWorm, your virtual assistant. I’m here to help you browse and find the perfect book for your collection. Ready to start exploring?", "bot");
  };

  const handleClose = async () => {
    sendMessage("quit");
    setIsOpen(false);
    setMessages([]);
    setCart([]);
    setIsOrderProcessing(false);
  };

  const handleAddToCart = (book) => {
    setCart((prevCart) => {
      const bookId = book.title;
      const existingItem = prevCart[bookId];

      return {
        ...prevCart,
        [bookId]: {
          book,
          quantity: existingItem ? existingItem.quantity + 1 : 1,
        },
      };
    });

    setTempMessage(`"${book.title}" added to cart`);
    setTimeout(() => setTempMessage(null), 3000);
  };

  const handleRemoveFromCart = (bookId) => {
    setCart((prevCart) => {
      const newCart = { ...prevCart };
      delete newCart[bookId];
      return newCart;
    });
  };

  const handlePlaceOrder = () => {
    setShowUserForm(true);
  };

  const handleOrderConfirmation = (orderDetails) => {
    addMessage(orderDetails, "bot", "order_confirmation");
  };

  const handleFormSubmit = async (formData) => {
    setIsOrderProcessing(true);
    setShowUserForm(false);
  
    try {
      const cartArray = Object.values(cart).map((item) => ({
        ...item.book,
        quantity: item.quantity,
      }));
  
      const userDetails = {
        name: formData.name,
        address: formData.address,
        cardNumber: formData.cardNumber,
        expiryDate: formData.expiryDate,
        cvv: formData.cvv,
      };
  
      const payload = {
        order_data: cartArray,
        user_details: userDetails,
      };
  
      const response = await axios.post(
        "http://localhost:8000/api/chatbot/place-order",
        payload
      );
  
      // Handle the response from the backend
      if (response?.data?.response) {
        handleOrderConfirmation(response.data.response); 
        setCart({});
      } else {
        throw new Error("Invalid response format");
      }
    } catch (error) {
      console.error("Error placing order:", error);
      addMessage(
        "I'm sorry, there was an error placing your order. Please try again.",
        "bot"
      );
    } finally {
      setIsOrderProcessing(false);
    }
  };  

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      addMessage(
        "Welcome! I'm BookWorm, your virtual assistant. I’m here to help you browse and find the perfect book for your collection. Ready to start exploring?",
        "bot"
      );
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
    const lowerInput = userInput.toLowerCase();
    setInput("");

    if (lowerInput === "quit") {
      handleClose();
    } else if (lowerInput === "clear") {
      addMessage(userInput, "user");
      await clearConversation();
    } else {
      addMessage(userInput, "user");
      await sendMessage(userInput);
    }
  };

  return (
    <div className="fixed right-4 bottom-4 z-50">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-500 text-white rounded-full p-4 shadow-lg hover:bg-blue-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </button>
      ) : (
        <div className="bg-white rounded-lg shadow-xl flex flex-col w-[28rem] h-[36rem] transition-all duration-300 ease-in-out">
          <div className="bg-blue-500 text-white px-4 py-3 flex justify-between items-center rounded-t-lg">
            <FontAwesomeIcon icon={faRobot} className="h-5 w-5 text-white" />
            <h3 className="text-lg font-semibold">BookWorm</h3>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleClose}
                className="text-white hover:text-gray-200 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`${
                    msg.type === "recommendations" ||
                    msg.type === "order_confirmation"
                      ? "max-w-[75%]"
                      : "max-w-[75%]"
                  } p-3 rounded-lg ${
                    msg.sender === "user"
                      ? "bg-blue-100 text-blue-900"
                      : "bg-gray-100 text-gray-900"
                  } shadow-md`}
                >
                  {msg.type === "recommendations" ? (
                    <div className="w-full space-y-4">
                      {msg.content.map((book, bookIndex) => (
                        <BookCard
                          key={bookIndex}
                          book={book}
                          onAddToCart={handleAddToCart}
                        />
                      ))}
                    </div>
                  ) : msg.type === "order_confirmation" ? (
                    <OrderConfirmationCard orderDetails={msg.content} />
                  ) : msg.type === "order_list" ? (
                    <OrderListCard 
                      orders={msg.content} 
                      onViewDetails={handleViewOrderDetails}
                    />
                  ) : msg.type === "order_info" ? (
                    <OrderInfoCard orderInfo={msg.content} />
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

          {showUserForm ? (
            <UserForm
              onSubmit={handleFormSubmit}
              onCancel={() => setShowUserForm(false)}
            />
          ) : (
            <Cart
              cartItems={cart}
              onRemoveFromCart={handleRemoveFromCart}
              onPlaceOrder={handlePlaceOrder}
              isOrderProcessing={isOrderProcessing}
            />
          )}

          <form onSubmit={handleSubmit} className="border-t p-4 flex">
            {isOrderComplete ? (
              <button
                onClick={handleRestart}
                className="w-full bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg font-medium text-sm transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 flex items-center justify-center space-x-2"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                <span>Start New Chat</span>
              </button>
            ) : (
              <>
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
                  className={`bg-blue-500 text-white px-4 py-2 rounded-r-lg 
          ${isLoading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"} 
          transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50`}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <svg
                      className="animate-spin h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                  ) : (
                    "Send"
                  )}
                </button>
              </>
            )}
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
