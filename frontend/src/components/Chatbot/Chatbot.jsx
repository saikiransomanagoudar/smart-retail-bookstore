import React, { useState, useEffect, useRef, useCallback } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRobot } from "@fortawesome/free-solid-svg-icons";
import { useUser } from "@clerk/clerk-react";
import axios from "axios";

const BookCard = ({ book, onAddToCart }) => (
  <div className="flex bg-white rounded-lg shadow-md overflow-hidden mb-4 hover:shadow-lg transition-shadow duration-300">
    <img
      src={book.image_url || "https://via.placeholder.com/100x150?text=No+Image"}
      alt={book.title || "Book"}
      className="w-20 h-30 object-cover"
    />
    <div className="p-3 flex-1 flex flex-col justify-between">
      <div>
        <h4 className="text-sm font-semibold mb-1 text-gray-800">
          {book.title || "Untitled"}
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
        <p className="text-xs text-gray-700">
          {book.ReasonForRecommendation || "No recommendation reason provided."}
        </p>
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
    address: {
      street: "",
      city: "",
      state: "",
      zip_code: "",
    },
    cardNumber: "",
    expiryDate: "",
    cvv: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (["street", "city", "state", "zip_code"].includes(name)) {
      setFormData((prev) => ({
        ...prev,
        address: {
          ...prev.address,
          [name]: value,
        },
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { name, address, cardNumber, expiryDate, cvv } = formData;

    if (
      !name ||
      !address.street ||
      !address.city ||
      !address.state ||
      !address.zip_code ||
      !cardNumber ||
      !expiryDate ||
      !cvv
    ) {
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
          Street
        </label>
        <input
          type="text"
          name="street"
          value={formData.address.street}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">City</label>
        <input
          type="text"
          name="city"
          value={formData.address.city}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">State</label>
        <input
          type="text"
          name="state"
          value={formData.address.state}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Zip Code
        </label>
        <input
          type="text"
          name="zip_code"
          value={formData.address.zip_code}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Card Number
        </label>
        <input
          type="text"
          name="cardNumber"
          value={formData.cardNumber}
          onChange={handleChange}
          className="mt-1 p-2 border border-gray-300 rounded w-full"
          required
          maxLength="16"
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
  console.log("Received orderDetails: ", orderDetails);
  if (!orderDetails || typeof orderDetails !== "object") {
    console.error("Invalid orderDetails:", orderDetails);
    return (
      <div className="text-red-600 text-center">
        <p>Unable to load order details. Please try again later.</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    try {
      const isoDateString = dateString.replace(' ', 'T');
      return new Date(isoDateString).toLocaleDateString();
    } catch {
      return "Invalid date";
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-green-100">
      <div className="flex items-center justify-center mb-4">
        <div className="bg-green-100 rounded-full p-2">
          <svg
            className="w-6 h-6 text-green-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
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
        {orderDetails.order_id && (
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-sm text-gray-600">Order ID</span>
            <span className="text-sm font-medium text-gray-800">
              {orderDetails.order_id}
            </span>
          </div>
        )}

        {orderDetails.total_cost && (
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-sm text-gray-600">Total Cost</span>
            <span className="text-sm font-medium text-green-600">
              ${parseFloat(orderDetails.total_cost).toFixed(2)}
            </span>
          </div>
        )}

        {orderDetails.order_placed_on && (
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-sm text-gray-600">Order Date</span>
            <span className="text-sm font-medium text-gray-800">
              {formatDate(orderDetails.order_placed_on)}
            </span>
          </div>
        )}

        {orderDetails.expected_delivery && (
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-sm text-gray-600">Expected Delivery</span>
            <span className="text-sm font-medium text-gray-800">
              {formatDate(orderDetails.expected_delivery)}
            </span>
          </div>
        )}

        {orderDetails.status && (
          <div className="flex justify-between items-center py-2 border-b border-gray-100">
            <span className="text-sm text-gray-600">Status</span>
            <span
              className={`text-sm font-medium ${
                orderDetails.status === "success"
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {orderDetails.status === "success"
                ? "Successful"
                : orderDetails.status}
            </span>
          </div>
        )}
      </div>

      <div className="mt-4 pt-3 text-center">
        {typeof orderDetails.message === "string" && orderDetails.message ? (
          <p className="text-sm text-gray-600">{orderDetails.message}</p>
        ) : (
          <p className="text-sm text-red-600">
            Something went wrong. Please try again.
          </p>
        )}
      </div>
    </div>
  );
};

const Chatbot = () => {
  const { user } = useUser();
  const userId = user?.id;
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

      if (data.type === "recommendation") {
        const recommendations = data.response.map((book) => ({
          title: book.title || "Untitled",
          pages: book.pages || "N/A",
          release_year: book.release_year || "N/A",
          Price: book.Price || "N/A",
          ReasonForRecommendation:
            book.ReasonForRecommendation || "No recommendation reason provided.",
          image_url:
            book.image_url ||
            "https://via.placeholder.com/100x150?text=No+Image",
        }));

        addMessage(
          "Based on our conversation, here are some book recommendations for you:",
          "bot"
        );
        addMessage(recommendations, "bot", "recommendations");
        addMessage(
          "Would you like more recommendations or have any other questions?",
          "bot"
        );
      } else if (data.type === "order_confirmation") {
        addMessage(data.response, "bot", "order_confirmation");
        setIsOrderProcessing(false);
        setCart({});
        setIsOrderComplete(true);
      } else {
        addMessage(data.response, "bot");
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
    if (type === "order_confirmation" || type === "recommendations") {
      // Pass content as is for these types
      setMessages((prev) => [...prev, { content, sender, type }]);
    } else if (typeof content === 'string') {
      // Content is a string
      setMessages((prev) => [...prev, { content, sender, type }]);
    } else if (content && typeof content === 'object' && content.message) {
      // Content is an object with a message property
      setMessages((prev) => [...prev, { content: content.message, sender, type }]);
    } else {
      // Other cases
      setMessages((prev) => [...prev, { content: JSON.stringify(content), sender, type }]);
    }
  }, []);

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

  const handleOrderConfirmation = (orderResponse) => {
    console.log("Order response received in handleOrderConfirmation:", orderResponse);
  
    if (
      orderResponse &&
      orderResponse.type === "order_confirmation" &&
      orderResponse.response
    ) {
      const orderDetails = orderResponse.response;
      addMessage(orderDetails, "bot", "order_confirmation");
    } else {
      console.error("Invalid order response:", orderResponse);
      addMessage("An error occurred while placing the order.", "bot", "error");
    }
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
        user_id: userId,
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

      if (response?.data) {
        handleOrderConfirmation(response.data);
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

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!input.trim() || isLoading) return;

    const userInput = input.trim();
    setInput("");

    if (userInput.toLowerCase() === "quit") {
      handleClose();
    } else if (userInput.toLowerCase() === "clear") {
      addMessage(userInput, "user");
      clearConversation();
    } else {
      addMessage(userInput, "user");
      sendMessage(userInput);
    }
  };

  const handleClose = () => {
    setIsOpen(false);
    setMessages([]);
    setCart({});
    setIsOrderProcessing(false);
  };

  const clearConversation = () => {
    setMessages([]);
    setCart({});
    setIsOrderProcessing(false);
    setIsOrderComplete(false);
    setShowUserForm(false);
    setTempMessage(null);
    addMessage(
      "Welcome! I'm BookWorm, your virtual assistant. I’m here to help you browse and find the perfect book for your collection. Ready to start exploring?",
      "bot"
    );
  };

  return (
    <div className="fixed right-4 bottom-4 z-50">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-blue-500 text-white rounded-full p-4 shadow-lg hover:bg-blue-600 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          <FontAwesomeIcon icon={faRobot} className="h-6 w-6" />
        </button>
      ) : (
        <div className="bg-white rounded-lg shadow-xl flex flex-col w-[28rem] h-[36rem] transition-all duration-300 ease-in-out">
          <div className="bg-blue-500 text-white px-4 py-3 flex justify-between items-center rounded-t-lg">
            <FontAwesomeIcon icon={faRobot} className="h-5 w-5 text-white" />
            <h3 className="text-lg font-semibold">BookWorm</h3>
            <button
              onClick={handleClose}
              className="text-white hover:text-gray-200 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
            >
              X
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {Array.isArray(messages) && messages.length > 0 ? (
              messages.map((msg, index) => (
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
                        ? "max-w-full"
                        : "max-w-[75%]"
                    } p-3 rounded-lg ${
                      msg.sender === "user"
                        ? "bg-blue-100 text-blue-900"
                        : "bg-gray-100 text-gray-900"
                    } shadow-md`}
                  >
                    {msg.type === "recommendations" &&
                    Array.isArray(msg.content) ? (
                      <div className="w-full space-y-4">
                        {msg.content.length > 0 ? (
                          msg.content.map((book, bookIndex) => (
                            <BookCard
                              key={`${book.title}-${bookIndex}`}
                              book={book}
                              onAddToCart={handleAddToCart}
                            />
                          ))
                        ) : (
                          <p className="text-sm text-gray-500">
                            No recommendations available.
                          </p>
                        )}
                      </div>
                    ) : msg.type === "order_confirmation" ? (
                      <OrderConfirmationCard orderDetails={msg.content} />
                    ) : (
                      <p className="text-sm">{msg.content}</p>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <p>No messages to display</p>
            )}
            {showUserForm ? (
              <div className="overflow-y-auto max-h-[20rem] p-4">
                <UserForm
                  onSubmit={handleFormSubmit}
                  onCancel={() => setShowUserForm(false)}
                />
              </div>
            ) : (
              <Cart
                cartItems={cart}
                onRemoveFromCart={handleRemoveFromCart}
                onPlaceOrder={handlePlaceOrder}
                isOrderProcessing={isOrderProcessing}
              />
            )}
          </div>
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
              className={`bg-blue-500 text-white px-4 py-2 rounded-r-lg ${
                isLoading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"
              } transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50`}
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
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
