import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Footer from "./components/Footer";
import AllBooks from "./pages/AllBooks";
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

const App = () => {
  const { user, isSignedIn } = useUser();

  const role = user?.publicMetadata?.role || "user";

  return (
    <div className="">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/all-books" element={<AllBooks />} />
        <Route path="/view-book-details/:id" element={<ViewBookDetails />} />
        <Route path="/login" element={!isSignedIn ? <Login /> : <Navigate to="/" />} />
        <Route path="/signup" element={!isSignedIn ? <Signup /> : <Navigate to="/" />} />
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
    </div>
  );
};

export default App;
