import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { BrowserRouter as Router } from "react-router-dom";
import { ClerkProvider } from "@clerk/clerk-react";

const PUBLISHABLE_KEY = "pk_test_ZmFtb3VzLXNhbG1vbi00LmNsZXJrLmFjY291bnRzLmRldiQ";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <Router>
        <App />
      </Router>
    </ClerkProvider>
  </React.StrictMode>
);