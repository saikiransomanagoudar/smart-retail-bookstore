import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Footer from "./components/Footer";
import ViewBookDetails from "./pages/ViewBookDetails";
import Cart from "./pages/Cart";
import Profile from "./pages/Profile";
import Favourite from "./pages/Favourite";
import OrderHistory from "./pages/OrderHistory";
import Settings from "./pages/Settings";
import AllOrders from "./components/AdminPages/AllOrders";
import AddBook from "./components/AdminPages/AddBook";
import UpdateBooks from "./components/AdminPages/UpdateBooks";
import { useUser } from "@clerk/clerk-react";
import Authors from "./pages/Authors";
import Dashboard from "./pages/Dashboard";
import Hero from "./components/Home/Hero";
import UserPreferences from "./components/Modals/UserPreferences";
import { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
  const { user, isSignedIn } = useUser();
  const [isFirstLogin, setIsFirstLogin] = useState(false);
  const [showPreferencesModal, setShowPreferencesModal] = useState(false);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    if (isSignedIn && user) {
      const firstLogin = localStorage.getItem(`firstLogin_${user.id}`);
      setUserId(user.id);

      if (!firstLogin) {
        setIsFirstLogin(true);
        setShowPreferencesModal(true);
        localStorage.setItem(`firstLogin_${user.id}`, 'true');
      }
    }
  }, [isSignedIn, user]);

  const role = user?.publicMetadata?.role || "user";

  const handlePreferencesSubmitted = async (preferences) => {
    try {
      await axios.post("http://localhost:8000/api/recommendations/save-preferences", {
        user_id: userId,
        ...preferences
      });
      
      setShowPreferencesModal(false);
      setIsFirstLogin(false);
    } catch (error) {
      console.error("Error saving user preferences:", error);
    }
  };

  return (
    <div className="">
      <Navbar />
      <Routes>
        <Route 
          path="/" 
          element={
            !isSignedIn ? (
              <Hero />
            ) : (
              <Navigate to="/dashboard" />
            )
          }
        />

        <Route
          path="/login"
          element={!isSignedIn ? <Login /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/signup"
          element={!isSignedIn ? <Signup /> : <Navigate to="/dashboard" />}
        />

        <Route
          path="/login/sso-callback"
          element={!isSignedIn ? <Login /> : <Navigate to="/" />}
        />
        <Route
          path="/signup/sso-callback"
          element={!isSignedIn ? <Signup /> : <Navigate to="/" />}
        />

        <Route path="/dashboard" element={isSignedIn ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/view-book-details/:id" element={<ViewBookDetails />} />
        <Route path="/Authors" element={<Authors />} />
        <Route
          path="/cart"
          element={isSignedIn ? <Cart /> : <Navigate to="/login" />}
        />
        <Route
          path="/profile"
          element={isSignedIn ? <Profile /> : <Navigate to="/login" />}
        >
          {role !== "admin" ? (
            <Route index element={<Favourite />} />
          ) : (
            <Route index element={<AllOrders />} />
          )}
          {role === "admin" && (
            <Route path="/profile/add-book" element={<AddBook />} />
          )}
          <Route path="/profile/order-history" element={<OrderHistory />} />
          <Route path="/profile/settings" element={<Settings />} />
        </Route>
        {role === "admin" && (
          <Route path="/update-book/:id" element={<UpdateBooks />} />
        )}
      </Routes>
      <Footer />

      {isSignedIn && isFirstLogin && (
        <UserPreferences
          isOpen={showPreferencesModal}
          onClose={() => setShowPreferencesModal(false)}
          onNext={handlePreferencesSubmitted}
        />
      )}
    </div>
  );
};

export default App;
