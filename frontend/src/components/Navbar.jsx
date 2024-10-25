import { useState } from "react";
import { Link } from "react-router-dom";
import { useUser, SignOutButton } from "@clerk/clerk-react";
import { Search, ShoppingCart, Heart, Menu, X } from "lucide-react"; // Import icons

const Navbar = () => {
  const { isSignedIn, user } = useUser();
  const [isNavOpen, setIsNavOpen] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  const links = [
    { title: "Home", link: "/", icon: null },
    { title: "Categories", link: "/categories", icon: null },
    ...(isSignedIn ? [
      { title: "Cart", link: "/cart", icon: <ShoppingCart className="w-5 h-5" /> },
      { title: "Wishlist", link: "/wishlist", icon: <Heart className="w-5 h-5" /> }
    ] : [])
  ];

  const SearchBar = () => (
    <div className="relative">
      <input
        type="text"
        placeholder="Search books..."
        className="w-full px-4 py-2 text-gray-900 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <Search className="absolute right-3 top-2.5 text-gray-500 w-5 h-5" />
    </div>
  );

  return (
    <nav className="fixed w-full top-0 z-50 bg-zinc-900 shadow-lg">
      {/* Main Navbar */}
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center space-x-3">
              <img
                src="https://cdn-icons-png.flaticon.com/128/10433/10433049.png"
                alt="logo"
                className="h-9 w-9"
              />
              <span className="text-white font-bold text-xl">BookStore</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {/* Search Bar */}
            <div className="w-96">
              <SearchBar />
            </div>

            {/* Navigation Links */}
            <div className="flex items-center space-x-6">
              {links.map((item, i) => (
                <Link
                  key={i}
                  to={item.link}
                  className="flex items-center space-x-1 text-gray-300 hover:text-white transition-colors duration-200"
                >
                  {item.icon}
                  <span>{item.title}</span>
                </Link>
              ))}
            </div>

            {/* Auth Section */}
            {!isSignedIn ? (
              <div className="flex items-center space-x-4">
                <Link
                  to="/login"
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Sign in
                </Link>
                <Link
                  to="/signup"
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Sign up
                </Link>
              </div>
            ) : (
              <div className="relative">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="flex items-center space-x-2 focus:outline-none"
                >
                  <img
                    src={user?.imageUrl || "https://cdn-icons-png.flaticon.com/128/149/149071.png"}
                    alt="profile"
                    className="h-8 w-8 rounded-full border-2 border-blue-500"
                  />
                  <span className="text-gray-300">{user?.firstName}</span>
                </button>

                {/* Dropdown Menu */}
                {showDropdown && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-50">
                    <div className="px-4 py-2 border-b">
                      <p className="text-sm font-medium text-gray-900">{user?.fullName}</p>
                      <p className="text-sm text-gray-500">{user?.primaryEmailAddress?.emailAddress}</p>
                    </div>
                    <Link
                      to="/profile"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setShowDropdown(false)}
                    >
                      Profile Settings
                    </Link>
                    <Link
                      to="/orders"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setShowDropdown(false)}
                    >
                      My Orders
                    </Link>
                    <SignOutButton>
                      <button className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                        Sign out
                      </button>
                    </SignOutButton>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsNavOpen(!isNavOpen)}
            className="md:hidden text-gray-300 hover:text-white"
          >
            {isNavOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {isNavOpen && (
        <div className="md:hidden bg-zinc-800">
          <div className="px-4 py-3">
            <SearchBar />
          </div>
          <div className="px-2 pt-2 pb-3 space-y-1">
            {links.map((item, i) => (
              <Link
                key={i}
                to={item.link}
                className="flex items-center space-x-2 text-gray-300 hover:text-white px-3 py-2 rounded-md text-base font-medium"
                onClick={() => setIsNavOpen(false)}
              >
                {item.icon}
                <span>{item.title}</span>
              </Link>
            ))}
            {!isSignedIn && (
              <div className="space-y-2 pt-4">
                <Link
                  to="/login"
                  className="block w-full text-center text-gray-300 hover:text-white px-3 py-2 rounded-md text-base font-medium"
                  onClick={() => setIsNavOpen(false)}
                >
                  Sign in
                </Link>
                <Link
                  to="/signup"
                  className="block w-full text-center bg-blue-600 text-white px-3 py-2 rounded-md text-base font-medium hover:bg-blue-700"
                  onClick={() => setIsNavOpen(false)}
                >
                  Sign up
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;