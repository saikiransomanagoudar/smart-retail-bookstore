import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ViewBookDetails from "./pages/ViewBookDetails";
import Cart from "./pages/Cart";
import Profile from "./pages/Profile";
import Favourite from "./pages/Favourite";
import OrderHistory from "./pages/OrderHistory";
import Settings from "./pages/Settings";
import { useUser } from "@clerk/clerk-react";
import Authors from "./pages/Authors";
import Dashboard from "./pages/Dashboard";
import Hero from "./components/Home/Home";
import UserPreferences from "./components/Modals/UserPreferences";
// Import the store

const App = () => {
  const { user, isSignedIn } = useUser();
  const role = user?.publicMetadata?.role || "user";

  return (
    <div className=''>
      <Navbar />
      <Routes>
        <Route
          path='/'
          element={!isSignedIn ? <Hero /> : <Navigate to='/dashboard' />}
        />

        <Route
          path='/login'
          element={!isSignedIn ? <Login /> : <Navigate to='/dashboard' />}
        />
        <Route path='/signup' element={<Signup />} />

        <Route path='/preferences' element={<UserPreferences />} />

        <Route
          path='/login/sso-callback'
          element={!isSignedIn ? <Login /> : <Navigate to='/' />}
        />
        <Route
          path='/signup/sso-callback'
          element={!isSignedIn ? <Signup /> : <Navigate to='/' />}
        />

        <Route
          path='/dashboard'
          element={isSignedIn ? <Dashboard /> : <Navigate to='/login' />}
        />
        <Route path='/view-book-details/:id?' element={<ViewBookDetails />} />
        <Route path='/authors' element={<Authors />} />
        <Route
          path='/cart'
          element={isSignedIn ? <Cart /> : <Navigate to='/login' />}
        />

        {/* Profile Routes */}
        <Route
          path='/profile'
          element={isSignedIn ? <Profile /> : <Navigate to='/login' />}
        >
          {role !== "admin" && <Route index element={<Favourite />} />}
          <Route path='order-history' element={<OrderHistory />} />
          <Route path='settings' element={<Settings />} />
        </Route>
      </Routes>
    </div>
  );
};

export default App;
